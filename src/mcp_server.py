#!/usr/bin/env python3
"""
FastMCP Server para integração com Spotify
"""

import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import BaseModel

try:
    from .config import MCP_SERVER_NAME, MCP_SERVER_VERSION
    from .service import spotify_service
except ImportError:
    from config import MCP_SERVER_NAME, MCP_SERVER_VERSION
    from service import spotify_service

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar instância do FastMCP
app = FastMCP(name=MCP_SERVER_NAME, version=MCP_SERVER_VERSION)


class PlayMusicRequest(BaseModel):
    """Modelo para requisição de tocar música"""

    track_uri: Optional[str] = None
    playlist_uri: Optional[str] = None
    album_uri: Optional[str] = None


class VolumeRequest(BaseModel):
    """Modelo para requisição de volume"""

    volume: int


class SearchRequest(BaseModel):
    """Modelo para requisição de busca"""

    query: str
    limit: int = 10


class RecommendationsRequest(BaseModel):
    """Modelo para requisição de recomendações"""

    seed_artists: Optional[str] = None
    seed_tracks: Optional[str] = None
    seed_genres: Optional[str] = None
    limit: int = 20


@app.tool()
def get_current_track() -> Dict[str, Any]:
    """Obter música atual tocando no Spotify"""
    try:
        return spotify_service.get_current_track()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def play_music(request: PlayMusicRequest) -> Dict[str, str]:
    """Tocar música no Spotify"""
    try:
        import time

        start_time = time.time()

        result = spotify_service.play_music(
            track_uri=request.track_uri,
            playlist_uri=request.playlist_uri,
            album_uri=request.album_uri,
        )

        elapsed_time = time.time() - start_time
        logger.info(f"play_music executado em {elapsed_time:.2f}s")

        return result
    except Exception as e:
        logger.error(f"Erro em play_music: {e}")
        return {"error": str(e)}


@app.tool()
def pause_music() -> Dict[str, str]:
    """Pausar música no Spotify"""
    try:
        return spotify_service.pause_music()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def next_track() -> Dict[str, str]:
    """Avançar para próxima música"""
    try:
        return spotify_service.next_track()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def previous_track() -> Dict[str, str]:
    """Voltar para música anterior"""
    try:
        return spotify_service.previous_track()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def set_volume(request: VolumeRequest) -> Dict[str, str]:
    """Ajustar volume (0-100)"""
    try:
        return spotify_service.set_volume(request.volume)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def search_tracks(request: SearchRequest) -> Dict[str, List[Dict[str, Any]]]:
    """Buscar músicas no Spotify"""
    try:
        return spotify_service.search_tracks(request.query, request.limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_playlists() -> Dict[str, List[Dict[str, Any]]]:
    """Obter playlists do usuário"""
    try:
        return spotify_service.get_playlists()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_recommendations(
    request: RecommendationsRequest,
) -> Dict[str, List[Dict[str, Any]]]:
    """Obter recomendações baseadas em artistas, músicas ou gêneros"""
    try:
        return spotify_service.get_recommendations(
            seed_artists=request.seed_artists,
            seed_tracks=request.seed_tracks,
            seed_genres=request.seed_genres,
            limit=request.limit,
        )
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_user_profile() -> Dict[str, Any]:
    """Obter perfil do usuário Spotify"""
    try:
        return spotify_service.get_user_profile()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_devices() -> Dict[str, List[Dict[str, Any]]]:
    """Obter dispositivos disponíveis"""
    try:
        return spotify_service.get_devices()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_queue() -> Dict[str, Any]:
    """Obter fila de reprodução atual"""
    try:
        return spotify_service.get_queue()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_genres() -> Dict[str, List[str]]:
    """Obter gêneros musicais disponíveis"""
    try:
        return spotify_service.get_genres()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_audio_features(track_id: str) -> Dict[str, Any]:
    """Obter características de áudio de uma música (tempo, energia, dançabilidade, etc.)

    Nota: Pode requerer Spotify Premium. Se retornar erro 403, as características
    podem não estar disponíveis.
    """
    try:
        return spotify_service.get_audio_features(track_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_track_tempo(track_id: str) -> Dict[str, Any]:
    """Obter especificamente a batida (tempo/BPM) de uma música

    Nota: Pode requerer Spotify Premium. Se retornar erro 403, o tempo pode não
    estar disponível.
    """
    try:
        return spotify_service.get_track_tempo(track_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_audio_features_by_uri(track_uri: str) -> Dict[str, Any]:
    """Obter características de áudio usando URI da música (spotify:track:ID)"""
    try:
        return spotify_service.get_audio_features_by_uri(track_uri)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_track_tempo_by_uri(track_uri: str) -> Dict[str, Any]:
    """Obter batida (tempo/BPM) usando URI da música (spotify:track:ID)"""
    try:
        return spotify_service.get_track_tempo_by_uri(track_uri)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def add_track_to_favorites(track_id: str) -> Dict[str, str]:
    """Adicionar música aos favoritos (liked songs) usando track ID"""
    try:
        return spotify_service.add_track_to_favorites(track_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def remove_track_from_favorites(track_id: str) -> Dict[str, str]:
    """Remover música dos favoritos (liked songs) usando track ID"""
    try:
        return spotify_service.remove_track_from_favorites(track_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def check_track_in_favorites(track_id: str) -> Dict[str, Any]:
    """Verificar se uma música está nos favoritos usando track ID"""
    try:
        return spotify_service.check_track_in_favorites(track_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def check_track_in_favorites_by_uri(track_uri: str) -> Dict[str, Any]:
    """Verificar se uma música está nos favoritos usando URI da música"""
    try:
        return spotify_service.check_track_in_favorites_by_uri(track_uri)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_listening_analytics(limit: int = 50) -> Dict[str, Any]:
    """Obter dados analíticos de escuta para gerar gráficos HTML"""
    try:
        return spotify_service.get_listening_analytics(limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def search_and_add_to_queue(query: str, limit: int = 10) -> Dict[str, Any]:
    """Buscar músicas e adicionar todas à fila de reprodução"""
    try:
        return spotify_service.search_and_add_to_queue(query, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def search_and_add_to_favorites(query: str, limit: int = 10) -> Dict[str, Any]:
    """Buscar músicas e adicionar todas aos favoritos"""
    try:
        return spotify_service.search_and_add_to_favorites(query, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def search_and_play_all(query: str, limit: int = 10) -> Dict[str, Any]:
    """Buscar músicas e reproduzir todas em sequência (primeira + fila)"""
    try:
        return spotify_service.search_and_play_all(query, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def add_to_queue(track_uri: str) -> Dict[str, Any]:
    """Adicionar música à fila de reprodução"""
    try:
        return spotify_service.add_to_queue(track_uri)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def skip_to_next() -> Dict[str, Any]:
    """Pular para próxima música"""
    try:
        return spotify_service.skip_to_next()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def skip_to_previous() -> Dict[str, Any]:
    """Voltar para música anterior"""
    try:
        return spotify_service.skip_to_previous()
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def seek_to_position(position_ms: int) -> Dict[str, Any]:
    """Pular para posição específica na música (em milissegundos)"""
    try:
        return spotify_service.seek_to_position(position_ms)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_recently_played(limit: int = 20) -> Dict[str, Any]:
    """Obter músicas reproduzidas recentemente"""
    try:
        return spotify_service.get_recently_played(limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_top_tracks(limit: int = 20, time_range: str = "medium_term") -> Dict[str, Any]:
    """Obter músicas mais tocadas do usuário"""
    try:
        return spotify_service.get_top_tracks(limit, time_range)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_top_artists(limit: int = 20, time_range: str = "medium_term") -> Dict[str, Any]:
    """Obter artistas mais ouvidos do usuário"""
    try:
        return spotify_service.get_top_artists(limit, time_range)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_saved_tracks(limit: int = 20) -> Dict[str, Any]:
    """Obter músicas salvas do usuário"""
    try:
        return spotify_service.get_saved_tracks(limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_saved_albums(limit: int = 20) -> Dict[str, Any]:
    """Obter álbuns salvos do usuário"""
    try:
        return spotify_service.get_saved_albums(limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_followed_artists(limit: int = 20) -> Dict[str, Any]:
    """Obter artistas seguidos pelo usuário"""
    try:
        return spotify_service.get_followed_artists(limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def search_artists(query: str, limit: int = 10) -> Dict[str, Any]:
    """Buscar artistas por nome"""
    try:
        return spotify_service.search_artists(query, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def search_albums(query: str, limit: int = 10) -> Dict[str, Any]:
    """Buscar álbuns por nome"""
    try:
        return spotify_service.search_albums(query, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def search_playlists(query: str, limit: int = 10) -> Dict[str, Any]:
    """Buscar playlists por nome"""
    try:
        return spotify_service.search_playlists(query, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_playlist_tracks(playlist_id: str, limit: int = 50) -> Dict[str, Any]:
    """Obter músicas de uma playlist específica"""
    try:
        return spotify_service.get_playlist_tracks(playlist_id, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_album_tracks(album_id: str) -> Dict[str, Any]:
    """Obter músicas de um álbum específico"""
    try:
        return spotify_service.get_album_tracks(album_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_artist_top_tracks(artist_id: str) -> Dict[str, Any]:
    """Obter músicas mais populares de um artista"""
    try:
        return spotify_service.get_artist_top_tracks(artist_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_artist_albums(artist_id: str, limit: int = 20) -> Dict[str, Any]:
    """Obter álbuns de um artista"""
    try:
        return spotify_service.get_artist_albums(artist_id, limit)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def get_related_artists(artist_id: str) -> Dict[str, Any]:
    """Obter artistas relacionados"""
    try:
        return spotify_service.get_related_artists(artist_id)
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def auto_transfer_playback() -> Dict[str, str]:
    """Transferir playback automaticamente para um dispositivo disponível"""
    try:
        return spotify_service.auto_transfer_playback()
    except Exception as e:
        return {"error": str(e)}


@app.prompt()
def spotify_assistant() -> str:
    """Assistente especializado em controle de música via Spotify.

    Este servidor MCP oferece controle completo do Spotify através de:

    🎵 **Tools de Controle de Reprodução:**
    - play_music: Reproduzir música, playlist ou álbum
    - search_tracks: Buscar músicas por nome
    - search_and_play_all: Buscar e reproduzir todas em sequência
    - search_and_add_to_queue: Buscar e adicionar todas à fila
    - get_current_track: Obter música atual
    - add_to_queue: Adicionar música à fila
    - skip_to_next: Próxima música
    - skip_to_previous: Música anterior
    - set_volume: Definir volume (0-100)
    - seek_to_position: Pular para posição específica
    - toggle_shuffle: Alternar modo shuffle
    - toggle_repeat: Alternar modo repeat
    - get_queue: Fila de reprodução
    - auto_transfer_playback: Transferir playback automaticamente

    📚 **Tools de Busca e Descoberta:**
    - get_recommendations: Recomendações personalizadas
    - search_artists: Buscar artistas
    - search_albums: Buscar álbuns
    - search_playlists: Buscar playlists
    - get_genres: Gêneros musicais
    - get_audio_features: Características de áudio (tempo, dançabilidade, etc.)
    - get_track_tempo: Obter batida (BPM) de uma música
    - get_audio_features_by_uri: Características por URI
    - get_track_tempo_by_uri: Batida por URI

    ❤️ **Tools de Favoritos:**
    - add_track_to_favorites: Adicionar música aos favoritos
    - add_track_to_favorites_by_uri: Adicionar favoritos por URI
    - search_and_add_to_favorites: Buscar e adicionar todas aos favoritos
    - remove_track_from_favorites: Remover dos favoritos
    - remove_track_from_favorites_by_uri: Remover favoritos por URI
    - check_track_in_favorites: Verificar se está nos favoritos
    - check_track_in_favorites_by_uri: Verificar favoritos por URI

    📊 **Tools de Analytics e Gráficos:**
    - get_listening_analytics: Dados analíticos completos para gráficos HTML
    - get_recently_played: Músicas reproduzidas recentemente
    - get_top_tracks: Músicas mais tocadas
    - get_top_artists: Artistas mais ouvidos
    - get_saved_tracks: Músicas salvas
    - get_playlists: Playlists do usuário

    👤 **Tools de Perfil e Dispositivos:**
    - get_user_profile: Perfil do usuário
    - get_devices: Dispositivos disponíveis
    - get_saved_albums: Álbuns salvos
    - get_followed_artists: Artistas seguidos

    🎵 **Tools de Conteúdo:**
    - get_playlists: Playlists do usuário
    - get_playlist_tracks: Músicas de playlist
    - get_album_tracks: Músicas de álbum
    - get_artist_top_tracks: Top músicas do artista
    - get_artist_albums: Álbuns do artista
    - get_related_artists: Artistas relacionados

    🔧 **Tools de Autenticação:**
    - authenticate: Autenticar com Spotify
    - reauthenticate: Reautenticar (útil para novos escopos)
    - check_token_validity: Verificar se o token é válido
    - ensure_valid_token: Garantir token válido (reautentica se necessário)
    - smart_authenticate: Autenticação inteligente (verifica e renova automaticamente)

    📚 **Recursos Disponíveis:**
    - spotify://playback/current: Estado atual de reprodução
    - spotify://playlists: Playlists do usuário
    - spotify://devices: Dispositivos conectados
    - spotify://genres: Gêneros disponíveis
    - spotify://profile: Perfil do usuário
    - spotify://playback/queue: Fila de reprodução
    - spotify://user/top-tracks: Músicas mais tocadas
    - spotify://user/top-artists: Artistas mais ouvidos
    - spotify://user/recently-played: Músicas recentes
    - spotify://user/saved-tracks: Músicas salvas
    - spotify://user/saved-albums: Álbuns salvos
    - spotify://user/followed-artists: Artistas seguidos

    🎯 **Como usar:**
    1. Use as tools de controle para reprodução
    2. Use as tools de busca para encontrar conteúdo
    3. Use as tools de favoritos para gerenciar biblioteca
    4. Use as tools de analytics para visualizar dados
    5. Use as tools de perfil para informações pessoais
    6. Acesse recursos para dados em tempo real

    💡 **Dicas de Uso:**
    - Sempre verifique dispositivos ativos antes de reproduzir
    - Use search_tracks para encontrar músicas específicas
    - Combine get_recommendations com play_music para descobertas
    - Use get_related_artists para explorar novos artistas
    - Use get_audio_features para análises detalhadas de música
    - Use auto_transfer_playback se nenhum dispositivo estiver ativo
    - Use check_track_in_favorites antes de adicionar/remover favoritos
    - Use get_listening_analytics para gerar gráficos HTML

    🎨 **Geração de Gráficos HTML:**
    - Use get_listening_analytics para obter dados
    - Use o prompt 'spotify_analytics_generator' para criar gráficos
    - Gráficos incluem: top artistas, distribuição de gêneros, histórico de reprodução
    - Design responsivo com tema Spotify

    ⚠️ **Notas Importantes:**
    - Características de áudio podem requerer Spotify Premium
    - Favoritos requerem escopo user-library-modify
    - Reautenticação pode ser necessária para novos escopos
    - Gráficos HTML são gerados com Chart.js e CSS responsivo
    """
    return spotify_assistant.__doc__


@app.prompt()
def spotify_usage_guide() -> str:
    """Guia de uso do Spotify MCP Server.

    🚀 **Início Rápido:**
    1. Verifique dispositivos: get_devices
    2. Obtenha música atual: get_current_track
    3. Busque e reproduza: search_tracks + play_music

    🎵 **Fluxos Comuns:**

    **Descoberta de Música:**
    1. get_top_artists → get_artist_top_tracks → play_music
    2. get_recommendations → play_music
    3. get_related_artists → get_artist_albums → play_music

    **Controle de Reprodução:**
    1. get_current_track → skip_to_next/skip_to_previous
    2. set_volume → toggle_shuffle → toggle_repeat
    3. add_to_queue → get_queue
    4. auto_transfer_playback (se nenhum dispositivo ativo)
    5. search_and_play_all → Reproduzir todas as músicas encontradas
    6. search_and_add_to_queue → Adicionar todas à fila

    **Exploração de Conteúdo:**
    1. search_artists → get_artist_albums → get_album_tracks
    2. search_playlists → get_playlist_tracks
    3. get_genres → get_recommendations

    ❤️     **Gerenciamento de Favoritos:**
    1. check_track_in_favorites → add_track_to_favorites
    2. search_tracks → add_track_to_favorites_by_uri
    3. search_and_add_to_favorites → Adicionar todas as músicas encontradas
    4. get_current_track → add_track_to_favorites (música atual)
    5. get_saved_tracks → check_track_in_favorites → remove_track_from_favorites

    📊 **Análise de Dados e Gráficos:**
    1. get_listening_analytics → Usar prompt 'spotify_analytics_generator'
    2. get_audio_features: Características técnicas (tempo, dançabilidade)
    3. get_track_tempo: Obter batida (BPM) específica
    4. get_top_tracks: Histórico de reprodução
    5. get_recently_played: Atividade recente

    🎨 **Geração de Gráficos HTML:**
    1. get_listening_analytics(50) → Obter dados completos
    2. Usar prompt 'spotify_analytics_generator' → Gerar HTML
    3. Resultado: Dashboard interativo com gráficos

    🔧 **Autenticação e Configuração:**
    1. authenticate → Autenticação inicial
    2. reauthenticate → Para novos escopos (favoritos, analytics)
    3. get_user_profile → Verificar status da conta

    ⚡ **Comandos Úteis:**

    **Controle Básico:**
    - Volume: set_volume(50) para 50%
    - Posição: seek_to_position(30000) para 30 segundos
    - Busca: search_tracks("queen") para músicas da Queen
    - Busca e reproduzir todas: search_and_play_all("queen", 10)
    - Busca e adicionar à fila: search_and_add_to_queue("queen", 10)

    **Favoritos:**
    - Verificar: check_track_in_favorites("track_id")
    - Adicionar: add_track_to_favorites("track_id")
    - Busca e adicionar todas: search_and_add_to_favorites("queen", 10)
    - Remover: remove_track_from_favorites("track_id")

    **Analytics:**
    - Dados completos: get_listening_analytics(30)
    - Batida específica: get_track_tempo("track_id")
    - Características: get_audio_features("track_id")

    **Transferência de Playback:**
    - Automática: auto_transfer_playback()
    - Manual: get_devices → play_music com device_id

    📋 **Workflows Avançados:**

    **Dashboard Pessoal:**
    1. get_listening_analytics(50)
    2. get_user_profile
    3. get_current_track
    4. Usar prompt 'spotify_analytics_generator'

    **Descoberta Inteligente:**
    1. get_top_artists → get_related_artists
    2. get_artist_top_tracks → get_audio_features
    3. play_music (baseado em características)

    **Gerenciamento de Biblioteca:**
    1. get_saved_tracks → check_track_in_favorites
    2. search_tracks → add_track_to_favorites
    3. get_playlists → get_playlist_tracks

    **Análise de Tendências:**
    1. get_recently_played(100)
    2. get_top_tracks(50)
    3. get_top_artists(50)
    4. Gerar relatório com gráficos

    💡 **Dicas de Performance:**
    - Use limites apropriados (20-50) para analytics
    - Verifique favoritos antes de adicionar/remover
    - Use auto_transfer_playback para dispositivos inativos
    - Combine dados de múltiplas fontes para análises ricas

    🎯 **Casos de Uso Específicos:**

    **Música Atual:**
    - get_current_track → add_track_to_favorites
    - get_current_track → get_track_tempo

    **Busca e Favoritos:**
    - search_tracks("rock") → add_track_to_favorites_by_uri

    **Análise de Batida:**
    - search_tracks("dance") → get_track_tempo → Filtrar por BPM

    **Relatório Semanal:**
    - get_recently_played(100) → get_listening_analytics → Gráficos
    """
    return spotify_usage_guide.__doc__


@app.prompt()
def spotify_troubleshooting() -> str:
    """Guia de solução de problemas do Spotify MCP.

    🔧 **Problemas Comuns:**

    **Erro: "No active device found"**
    - Solução: get_devices → Verificar se há dispositivos ativos
    - Alternativa: auto_transfer_playback() para transferir automaticamente
    - Abra o Spotify em algum dispositivo antes de usar

    **Erro: "403 Insufficient client scope"**
    - Solução: reauthenticate() para obter novos escopos
    - Escopos necessários: user-library-modify (favoritos), user-read-private
    - Verificar se todos os escopos estão configurados no .env

    **Erro: "Track not found"**
    - Solução: Usar search_tracks para verificar se a música existe
    - Verificar se o track_uri está correto
    - Testar com search_and_play_all para busca mais robusta

    **Erro: "Playback not available"**
    - Solução: Verificar se o Spotify Premium está ativo
    - Verificar se há dispositivos conectados
    - Usar auto_transfer_playback() para ativar dispositivo

    **Erro: "HTTP Error 403" em características de áudio**
    - Solução: Características de áudio podem requerer Spotify Premium
    - Verificar se a conta tem acesso a audio features
    - Usar get_track_tempo como alternativa

    **Erro: "Queue is full" ou "Too many requests"**
    - Solução: Reduzir limite em search_and_add_to_queue (max 10)
    - Aguardar alguns segundos entre operações
    - Usar search_and_play_all com limite menor

    **Erro: "Authentication failed"**
    - Solução: authenticate() para nova autenticação
    - Verificar credenciais no .env
    - Limpar cache de tokens se necessário

    📋 **Checklist de Diagnóstico Completo:**

    **1. Verificação Básica:**
    1. get_devices - Verificar dispositivos disponíveis
    2. get_user_profile - Verificar autenticação
    3. get_current_track - Testar API básica
    4. search_tracks("test") - Testar busca

    **2. Verificação de Funcionalidades:**
    5. search_and_add_to_queue("test", 1) - Testar adição à fila
    6. check_track_in_favorites("test_id") - Testar favoritos
    7. get_listening_analytics(5) - Testar analytics
    8. get_audio_features("test_id") - Testar características

    **3. Verificação de Autenticação:**
    9. authenticate() - Reautenticar se necessário
    10. reauthenticate() - Para novos escopos

    🎯 **Soluções Específicas por Funcionalidade:**

    **Problemas com Reprodução:**
    - get_devices → Verificar dispositivos ativos
    - auto_transfer_playback() → Transferir automaticamente
    - search_and_play_all() → Reprodução mais robusta

    **Problemas com Favoritos:**
    - reauthenticate() → Obter escopo user-library-modify
    - check_track_in_favorites() → Verificar antes de adicionar
    - search_and_add_to_favorites() → Adição em lote mais eficiente

    **Problemas com Analytics:**
    - get_listening_analytics(10) → Começar com limite baixo
    - Verificar conectividade com get_user_profile
    - Usar prompt 'spotify_analytics_generator' para gráficos

    **Problemas com Características de Áudio:**
    - get_track_tempo() → Alternativa mais simples
    - Verificar se conta tem Spotify Premium
    - Usar search_tracks() + get_audio_features() individualmente

    **Problemas com Busca em Lote:**
    - Reduzir limite (max 10 músicas por vez)
    - Usar search_and_add_to_queue() com limite baixo
    - Verificar conectividade antes de operações em lote

    🚀 **Dicas de Performance:**

    **Para Melhor Experiência:**
    - Sempre verificar dispositivos antes de reproduzir
    - Usar auto_transfer_playback() para dispositivos inativos
    - Verificar favoritos antes de adicionar/remover
    - Usar limites apropriados (5-10) para operações em lote
    - Aguardar entre operações múltiplas

    **Para Operações em Lote:**
    - search_and_add_to_queue(query, 5) → Limite baixo
    - search_and_add_to_favorites(query, 3) → Poucas músicas
    - search_and_play_all(query, 5) → Reprodução controlada

    **Para Analytics:**
    - get_listening_analytics(20) → Dados suficientes
    - Usar prompt 'spotify_analytics_generator' para gráficos
    - Combinar dados de múltiplas fontes

    📊 **Monitoramento e Logs:**

    **Logs Úteis:**
    - Sempre verifique os logs do servidor
    - Use get_current_track para testar conectividade
    - Monitore get_queue para verificar estado
    - Verifique get_devices para status de dispositivos

    **Indicadores de Problemas:**
    - Muitos erros 403 → Reautenticação necessária
    - Erros de dispositivo → Verificar Spotify aberto
    - Timeouts → Reduzir limites ou aguardar
    - Erros de busca → Verificar conectividade

    🔄 **Fluxo de Resolução de Problemas:**

    **1. Problema de Conectividade:**
    1. get_user_profile() → Verificar autenticação
    2. get_devices() → Verificar dispositivos
    3. authenticate() → Reautenticar se necessário

    **2. Problema de Reprodução:**
    1. get_current_track() → Testar API básica
    2. auto_transfer_playback() → Ativar dispositivo
    3. search_and_play_all() → Reprodução alternativa

    **3. Problema de Favoritos:**
    1. reauthenticate() → Obter escopo correto
    2. check_track_in_favorites() → Testar funcionalidade
    3. search_and_add_to_favorites() → Adição em lote

    **4. Problema de Analytics:**
    1. get_listening_analytics(5) → Teste simples
    2. Verificar conectividade
    3. Usar prompt 'spotify_analytics_generator'

    ⚠️ **Limitações Conhecidas:**

    - Características de áudio requerem Spotify Premium
    - Operações em lote têm limite de 10 itens
    - Favoritos requerem escopo user-library-modify
    - Analytics podem ser limitados por conta
    - Dispositivos devem estar ativos para reprodução

    💡 **Comandos de Recuperação Rápida:**

    ```python
    # Recuperação básica
    authenticate()
    get_devices()
    auto_transfer_playback()

    # Teste de funcionalidades
    search_and_play_all("test", 1)
    check_track_in_favorites("test_id")
    get_listening_analytics(5)
    ```
    """
    return spotify_troubleshooting.__doc__


@app.prompt()
def spotify_analytics_generator() -> str:
    """Gerador de Gráficos HTML para Análise de Músicas do Spotify.

    📊 **Funcionalidade:**
    Este prompt gera gráficos HTML interativos baseados nos dados de escuta do Spotify.

    🎯 **Tools Disponíveis para Análise:**
    - get_listening_analytics(limit): Obter dados completos de escuta
    - get_recently_played(limit): Músicas reproduzidas recentemente
    - get_top_tracks(limit): Músicas mais tocadas
    - get_top_artists(limit): Artistas mais ouvidos
    - get_saved_tracks(limit): Músicas salvas
    - get_playlists(): Playlists do usuário

    📈 **Tipos de Gráficos Gerados:**

    **1. Gráfico de Barras - Top Artistas:**
    ```html
    <div class="chart-container">
        <h3>🎤 Top Artistas Mais Ouvidos</h3>
        <canvas id="artistsChart"></canvas>
    </div>
    ```

    **2. Gráfico de Pizza - Distribuição de Gêneros:**
    ```html
    <div class="chart-container">
        <h3>🎵 Distribuição por Gênero</h3>
        <canvas id="genresChart"></canvas>
    </div>
    ```

    **3. Gráfico de Linha - Histórico de Reprodução:**
    ```html
    <div class="chart-container">
        <h3>📈 Histórico de Reprodução</h3>
        <canvas id="historyChart"></canvas>
    </div>
    ```

    **4. Tabela Interativa - Top Músicas:**
    ```html
    <div class="table-container">
        <h3>🎵 Top Músicas</h3>
        <table class="music-table">
            <thead>
                <tr><th>Posição</th><th>Música</th><th>Artista</th><th>Popularidade</th></tr>
            </thead>
            <tbody>
                <!-- Dados dinâmicos -->
            </tbody>
        </table>
    </div>
    ```

    **5. Cards de Estatísticas:**
    ```html
    <div class="stats-grid">
        <div class="stat-card">
            <h4>🎵 Total de Músicas</h4>
            <p class="stat-number">{{total_tracks}}</p>
        </div>
        <div class="stat-card">
            <h4>🎤 Artista Favorito</h4>
            <p class="stat-text">{{top_artist}}</p>
        </div>
    </div>
    ```

    🎨 **Estilo CSS Incluído:**
    - Design responsivo e moderno
    - Cores do tema Spotify (verde #1DB954)
    - Animações suaves
    - Gradientes e sombras
    - Tipografia otimizada

    📊 **Bibliotecas JavaScript:**
    - Chart.js para gráficos interativos
    - D3.js para visualizações avançadas
    - Moment.js para formatação de datas

    🔧 **Como Usar:**

    **1. Obter Dados:**
    ```python
    analytics = get_listening_analytics(50)
    ```

    **2. Processar Dados:**
    - Contar frequência de artistas
    - Agrupar por gêneros
    - Calcular estatísticas
    - Formatar datas

    **3. Gerar HTML:**
    - Criar estrutura HTML completa
    - Incluir CSS inline ou externo
    - Adicionar JavaScript para gráficos
    - Inserir dados dinâmicos

    **4. Exemplo de Estrutura:**
    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spotify Analytics Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            /* CSS personalizado */
        </style>
    </head>
    <body>
        <div class="dashboard">
            <!-- Gráficos e estatísticas -->
        </div>
        <script>
            // JavaScript para gráficos
        </script>
    </body>
    </html>
    ```

    📋 **Checklist de Geração:**
    1. ✅ Obter dados com get_listening_analytics()
    2. ✅ Processar e organizar dados
    3. ✅ Criar estrutura HTML
    4. ✅ Adicionar CSS responsivo
    5. ✅ Implementar gráficos com Chart.js
    6. ✅ Adicionar interatividade
    7. ✅ Incluir estatísticas resumidas
    8. ✅ Testar responsividade

    🎯 **Recursos Avançados:**
    - Filtros por período
    - Comparação de períodos
    - Exportação de dados
    - Modo escuro/claro
    - Animações de transição
    - Tooltips informativos

    💡 **Dicas de Design:**
    - Use cores consistentes com a marca Spotify
    - Mantenha hierarquia visual clara
    - Adicione micro-interações
    - Otimize para mobile
    - Inclua loading states

    📱 **Responsividade:**
    - Breakpoints para mobile, tablet e desktop
    - Gráficos adaptáveis
    - Navegação touch-friendly
    - Texto legível em todas as telas
    """
    return spotify_analytics_generator.__doc__


@app.resource("spotify://playback/current")
def current_playback() -> Dict[str, Any]:
    """Recurso: Estado atual de reprodução do Spotify"""
    try:
        return {
            "name": "Reprodução Atual",
            "description": "Estado atual de reprodução do Spotify",
            "mimeType": "application/json",
            "data": spotify_service.get_current_track(),
        }
    except Exception as e:
        return {
            "name": "Reprodução Atual",
            "description": "Estado atual de reprodução do Spotify",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://playlists/user")
def user_playlists() -> Dict[str, Any]:
    """Recurso: Playlists do usuário"""
    try:
        return {
            "name": "Minhas Playlists",
            "description": "Playlists do usuário no Spotify",
            "mimeType": "application/json",
            "data": spotify_service.get_playlists(),
        }
    except Exception as e:
        return {
            "name": "Minhas Playlists",
            "description": "Playlists do usuário no Spotify",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://devices/available")
def available_devices() -> Dict[str, Any]:
    """Recurso: Dispositivos disponíveis"""
    try:
        return {
            "name": "Dispositivos Disponíveis",
            "description": "Dispositivos disponíveis para reprodução",
            "mimeType": "application/json",
            "data": spotify_service.get_devices(),
        }
    except Exception as e:
        return {
            "name": "Dispositivos Disponíveis",
            "description": "Dispositivos disponíveis para reprodução",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://genres/available")
def music_genres() -> Dict[str, Any]:
    """Recurso: Gêneros musicais disponíveis"""
    try:
        return {
            "name": "Gêneros Musicais",
            "description": "Gêneros musicais disponíveis para recomendações",
            "mimeType": "application/json",
            "data": spotify_service.get_genres(),
        }
    except Exception as e:
        return {
            "name": "Gêneros Musicais",
            "description": "Gêneros musicais disponíveis para recomendações",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://user/profile")
def user_profile() -> Dict[str, Any]:
    """Recurso: Perfil do usuário"""
    try:
        return {
            "name": "Perfil do Usuário",
            "description": "Informações do perfil do usuário no Spotify",
            "mimeType": "application/json",
            "data": spotify_service.get_user_profile(),
        }
    except Exception as e:
        return {
            "name": "Perfil do Usuário",
            "description": "Informações do perfil do usuário no Spotify",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://playback/queue")
def playback_queue() -> Dict[str, Any]:
    """Recurso: Fila de reprodução atual"""
    try:
        return {
            "name": "Fila de Reprodução",
            "description": "Fila de reprodução atual do Spotify",
            "mimeType": "application/json",
            "data": spotify_service.get_queue(),
        }
    except Exception as e:
        return {
            "name": "Fila de Reprodução",
            "description": "Fila de reprodução atual do Spotify",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://user/top-tracks")
def user_top_tracks() -> Dict[str, Any]:
    """Recurso: Músicas mais tocadas do usuário"""
    try:
        return {
            "name": "Minhas Músicas Mais Tocadas",
            "description": "Músicas mais reproduzidas pelo usuário",
            "mimeType": "application/json",
            "data": spotify_service.get_top_tracks(20, "medium_term"),
        }
    except Exception as e:
        return {
            "name": "Minhas Músicas Mais Tocadas",
            "description": "Músicas mais reproduzidas pelo usuário",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://user/top-artists")
def user_top_artists() -> Dict[str, Any]:
    """Recurso: Artistas mais ouvidos do usuário"""
    try:
        return {
            "name": "Meus Artistas Mais Ouvidos",
            "description": "Artistas mais reproduzidos pelo usuário",
            "mimeType": "application/json",
            "data": spotify_service.get_top_artists(20, "medium_term"),
        }
    except Exception as e:
        return {
            "name": "Meus Artistas Mais Ouvidos",
            "description": "Artistas mais reproduzidos pelo usuário",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://user/recently-played")
def user_recently_played() -> Dict[str, Any]:
    """Recurso: Músicas reproduzidas recentemente"""
    try:
        return {
            "name": "Músicas Reproduzidas Recentemente",
            "description": "Histórico de reprodução recente do usuário",
            "mimeType": "application/json",
            "data": spotify_service.get_recently_played(20),
        }
    except Exception as e:
        return {
            "name": "Músicas Reproduzidas Recentemente",
            "description": "Histórico de reprodução recente do usuário",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://user/saved-tracks")
def user_saved_tracks() -> Dict[str, Any]:
    """Recurso: Músicas salvas do usuário"""
    try:
        return {
            "name": "Minhas Músicas Salvas",
            "description": "Músicas salvas na biblioteca do usuário",
            "mimeType": "application/json",
            "data": spotify_service.get_saved_tracks(20),
        }
    except Exception as e:
        return {
            "name": "Minhas Músicas Salvas",
            "description": "Músicas salvas na biblioteca do usuário",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://user/saved-albums")
def user_saved_albums() -> Dict[str, Any]:
    """Recurso: Álbuns salvos do usuário"""
    try:
        return {
            "name": "Meus Álbuns Salvos",
            "description": "Álbuns salvos na biblioteca do usuário",
            "mimeType": "application/json",
            "data": spotify_service.get_saved_albums(20),
        }
    except Exception as e:
        return {
            "name": "Meus Álbuns Salvos",
            "description": "Álbuns salvos na biblioteca do usuário",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


@app.resource("spotify://user/followed-artists")
def user_followed_artists() -> Dict[str, Any]:
    """Recurso: Artistas seguidos pelo usuário"""
    try:
        return {
            "name": "Artistas que eu Sigo",
            "description": "Artistas seguidos pelo usuário no Spotify",
            "mimeType": "application/json",
            "data": spotify_service.get_followed_artists(20),
        }
    except Exception as e:
        return {
            "name": "Artistas que eu Sigo",
            "description": "Artistas seguidos pelo usuário no Spotify",
            "mimeType": "application/json",
            "data": {"error": str(e)},
        }


# Nota: FastMCP não suporta templates de recursos dinâmicos
# Os recursos estáticos já estão definidos acima


if __name__ == "__main__":
    logger.info(f"🚀 Iniciando {MCP_SERVER_NAME} v{MCP_SERVER_VERSION}")
    logger.info("📡 Servidor MCP rodando com FastMCP")

    app.run()
