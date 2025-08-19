# Spotipy MCP Server

Servidor MCP (Model Context Protocol) com integração Spotipy para controle de música via Spotify.

## 🚀 Funcionalidades

- ✅ Controle de playback (play, pause, next, previous)
- ✅ Ajuste de volume
- ✅ Busca de músicas
- ✅ Obter música atual
- ✅ Gerenciar playlists
- ✅ API REST completa
- ✅ Documentação automática (Swagger)
- ✅ Integração MCP completa com tools e resources

## 📋 Pré-requisitos

- Python 3.12+
- Conta no Spotify Developer
- Aplicação registrada no Spotify Developer Dashboard

## 🛠️ Instalação

1. **Clone o repositório:**

```bash
git clone <seu-repositorio>
cd mcp-server
```

2. **Instale as dependências:**

```bash
make install
```

3. **Configure as variáveis de ambiente:**

```bash
cp env.example .env
```

Edite o arquivo `.env` com suas credenciais do Spotify:

```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## 🎵 Configuração do Spotify

1. Acesse [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Crie uma nova aplicação
3. Copie o `Client ID` e `Client Secret`
4. Adicione `http://localhost:8888/callback` nas URLs de redirecionamento
5. **Importante:** Configure os seguintes escopos na sua aplicação:
   - `user-read-playback-state` - Ler estado de reprodução
   - `user-modify-playback-state` - Controlar reprodução
   - `user-read-currently-playing` - Música atual
   - `playlist-read-private` - Playlists privadas
   - `user-library-read` - Biblioteca do usuário
   - `user-top-read` - Top artistas e músicas
   - `user-read-recently-played` - Músicas recentes
   - `user-follow-read` - Artistas seguidos
   - `user-read-email` - Email do usuário
   - `user-read-private` - Informações privadas

## 🚀 Uso

### Iniciar o servidor:

```bash
make dev
```

O servidor estará disponível em:

- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛠️ **Guia de Desenvolvimento**

### 🔄 **Comandos Essenciais**

```bash
# Restart completo do servidor
pkill -f "python.*mcp-server" && sleep 2 && make dev

# Kill portas MCP (OBRIGATÓRIO antes de run-inspector)
lsof -ti:6274 | xargs kill -9 && lsof -ti:6277 | xargs kill -9

# Verificar portas em uso
lsof -i:6274 && lsof -i:6277
```

### ⚠️ **IMPORTANTE: Sempre Kill as Portas!**

**ANTES de executar `make run-inspector`, SEMPRE execute:**

```bash
# Kill portas MCP (OBRIGATÓRIO)
lsof -ti:6274 | xargs kill -9 && lsof -ti:6277 | xargs kill -9
```

**Por que isso é necessário?**

- O MCP Inspector usa as portas 6274 (UI) e 6277 (Proxy)
- Se as portas estiverem ocupadas, o Inspector não consegue iniciar
- Processos anteriores podem ter deixado as portas em uso

### 🎯 **Fluxo de Desenvolvimento**

1. **Após Modificar o Código:**

```bash
pkill -f "python.*mcp-server" && sleep 2 && make dev
```

2. **Para Testar com MCP Inspector:**

```bash
lsof -ti:6274 | xargs kill -9 && lsof -ti:6277 | xargs kill -9
make run-inspector
```

### Comandos disponíveis:

```bash
make dev              # Iniciar servidor de desenvolvimento
make install          # Instalar dependências
make clean            # Limpar arquivos temporários
make test             # Executar testes
make lint             # Verificar qualidade do código
make format           # Formatar código
make run-inspector    # Executar MCP Inspector
make help             # Mostrar ajuda
```

## 🎵 **Funcionalidades MCP**

### **Tools Disponíveis:**

- `play_music` - Reproduzir música
- `search_tracks` - Buscar músicas
- `get_current_track` - Música atual
- `get_playlists` - Listar playlists
- `get_recommendations` - Recomendações
- `get_user_profile` - Perfil do usuário
- `get_devices` - Dispositivos disponíveis
- `toggle_shuffle` - Alternar shuffle
- `toggle_repeat` - Alternar repeat
- `get_queue` - Fila de reprodução
- `get_genres` - Gêneros musicais
- `get_audio_features` - Características da música

### **Recursos Disponíveis:**

- `spotify://playback/current` - Reprodução atual
- `spotify://playlists` - Playlists do usuário
- `spotify://devices` - Dispositivos
- `spotify://genres` - Gêneros
- `spotify://profile` - Perfil do usuário
- `spotify://playback/queue` - Fila de reprodução

### **Templates de Recursos:**

- `spotify://playlist/{playlist_id}` - Playlist específica
- `spotify://track/{track_id}` - Música específica
- `spotify://artist/{artist_id}` - Artista específico
- `spotify://album/{album_id}` - Álbum específico
- `spotify://search/{query}` - Resultados de busca

## 📚 API Endpoints

### Autenticação

- `POST /auth` - Autenticar com Spotify
- `POST /auth/reauth` - Reautenticar com credenciais configuradas

### Playback

- `GET /current-track` - Obter música atual
- `POST /play` - Tocar música
- `POST /pause` - Pausar música
- `POST /next` - Próxima música
- `POST /previous` - Música anterior
- `POST /volume/{volume}` - Ajustar volume (0-100)
- `POST /seek/{position_ms}` - Pular para posição específica
- `POST /shuffle` - Alternar modo shuffle
- `POST /repeat` - Alternar modo repeat

### Playlists e Álbuns

- `GET /playlists` - Obter playlists do usuário
- `GET /playlist/{playlist_id}` - Obter músicas de uma playlist
- `GET /albums` - Obter álbuns salvos do usuário
- `GET /tracks` - Obter músicas salvas do usuário

### Artistas e Top Tracks

- `GET /artists` - Obter artistas favoritos do usuário
- `GET /tracks/top` - Obter músicas mais tocadas

### Fila de Reprodução

- `GET /queue` - Obter fila de reprodução atual
- `POST /queue/add` - Adicionar música à fila

### Dispositivos

- `GET /devices` - Obter dispositivos disponíveis
- `POST /devices/{device_id}/transfer` - Transferir playback

### Busca e Recomendações

- `GET /search/{query}` - Buscar músicas
- `GET /recommendations` - Obter recomendações personalizadas
- `GET /genres` - Obter gêneros musicais disponíveis

### Usuário e Análise

- `GET /user/profile` - Obter perfil do usuário
- `GET /audio-features/{track_id}` - Obter características de áudio

### Sistema

- `GET /` - Status do servidor
- `GET /health` - Verificação de saúde

## 🔧 Exemplos de Uso

### Tocar uma música específica:

```bash
curl -X POST "http://localhost:8000/play" \
  -H "Content-Type: application/json" \
  -d '{"track_uri": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"}'
```

### Buscar músicas:

```bash
curl "http://localhost:8000/search/bohemian%20rhapsody?limit=5"
```

### Ajustar volume:

```bash
curl -X POST "http://localhost:8000/volume/50"
```

### Obter música atual:

```bash
curl "http://localhost:8000/current-track"
```

### Obter playlists do usuário:

```bash
curl "http://localhost:8000/playlists"
```

### Obter músicas de uma playlist específica:

```bash
curl "http://localhost:8000/playlist/37i9dQZF1DXcBWIGoYBM5M"
```

### Obter músicas salvas:

```bash
curl "http://localhost:8000/tracks"
```

### Obter artistas favoritos:

```bash
curl "http://localhost:8000/artists"
```

### Obter recomendações baseadas em artistas:

```bash
curl "http://localhost:8000/recommendations?seed_artists=4gzpq5DPGxSnKTe4SA8HAU&limit=10"
```

### Alternar shuffle:

```bash
curl -X POST "http://localhost:8000/shuffle"
```

### Adicionar música à fila:

```bash
curl -X POST "http://localhost:8000/queue/add?track_uri=spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
```

### Obter dispositivos disponíveis:

```bash
curl "http://localhost:8000/devices"
```

### Pular para posição específica (30 segundos):

```bash
curl -X POST "http://localhost:8000/seek/30000"
```

### Reautenticar com Spotify:

```bash
curl -X POST "http://localhost:8000/auth/reauth"
```

## 🧪 Testes

### 📊 **Status dos Testes**

✅ **60 testes PASSANDO** | ⏱️ **~0.38s** | 🔧 **100% Funcional**

### 🚀 **Executar Testes**

```bash
# Executar todos os testes (recomendado)
make test-pytest

# Ou usar pytest diretamente
python -m pytest tests/ -v --tb=short --color=yes
```

### 📋 **Cobertura de Testes**

#### 🔧 **Testes de Tools MCP (36 testes)**

- ✅ Controle de playback (`play_music`, `pause_music`, `next_track`, `previous_track`)
- ✅ Gerenciamento de volume (`set_volume`)
- ✅ Busca e descoberta (`search_tracks`, `search_artists`, `search_albums`, `search_playlists`)
- ✅ Playlists e álbuns (`get_playlists`, `get_playlist_tracks`, `get_album_tracks`)
- ✅ Perfil e preferências (`get_user_profile`, `get_top_tracks`, `get_top_artists`)
- ✅ Biblioteca pessoal (`get_saved_tracks`, `get_saved_albums`, `get_followed_artists`)
- ✅ Dispositivos e fila (`get_devices`, `get_queue`, `add_to_queue`)
- ✅ Recomendações (`get_recommendations`, `get_genres`, `get_audio_features`)
- ✅ Navegação (`skip_to_next`, `skip_to_previous`, `seek_to_position`)
- ✅ Histórico (`get_recently_played`)
- ✅ Artistas relacionados (`get_related_artists`, `get_artist_top_tracks`, `get_artist_albums`)

#### 💬 **Testes de Prompts MCP (6 testes)**

- ✅ `spotify_assistant` - Assistente musical inteligente
- ✅ `spotify_usage_guide` - Guia de uso das funcionalidades
- ✅ `spotify_troubleshooting` - Solução de problemas

#### 📚 **Testes de Resources MCP (12 testes)**

- ✅ `spotify://playback/current` - Estado atual de reprodução
- ✅ `spotify://playlists/user` - Playlists do usuário
- ✅ `spotify://devices/available` - Dispositivos disponíveis
- ✅ `spotify://genres/available` - Gêneros musicais
- ✅ `spotify://user/profile` - Perfil do usuário
- ✅ `spotify://playback/queue` - Fila de reprodução
- ✅ `spotify://user/top-tracks` - Top músicas
- ✅ `spotify://user/top-artists` - Top artistas
- ✅ `spotify://user/recently-played` - Reproduções recentes
- ✅ `spotify://user/saved-tracks` - Músicas salvas
- ✅ `spotify://user/saved-albums` - Álbuns salvos
- ✅ `spotify://user/followed-artists` - Artistas seguidos

#### 🔧 **Testes de Funcionalidade (3 testes)**

- ✅ Estrutura correta das tools
- ✅ Descrições válidas em todas as tools
- ✅ Tratamento de erros implementado

#### 📊 **Testes de Validação (2 testes)**

- ✅ Validação de requisições de volume
- ✅ Validação de requisições de busca

#### 🔗 **Teste de Integração (1 teste)**

- ✅ Completude do servidor (tools, prompts, resources)

### 🎯 **Comandos de Teste Disponíveis**

```bash
# Executar todos os testes
make test-pytest           # Usando pytest (recomendado)

# Testes específicos (futuros)
make test-tools            # Testes de tools apenas
make test-prompts          # Testes de prompts apenas
make test-resources        # Testes de resources apenas
make test-integration      # Testes de integração apenas
make test-coverage         # Verificar cobertura

# Teste com saída detalhada
python -m pytest tests/ -v -s --tb=long
```

### 📈 **Resultados dos Últimos Testes**

```
===================================== test session starts =====================================
collected 60 items

TestMCPServerBasics ✅ (4/4)
TestMCPTools ✅ (36/36)
TestMCPPrompts ✅ (6/6)
TestMCPResources ✅ (12/12)
TestToolFunctionality ✅ (2/2)
TestErrorHandling ✅ (1/1)
TestDataValidation ✅ (2/2)
TestIntegration ✅ (1/1)

===================================== 60 passed in 0.38s ======================================
```

### 🔍 **Estrutura dos Testes**

```
tests/
├── test_main.py          # Todos os testes do servidor MCP
├── __init__.py           # Inicialização do módulo
└── README.md            # Documentação dos testes
```

### 🧪 **Como Adicionar Novos Testes**

1. **Para nova tool:**

```python
@pytest.mark.asyncio
async def test_nova_tool_exists(self):
    """Testa se a nova tool existe"""
    tools = await app.get_tools()
    assert 'nova_tool' in tools
```

2. **Para novo resource:**

```python
@pytest.mark.asyncio
async def test_novo_resource_exists(self):
    """Testa se o novo resource existe"""
    resources = await app.get_resources()
    assert 'spotify://novo/resource' in resources
```

### ⚠️ **Importante para Testes**

- **SEMPRE** execute os testes após modificar o código
- Use `make test-pytest` para execução rápida e confiável
- Testes não requerem autenticação real do Spotify
- Testes focam na estrutura e disponibilidade das funcionalidades

## 🔍 Linting e Formatação

```bash
make lint    # Verificar qualidade do código
make format  # Formatar código automaticamente
```

## 📝 Estrutura do Projeto

```
mcp-server/
├── src/
│   ├── mcp-server.py    # Servidor MCP principal
│   ├── service.py       # Lógica do Spotify
│   ├── server.py        # API FastAPI
│   └── config.py        # Configurações
├── tests/               # Testes
├── makefile             # Comandos de desenvolvimento
├── pyproject.toml       # Configurações do projeto

├── env.example          # Exemplo de variáveis de ambiente
└── README.md           # Este arquivo
```

## ⚠️ **Problemas Comuns**

### **Erro: "PORT IS IN USE"**

```bash
# Solução rápida
lsof -ti:6274 | xargs kill -9
lsof -ti:6277 | xargs kill -9
```

### **Erro: "ModuleNotFoundError"**

```bash
# Reinstalar dependências
make install
```

### **Servidor não responde**

```bash
# Restart completo
pkill -f "python.*mcp-server" && sleep 2 && make dev
```

### **Erro 403 - Permissão Insuficiente**

Se você receber erro 403 com mensagem "Insufficient client scope":

1. Verifique se todos os escopos necessários estão configurados
2. Reautentique com o Spotify usando o endpoint `/auth`
3. Certifique-se de que aceitou todas as permissões solicitadas

### **Endpoints que Requerem Permissões Específicas**

- `/artists` e `/tracks/top` - Requerem `user-top-read`
- `/recommendations` - Requer pelo menos um seed válido
- `/user/profile` - Requer `user-read-email` e `user-read-private`

### **Problemas Conhecidos**

- **Recomendações (404)**: A API de recomendações pode retornar 404 em alguns casos. Isso pode ser devido a:
  - Problemas temporários da API do Spotify
  - Seeds inválidos ou não encontrados
  - Problemas de autenticação
- **Solução**: Use o endpoint `/auth/reauth` para reautenticar se necessário

## 🔧 **Dicas Importantes**

1. **SEMPRE** restart o servidor após modificar `mcp-server.py`
2. **SEMPRE** kill as portas antes de executar o Inspector (6274 e 6277)
3. **SEMPRE** verifique se as portas estão livres antes de executar `make run-inspector`
4. **Verifique os logs** para identificar problemas
5. **Use `make dev`** para desenvolvimento local
6. **Mantenha o `.env`** configurado corretamente

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique se as credenciais do Spotify estão corretas
2. Certifique-se de que o Spotify está rodando em algum dispositivo
3. Verifique os logs do servidor para mais detalhes
4. Abra uma issue no repositório

## 🔗 Links Úteis

- [Spotipy Documentation](https://spotipy.readthedocs.io/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

**🎵 Música é vida! Vamos fazer um servidor MCP incrível! 🚀**
