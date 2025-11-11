"""
Base classes para MCP (Model Context Protocol) adapters.

Fuente: docs/04_ARCHITECTURE.md (MCP Layer Integration)

Todos los MCP servers deben heredar de MCPAdapter y implementar
los métodos abstractos.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Generic, TypeVar
import asyncio
from datetime import datetime
import structlog
from redis.asyncio import Redis

from config.settings import settings

logger = structlog.get_logger()

T = TypeVar("T")


class MCPAdapter(ABC, Generic[T]):
    """
    Adaptador base para MCP servers.
    
    Funcionalidades comunes:
    - Rate limiting
    - Caching (Redis)
    - Error handling
    - Telemetry
    - Retry logic
    """
    
    def __init__(
        self,
        name: str,
        redis_client: Optional[Redis] = None,
        rate_limit_rpm: int = 60,
        cache_ttl: int = 3600,
    ):
        self.name = name
        self.redis = redis_client
        self.rate_limit_rpm = rate_limit_rpm
        self.cache_ttl = cache_ttl
        
        self.logger = logger.bind(mcp_adapter=name)
        
        # Rate limiter (sliding window)
        self._request_timestamps: list[float] = []
        self._rate_limit_lock = asyncio.Lock()
    
    @abstractmethod
    async def connect(self) -> None:
        """Establece conexión con el MCP server."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Cierra conexión con el MCP server."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Verifica que el MCP server esté disponible."""
        pass
    
    async def _wait_for_rate_limit(self) -> None:
        """
        Rate limiting con sliding window.
        
        Ejemplo: Si rate_limit_rpm=60, solo permite 60 requests en 60 segundos.
        """
        async with self._rate_limit_lock:
            now = asyncio.get_event_loop().time()
            window_start = now - 60.0
            
            # Limpiar timestamps antiguos
            self._request_timestamps = [
                ts for ts in self._request_timestamps if ts > window_start
            ]
            
            # Si alcanzamos el límite, esperar
            if len(self._request_timestamps) >= self.rate_limit_rpm:
                oldest = self._request_timestamps[0]
                wait_time = 60.0 - (now - oldest)
                
                if wait_time > 0:
                    self.logger.debug(
                        "rate_limit_waiting",
                        wait_seconds=wait_time,
                        current_requests=len(self._request_timestamps),
                    )
                    await asyncio.sleep(wait_time)
            
            # Registrar este request
            self._request_timestamps.append(now)
    
    async def _get_cached(self, cache_key: str) -> Optional[T]:
        """Obtiene valor del cache (Redis)."""
        if not self.redis:
            return None
        
        try:
            cached = await self.redis.get(cache_key)
            if cached:
                self.logger.debug("cache_hit", key=cache_key)
                import json
                return json.loads(cached)
            else:
                self.logger.debug("cache_miss", key=cache_key)
                return None
        except Exception as e:
            self.logger.error("cache_get_error", error=str(e), key=cache_key)
            return None
    
    async def _set_cached(
        self,
        cache_key: str,
        value: T,
        ttl: Optional[int] = None,
    ) -> None:
        """Guarda valor en cache (Redis)."""
        if not self.redis:
            return
        
        try:
            import json
            ttl = ttl or self.cache_ttl
            await self.redis.setex(
                cache_key,
                ttl,
                json.dumps(value, default=str)
            )
            self.logger.debug("cache_set", key=cache_key, ttl=ttl)
        except Exception as e:
            self.logger.error("cache_set_error", error=str(e), key=cache_key)
    
    async def _invalidate_cache(self, pattern: str) -> int:
        """Invalida cache que coincida con el patrón."""
        if not self.redis:
            return 0
        
        try:
            keys = []
            async for key in self.redis.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                deleted = await self.redis.delete(*keys)
                self.logger.info("cache_invalidated", pattern=pattern, count=deleted)
                return deleted
            return 0
        except Exception as e:
            self.logger.error("cache_invalidate_error", error=str(e), pattern=pattern)
            return 0
    
    def _make_cache_key(self, *parts: str) -> str:
        """Genera cache key consistente."""
        return f"mcp:{self.name}:{':'.join(parts)}"
    
    async def __aenter__(self):
        """Context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.disconnect()
