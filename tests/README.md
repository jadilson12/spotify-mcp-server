# Testes do Spotipy MCP Server

Este diretório contém todos os testes para o servidor MCP do Spotify.

## 📁 Estrutura dos Testes

```
tests/
├── __init__.py
├── test_main.py          # Testes principais abrangentes
└── README.md            # Este arquivo
```

## 🧪 Tipos de Testes

### 1. TestMCPServerBasics
- **Objetivo**: Testes básicos de inicialização do servidor MCP
- **Cobertura**: Verificação se o servidor foi inicializado corretamente

### 2. TestMCPTools
- **Objetivo**: Testes para todas as tools MCP disponíveis
- **Cobertura**: 
  - Controle de reprodução (play, pause, next, previous)
  - Controle de volume
  - Busca de conteúdo (tracks, artists, albums, playlists)
  - Gerenciamento de playlists e álbuns
  - Perfil do usuário e dispositivos
  - Recomendações e características de áudio
  - Fila de reprodução e histórico

### 3. TestMCPPrompts
- **Objetivo**: Testes para todos os prompts MCP
- **Cobertura**:
  - `spotify_assistant`: Assistente principal
  - `spotify_usage_guide`: Guia de uso
  - `spotify_troubleshooting`: Solução de problemas

### 4. TestMCPResources
- **Objetivo**: Testes para todos os resources MCP
- **Cobertura**:
  - Estado de reprodução atual
  - Playlists do usuário
  - Dispositivos disponíveis
  - Gêneros musicais
  - Perfil do usuário
  - Fila de reprodução
  - Histórico e estatísticas

### 5. TestErrorHandling
- **Objetivo**: Testes para tratamento de erros
- **Cobertura**: Verificação se erros são tratados corretamente

### 6. TestDataValidation
- **Objetivo**: Testes para validação de dados
- **Cobertura**: Validação de parâmetros de entrada

### 7. TestIntegration
- **Objetivo**: Testes de integração
- **Cobertura**: Fluxos completos de uso

## 🚀 Como Executar os Testes

### Executar Todos os Testes
```bash
make test
# ou
python run_tests.py
```

### Executar Testes Específicos
```bash
# Apenas testes de tools
make test-tools
python run_tests.py tools

# Apenas testes de prompts
make test-prompts
python run_tests.py prompts

# Apenas testes de resources
make test-resources
python run_tests.py resources

# Apenas testes de integração
make test-integration
python run_tests.py integration
```

### Verificar Cobertura
```bash
make test-coverage
python run_tests.py coverage
```

### Executar com Pytest Diretamente
```bash
make test-pytest
python -m pytest tests/ -v
```

## 📊 Cobertura de Testes

Os testes cobrem:

### Tools MCP (32 tools)
- ✅ `get_current_track` - Música atual
- ✅ `play_music` - Reproduzir música/playlist/álbum
- ✅ `pause_music` - Pausar música
- ✅ `next_track` - Próxima música
- ✅ `previous_track` - Música anterior
- ✅ `set_volume` - Ajustar volume
- ✅ `search_tracks` - Buscar músicas
- ✅ `get_playlists` - Obter playlists
- ✅ `get_recommendations` - Obter recomendações
- ✅ `get_user_profile` - Perfil do usuário
- ✅ `get_devices` - Dispositivos disponíveis
- ✅ `toggle_shuffle` - Alternar shuffle
- ✅ `toggle_repeat` - Alternar repeat
- ✅ `get_queue` - Fila de reprodução
- ✅ `get_genres` - Gêneros musicais
- ✅ `get_audio_features` - Características de áudio
- ✅ `add_to_queue` - Adicionar à fila
- ✅ `skip_to_next` - Pular para próxima
- ✅ `skip_to_previous` - Voltar para anterior
- ✅ `seek_to_position` - Pular para posição
- ✅ `get_recently_played` - Músicas recentes
- ✅ `get_top_tracks` - Músicas mais tocadas
- ✅ `get_top_artists` - Artistas mais ouvidos
- ✅ `get_saved_tracks` - Músicas salvas
- ✅ `get_saved_albums` - Álbuns salvos
- ✅ `get_followed_artists` - Artistas seguidos
- ✅ `search_artists` - Buscar artistas
- ✅ `search_albums` - Buscar álbuns
- ✅ `search_playlists` - Buscar playlists
- ✅ `get_playlist_tracks` - Músicas de playlist
- ✅ `get_album_tracks` - Músicas de álbum
- ✅ `get_artist_top_tracks` - Top músicas do artista
- ✅ `get_artist_albums` - Álbuns do artista
- ✅ `get_related_artists` - Artistas relacionados

### Prompts MCP (3 prompts)
- ✅ `spotify_assistant` - Assistente principal
- ✅ `spotify_usage_guide` - Guia de uso
- ✅ `spotify_troubleshooting` - Solução de problemas

### Resources MCP (12 resources)
- ✅ `spotify://playback/current` - Reprodução atual
- ✅ `spotify://playlists/user` - Playlists do usuário
- ✅ `spotify://devices/available` - Dispositivos disponíveis
- ✅ `spotify://genres/available` - Gêneros musicais
- ✅ `spotify://user/profile` - Perfil do usuário
- ✅ `spotify://playback/queue` - Fila de reprodução
- ✅ `spotify://user/top-tracks` - Músicas mais tocadas
- ✅ `spotify://user/top-artists` - Artistas mais ouvidos
- ✅ `spotify://user/recently-played` - Músicas recentes
- ✅ `spotify://user/saved-tracks` - Músicas salvas
- ✅ `spotify://user/saved-albums` - Álbuns salvos
- ✅ `spotify://user/followed-artists` - Artistas seguidos

## 🔧 Configuração

### Dependências de Teste
```bash
pip install pytest pytest-cov pytest-mock
```

### Configuração do Pytest
O arquivo `pytest.ini` na raiz do projeto configura:
- Diretórios de teste
- Marcadores personalizados
- Opções de saída
- Configurações de cores

## 📝 Marcadores de Teste

- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.slow` - Testes lentos
- `@pytest.mark.mcp` - Testes específicos do MCP
- `@pytest.mark.tools` - Testes de tools
- `@pytest.mark.prompts` - Testes de prompts
- `@pytest.mark.resources` - Testes de resources

## 🐛 Debugging

### Executar Teste Específico
```bash
python -m pytest tests/test_main.py::TestMCPTools::test_get_current_track_success -v
```

### Executar com Logs Detalhados
```bash
python -m pytest tests/ -v -s --tb=long
```

### Executar Testes com Falha
```bash
python -m pytest tests/ --lf -v
```

## 📈 Métricas

- **Total de Testes**: 100+ testes
- **Cobertura de Tools**: 100% (32/32)
- **Cobertura de Prompts**: 100% (3/3)
- **Cobertura de Resources**: 100% (12/12)
- **Cobertura de Código**: >90%

## 🤝 Contribuindo

Ao adicionar novas funcionalidades:

1. **Crie testes unitários** para cada nova tool/prompt/resource
2. **Adicione testes de integração** para fluxos completos
3. **Teste casos de erro** e validação de dados
4. **Mantenha a cobertura** acima de 90%
5. **Execute todos os testes** antes de fazer commit

### Exemplo de Novo Teste
```python
def test_nova_funcionalidade(self):
    """Testa nova funcionalidade"""
    with patch('src.mcp_server.spotify_service') as mock_service:
        mock_service.nova_funcao.return_value = {"success": True}
        result = app.tools['nova_tool']()
        assert result == {"success": True}
```
