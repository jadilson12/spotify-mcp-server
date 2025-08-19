# 🔒 Política de Segurança

## ⚠️ **Importante: Credenciais do Spotify**

Este repositório **NÃO** deve conter credenciais reais do Spotify. Sempre use o arquivo `.env.example` como template.

### 🚨 **Nunca commite:**

- ✅ `.env` (arquivo com credenciais reais)
- ✅ `.spotify_token_cache` (cache de tokens)
- ✅ Qualquer arquivo com `SPOTIFY_CLIENT_ID` ou `SPOTIFY_CLIENT_SECRET` reais

### ✅ **Sempre commite:**

- ✅ `env.example` (template seguro)
- ✅ `.gitignore` (configurado para ignorar arquivos sensíveis)

## 🔧 **Configuração Segura**

1. **Clone o repositório:**
```bash
git clone <seu-repositorio>
cd mcp-server
```

2. **Configure suas credenciais (localmente):**
```bash
cp env.example .env
# Edite .env com suas credenciais reais
```

3. **Verifique se .env está no .gitignore:**
```bash
git status
# .env NÃO deve aparecer nos arquivos tracked
```

## 🛡️ **Configurações de Segurança**

### **Produção:**
- `HOST=127.0.0.1` (não 0.0.0.0)
- `DEBUG=false`
- `LOG_LEVEL=WARNING`

### **Desenvolvimento:**
- `HOST=0.0.0.0` (para testes)
- `DEBUG=true`
- `LOG_LEVEL=INFO`

## 🚨 **Se encontrar credenciais expostas:**

1. **Imediatamente:**
   - Revogue as credenciais no Spotify Developer Dashboard
   - Gere novas credenciais
   - Atualize seu arquivo `.env` local

2. **No repositório:**
   - Remova o commit com credenciais
   - Force push para limpar o histórico
   - Notifique colaboradores

## 📞 **Reportar Vulnerabilidades**

Se encontrar uma vulnerabilidade de segurança:

1. **NÃO** abra uma issue pública
2. **NÃO** discuta em pull requests públicos
3. **Entre em contato** via email ou mensagem privada

## 🔍 **Verificação de Segurança**

Antes de fazer push:

```bash
# Verificar se .env não está sendo commitado
git status | grep .env

# Verificar se não há credenciais no código
grep -r "SPOTIFY_CLIENT_ID\|SPOTIFY_CLIENT_SECRET" . --exclude-dir=.venv --exclude-dir=__pycache__

# Verificar se .gitignore está correto
cat .gitignore | grep -E "\.env|token|secret"
```

## ✅ **Checklist de Segurança**

- [ ] `.env` está no `.gitignore`
- [ ] `.spotify_token_cache` está no `.gitignore`
- [ ] `env.example` não contém credenciais reais
- [ ] `DEBUG=false` em produção
- [ ] `HOST=127.0.0.1` em produção
- [ ] Logs não expõem informações sensíveis
- [ ] Dependências atualizadas e seguras

---

**🎵 Lembre-se: Segurança em primeiro lugar! 🔒**
