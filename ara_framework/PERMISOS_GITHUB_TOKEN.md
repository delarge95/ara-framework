# 🔑 PERMISOS DEL GITHUB TOKEN PARA GITHUB MODELS

## ⚠️ IMPORTANTE: Tokens Fine-Grained vs Classic

**GitHub Models requiere un tipo específico de token**:

### ❌ NO FUNCIONA: Fine-grained token (por repositorio)

- Los tokens "fine-grained" están limitados a repositorios específicos
- GitHub Models API **NO** es un recurso de repositorio
- **No puedes usar un token fine-grained** para GitHub Models

### ✅ SÍ FUNCIONA: Classic Personal Access Token

**Debes crear un token "Classic"** con estos permisos:

---

## 🎯 PERMISOS REQUERIDOS

### Mínimo necesario:

```
✅ read:packages    - Acceso a GitHub Packages (incluye GitHub Models)
```

### Recomendado (para desarrollo completo):

```
✅ read:packages    - Acceso a GitHub Models API
✅ repo (opcional)  - Solo si necesitas acceso a repos privados
```

---

## 📝 CÓMO CREAR EL TOKEN CORRECTO

### Paso 1: Ir a configuración de tokens

```
https://github.com/settings/tokens
```

### Paso 2: Crear token CLASSIC

```
Click en: "Generate new token" → "Generate new token (classic)"
NO uses: "Fine-grained token" ❌
```

### Paso 3: Configurar permisos

```
Note: "GitHub Models API Access"
Expiration: 90 days (o "No expiration" si prefieres)

Seleccionar scopes:
✅ read:packages
   └─ Este es el ÚNICO permiso necesario para GitHub Models
```

### Paso 4: Generar y copiar

```
Click "Generate token"
Copiar el token: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
⚠️ Se muestra solo UNA vez
```

---

## 🔧 CONFIGURAR EN EL PROYECTO

### Opción 1: Variable de entorno (.env)

```bash
# Agregar a .env:
GITHUB_TOKEN=ghp_tu_token_aqui
```

### Opción 2: Variable de entorno del sistema (Windows)

```powershell
# PowerShell:
$env:GITHUB_TOKEN = "ghp_tu_token_aqui"

# CMD:
set GITHUB_TOKEN=ghp_tu_token_aqui
```

### Opción 3: Configuración permanente (Windows)

```powershell
# PowerShell (como administrador):
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_tu_token_aqui', 'User')
```

---

## ✅ PROBAR EL TOKEN

### Test rápido con curl:

```bash
curl -H "Authorization: Bearer ghp_tu_token_aqui" \
  https://models.inference.ai.azure.com/chat/completions \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"test"}]}'
```

### Test con Python:

```bash
python test_github_models_quick.py
```

---

## 🚫 PROBLEMAS COMUNES

### Error 1: "Authentication required"

```
Causa: Token fine-grained (por repositorio)
Solución: Crear token Classic con read:packages
```

### Error 2: "Invalid token"

```
Causa: Token expirado o mal copiado
Solución: Verificar que el token esté completo y no expirado
```

### Error 3: "Insufficient permissions"

```
Causa: Falta el scope read:packages
Solución: Recrear token con read:packages habilitado
```

### Error 4: "Rate limit exceeded"

```
Causa: Demasiadas requests en poco tiempo
Límite: ~100-200 requests/hora durante beta
Solución: Esperar o implementar rate limiting
```

---

## 📊 COMPARACIÓN DE TOKENS

| Característica            | Classic Token    | Fine-grained Token |
| ------------------------- | ---------------- | ------------------ |
| **Scope por repositorio** | ❌ Global        | ✅ Por repo        |
| **GitHub Models**         | ✅ **FUNCIONA**  | ❌ No funciona     |
| **Seguridad**             | ⚠️ Acceso amplio | ✅ Más seguro      |
| **Expiración**            | Configurable     | Máximo 1 año       |
| **Recomendado para**      | APIs globales    | Repos específicos  |

---

## 🔐 SEGURIDAD

### ✅ Buenas prácticas:

1. **Nunca subas el token a GitHub**

   ```bash
   # Verifica que .env esté en .gitignore
   echo .env >> .gitignore
   ```

2. **Usa expiración razonable**

   - Desarrollo: 90 días
   - Producción: Variables de entorno del servidor

3. **Permisos mínimos**

   - Solo `read:packages` para GitHub Models
   - No agregues `repo` a menos que lo necesites

4. **Rotar tokens regularmente**

   - Cada 3-6 meses
   - Inmediatamente si se expone

5. **Usar secrets en producción**

   ```bash
   # GitHub Actions:
   secrets.GITHUB_TOKEN

   # Vercel/Netlify:
   Environment Variables

   # Docker:
   docker run -e GITHUB_TOKEN=$GITHUB_TOKEN ...
   ```

---

## ✅ CHECKLIST FINAL

Antes de continuar, verifica:

- [ ] Token creado como "Classic" (no fine-grained)
- [ ] Scope `read:packages` habilitado
- [ ] Token copiado correctamente (empieza con `ghp_`)
- [ ] Token agregado a `.env` o variable de entorno
- [ ] `.env` está en `.gitignore`
- [ ] Test ejecutado: `python test_github_models_quick.py`

---

## 📚 REFERENCIAS

**Documentación oficial**:

- GitHub Models: https://docs.github.com/github-models
- Personal Access Tokens: https://docs.github.com/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- GitHub Packages: https://docs.github.com/packages

**Crear tokens**:

- Classic tokens: https://github.com/settings/tokens
- Fine-grained tokens: https://github.com/settings/tokens?type=beta

---

## 💡 RESUMEN RÁPIDO

**TL;DR**:

1. ❌ Tu token fine-grained (por repositorio) NO funciona con GitHub Models
2. ✅ Necesitas crear un token **Classic** con scope `read:packages`
3. 📝 Ir a: https://github.com/settings/tokens
4. ➕ "Generate new token (classic)"
5. ✅ Marcar: `read:packages`
6. 💾 Copiar token y agregarlo a `.env`
7. 🧪 Probar con: `python test_github_models_quick.py`
