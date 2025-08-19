#!/usr/bin/env python3
"""
Script principal para executar o Spotipy MCP Server
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar e executar o servidor
from mcp_server import app

if __name__ == "__main__":
    # Não imprimir mensagens quando usado via STDIO (MCP)
    import sys
    if not sys.stdin.isatty():
        # Executar silenciosamente para MCP
        app.run()
    else:
        # Executar com mensagens para terminal
        print("🎵 Iniciando Spotipy MCP Server...")
        app.run()
