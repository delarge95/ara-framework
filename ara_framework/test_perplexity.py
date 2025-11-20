"""
Test Perplexity API Integration

This script demonstrates how to use Perplexity AI for real-time web search
in the ARA Framework.

Usage:
    python test_perplexity.py
"""

import asyncio
import structlog
from tools.perplexity_tool import perplexity_search, perplexity_search_fast
from config.settings import settings

logger = structlog.get_logger(__name__)


async def test_perplexity_basic():
    """Test basic Perplexity search."""
    print("\n" + "="*70)
    print("🔍 Test 1: Basic Perplexity Search")
    print("="*70)
    
    query = "Latest developments in Rust WebAssembly for real-time audio processing"
    
    print(f"\n📝 Query: {query}")
    print(f"⏱️  Searching with Perplexity...\n")
    
    result = await perplexity_search(
        query=query,
        search_recency_filter="month",
        max_tokens=2000,
    )
    
    print(result)
    print(f"\n✅ Search completed! Response length: {len(result)} characters")


async def test_perplexity_fast():
    """Test fast Perplexity search (smaller model)."""
    print("\n" + "="*70)
    print("⚡ Test 2: Fast Perplexity Search")
    print("="*70)
    
    query = "Top Rust WebAssembly libraries for audio processing"
    
    print(f"\n📝 Query: {query}")
    print(f"⏱️  Searching with fast model...\n")
    
    result = await perplexity_search_fast(
        query=query,
        max_tokens=1000,
    )
    
    print(result)
    print(f"\n✅ Fast search completed! Response length: {len(result)} characters")


async def test_perplexity_recent():
    """Test search with recent filter (last 24 hours)."""
    print("\n" + "="*70)
    print("📰 Test 3: Recent News (Last 24 Hours)")
    print("="*70)
    
    query = "Rust WebAssembly news announcements"
    
    print(f"\n📝 Query: {query}")
    print(f"⏱️  Searching last 24 hours...\n")
    
    result = await perplexity_search(
        query=query,
        search_recency_filter="day",
        max_tokens=1500,
    )
    
    print(result)
    print(f"\n✅ Recent search completed!")


async def test_perplexity_comparison():
    """Compare Perplexity with traditional scraping."""
    print("\n" + "="*70)
    print("⚖️  Test 4: Perplexity vs Traditional Scraping")
    print("="*70)
    
    query = "Best practices for Rust WebAssembly audio processing"
    
    print(f"\n📝 Query: {query}")
    print(f"\n🔍 Method 1: Perplexity (LLM + Web Search)")
    print("-" * 70)
    
    result_perplexity = await perplexity_search(
        query=query,
        search_recency_filter="month",
        max_tokens=1500,
    )
    
    print(f"✅ Perplexity: {len(result_perplexity)} characters")
    print(f"   - Includes: Summary + Citations + Related Questions")
    print(f"   - Processing: LLM-enhanced results")
    
    print(f"\n🌐 Method 2: Traditional Scraping (for comparison)")
    print("-" * 70)
    print(f"   - Would require: Multiple URL visits")
    print(f"   - Would need: Manual parsing and cleaning")
    print(f"   - No built-in: LLM analysis or citations")
    
    print(f"\n💡 Perplexity Advantages:")
    print(f"   ✅ Real-time web results")
    print(f"   ✅ LLM-processed summaries")
    print(f"   ✅ Automatic citations")
    print(f"   ✅ Related questions")
    print(f"   ✅ No need for separate scraping")


async def main():
    """Run all Perplexity tests."""
    print("\n" + "="*70)
    print("🧪 PERPLEXITY API INTEGRATION TESTS")
    print("="*70)
    
    if not settings.PERPLEXITY_API_KEY:
        print("\n❌ ERROR: PERPLEXITY_API_KEY not found in environment!")
        print("\n📋 Setup Instructions:")
        print("   1. Get API key from: https://www.perplexity.ai/settings/api")
        print("   2. Add to .env file: PERPLEXITY_API_KEY=pplx-xxxxx")
        print("   3. Restart the application")
        return
    
    print(f"\n✅ Perplexity API Key: {settings.PERPLEXITY_API_KEY[:10]}...****")
    print(f"✅ Model: {settings.PERPLEXITY_MODEL}")
    
    try:
        # Run tests
        await test_perplexity_basic()
        await asyncio.sleep(2)  # Rate limit buffer
        
        await test_perplexity_fast()
        await asyncio.sleep(2)
        
        await test_perplexity_recent()
        await asyncio.sleep(2)
        
        await test_perplexity_comparison()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📊 Summary:")
        print("   - Perplexity provides real-time web search + LLM analysis")
        print("   - Best for: Recent trends, current events, community insights")
        print("   - Complements: Traditional scraping and academic search")
        print("   - Integration: Ready to use in Niche Analyst (Agent 1)")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.error("test_failed", error=str(e))


if __name__ == "__main__":
    asyncio.run(main())
