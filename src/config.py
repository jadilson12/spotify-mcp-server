"""
Configurações centralizadas do projeto
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Diretório base do projeto (raiz de mcp-server), independente do CWD
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis de ambiente a partir do .env absoluto
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

# Configurações do Spotify
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv(
    "SPOTIFY_REDIRECT_URI", "http://localhost:8000/callback"
)

# Escopos do Spotify
SPOTIFY_SCOPES = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "playlist-read-private",
    "user-library-read",
    "user-library-modify",  # Necessário para adicionar/remover favoritos
    "user-top-read",
    "user-read-recently-played",
    "user-follow-read",
    "user-read-email",
    "user-read-private",
]

# Configurações do servidor
HOST = os.getenv("HOST", "127.0.0.1")  # Mais seguro para produção
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"  # Desabilitado por padrão

# Configurações do MCP
MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME", "spotipy-mcp-server")
MCP_SERVER_VERSION = os.getenv("MCP_SERVER_VERSION", "1.0.0")

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configurações de captura de stdout
CAPTURE_STDOUT = os.getenv("CAPTURE_STDOUT", "true").lower() == "true"

# Caminho absoluto para o cache do token do Spotify (evita depender do CWD)
TOKEN_CACHE_PATH = os.getenv(
    "SPOTIFY_TOKEN_CACHE_PATH", str(BASE_DIR / ".spotify_token_cache")
)
