#!/usr/bin/env python3
"""
Service layer para integração com Spotify
"""

import logging
import sys
import io
import os
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler

try:
    from .config import (
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        SPOTIFY_REDIRECT_URI,
        SPOTIFY_SCOPES,
    )
except ImportError:
    from config import (
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        SPOTIFY_REDIRECT_URI,
        SPOTIFY_SCOPES,
    )

# Configurar logging
logger = logging.getLogger(__name__)

# Autenticação simplificada: sem decorators, sempre via navegador (open_browser=True)


class SpotifyService:
    """Serviço para integração com Spotify"""
    
    def __init__(self):
        self.client: Optional[spotipy.Spotify] = None
        # Tentar inicializar o cliente se houver cache válido
        # self._try_initialize_from_cache()
        self._initialize_client()

    def _extract_track_id(self, track_or_uri: str) -> str:
        """Extrai o track_id a partir de um ID, URI ou URL do Spotify.

        Aceita formatos:
        - "spotify:track:ID"
        - "https://open.spotify.com/track/ID?si=..."
        - "ID" (já o próprio track id)
        """
        if not track_or_uri:
            return track_or_uri

        if track_or_uri.startswith("spotify:track:"):
            return track_or_uri.split(":")[-1]

        if "open.spotify.com/track/" in track_or_uri:
            try:
                parsed = urlparse(track_or_uri)
                parts = [p for p in parsed.path.split("/") if p]
                if len(parts) >= 2 and parts[0] == "track":
                    return parts[1]
            except Exception:
                # Silenciar parsing falho e retornar original
                return track_or_uri

        return track_or_uri

    def _create_auth_manager(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ) -> SpotifyOAuth:
        # Usar caminho absoluto do cache, evitando depender do CWD
        try:
            from .config import TOKEN_CACHE_PATH
        except ImportError:
            from config import TOKEN_CACHE_PATH
        cache_handler = CacheFileHandler(cache_path=TOKEN_CACHE_PATH)
        return SpotifyOAuth(
            client_id=client_id or SPOTIFY_CLIENT_ID,
            client_secret=client_secret or SPOTIFY_CLIENT_SECRET,
            redirect_uri=redirect_uri or SPOTIFY_REDIRECT_URI,
            scope=",".join(SPOTIFY_SCOPES),
            cache_handler=cache_handler,
            open_browser=True,
        ), cache_handler

    def _try_initialize_from_cache(self) -> None:
        """Tenta inicializar o cliente usando cache existente"""
        try:
            if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
                logger.warning("SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET não configurados")
                self.client = None
                return
            
            auth_manager, cache_handler = self._create_auth_manager()
            
            # Verificar se há cache válido
            token_info = cache_handler.get_cached_token()
            if token_info and not auth_manager.is_token_expired(token_info):
                # Cache válido, inicializar cliente
                self.client = spotipy.Spotify(auth_manager=auth_manager)
                logger.info("Cliente Spotipy inicializado com cache válido")
            else:
                logger.info("Cache inválido ou inexistente, cliente não inicializado automaticamente")
                self.client = None
                
        except Exception as e:
            logger.error(f"❌ Erro ao tentar inicializar com cache: {e}")
            self.client = None

    def _initialize_client(self) -> None:
        """Inicializa o cliente Spotipy (método completo com autenticação)"""
        try:
            if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
                logger.warning("SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET não configurados")
                self.client = None
                return
            
            auth_manager, cache_handler = self._create_auth_manager()
            
            token_info = cache_handler.get_cached_token()
            if not token_info or auth_manager.is_token_expired(token_info):
                # Dispara fluxo via navegador; se usuário concluir, segue
                try:
                    auth_manager.get_access_token(as_dict=False)
                except Exception as auth_error:
                    logger.warning(f"Autenticação necessária: {auth_error}")
            self.client = spotipy.Spotify(auth_manager=auth_manager)
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Spotipy: {e}")
            self.client = None
    
    def is_connected(self) -> bool:
        """Verifica se o cliente está conectado"""
        return self.client is not None
    
    def authenticate(self, client_id: str, client_secret: str, redirect_uri: Optional[str] = None) -> Dict[str, str]:
        """Autenticar com Spotify"""
        try:
            auth_manager, _ = self._create_auth_manager(client_id, client_secret, redirect_uri)
            auth_manager.get_access_token(as_dict=False)
            self.client = spotipy.Spotify(auth_manager=auth_manager)
            return {"message": "Autenticação realizada com sucesso"}
        except Exception as e:
            raise ValueError(f"Erro na autenticação: {str(e)}")
    
    def reauthenticate(self) -> Dict[str, str]:
        """Reautenticar com credenciais configuradas"""
        try:
            if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
                raise ValueError("SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET devem estar configurados")
            
            auth_manager, _ = self._create_auth_manager()
            auth_manager.get_access_token(as_dict=False)
            self.client = spotipy.Spotify(auth_manager=auth_manager)
            return {"message": "Reautenticação realizada com sucesso"}
        except Exception as e:
            raise ValueError(f"Erro na reautenticação: {str(e)}")
    
    def check_token_validity(self) -> Dict[str, Any]:
        """Verificar se o token atual é válido"""
        if not self.client:
            return {
                "valid": False,
                "message": "Cliente Spotipy não inicializado",
                "needs_auth": True
            }
        
        try:
            # Tentar fazer uma chamada simples para verificar o token
            self.client.current_user()
            
            return {
                "valid": True,
                "message": "Token válido e funcionando",
                "needs_auth": False
            }
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if "401" in error_msg or "unauthorized" in error_msg:
                return {
                    "valid": False,
                    "message": "Token expirado ou inválido",
                    "needs_auth": True,
                    "error": str(e)
                }
            elif "403" in error_msg or "forbidden" in error_msg:
                return {
                    "valid": False,
                    "message": "Token sem permissões suficientes",
                    "needs_auth": True,
                    "error": str(e)
                }
            else:
                return {
                    "valid": False,
                    "message": f"Erro ao verificar token: {str(e)}",
                    "needs_auth": True,
                    "error": str(e)
                }
    
    def ensure_valid_token(self) -> Dict[str, Any]:
        """Garantir que o token é válido, reautenticando se necessário"""
        try:
            # Verificar se o token atual é válido
            token_check = self.check_token_validity()
            
            if token_check["valid"]:
                return {
                    "success": True,
                    "message": "Token já é válido",
                    "action": "none"
                }
            
            # Token não é válido, tentar reautenticar
            logger.info("Token inválido detectado. Iniciando reautenticação...")
            
            # Limpar cache se existir
            # Remover cache usando caminho absoluto
            try:
                from .config import TOKEN_CACHE_PATH
            except ImportError:
                from config import TOKEN_CACHE_PATH
            cache_file = TOKEN_CACHE_PATH
            if os.path.exists(cache_file):
                try:
                    os.remove(cache_file)
                    logger.info("Cache de token removido")
                except Exception as e:
                    logger.warning(f"Erro ao remover cache: {e}")
            
            # Reautenticar
            try:
                reauth_result = self.reauthenticate()
                logger.info(f"Reautenticação bem-sucedida: {reauth_result}")
            except Exception as reauth_error:
                return {
                    "success": False,
                    "message": "Falha na reautenticação",
                    "action": "reauth_failed",
                    "error": str(reauth_error)
                }
            
            # Verificar se a reautenticação funcionou
            new_token_check = self.check_token_validity()
            
            if new_token_check["valid"]:
                return {
                    "success": True,
                    "message": "Reautenticação bem-sucedida",
                    "action": "reauth_success"
                }
            else:
                return {
                    "success": False,
                    "message": "Reautenticação falhou",
                    "action": "reauth_failed",
                    "error": new_token_check["error"]
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao verificar/renovar token: {str(e)}",
                "action": "error",
                "error": str(e)
            }
    
    def smart_authenticate(self) -> Dict[str, Any]:
        """Autenticação inteligente: verifica token e reautentica se necessário"""
        try:
            # Primeiro, tentar inicializar o cliente
            if not self.client:
                logger.info("Cliente não inicializado. Iniciando autenticação...")
                self._initialize_client()
                
                if not self.client:
                    return {
                        "success": False,
                        "message": "Falha ao inicializar cliente",
                        "action": "init_failed"
                    }
            
            # Verificar se o token é válido
            token_check = self.check_token_validity()
            
            if token_check["valid"]:
                return {
                    "success": True,
                    "message": "Token válido, cliente pronto para uso",
                    "action": "token_valid"
                }
            
            # Token não é válido, garantir token válido
            logger.info("Token inválido detectado. Iniciando renovação...")
            return self.ensure_valid_token()
            
        except Exception as e:
            logger.error(f"Erro na autenticação inteligente: {e}")
            return {
                "success": False,
                "message": f"Erro na autenticação inteligente: {str(e)}",
                "action": "error",
                "error": str(e)
            }
    
    def get_current_track(self) -> Dict[str, Any]:
        """Obter música atual"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            current = self.client.current_user_playing_track()
            if current:
                return {
                    "is_playing": current["is_playing"],
                    "track": {
                        "name": current["item"]["name"],
                        "artist": current["item"]["artists"][0]["name"],
                        "album": current["item"]["album"]["name"],
                        "uri": current["item"]["uri"],
                        "duration_ms": current["item"]["duration_ms"],
                        "progress_ms": current["progress_ms"]
                    }
                }
            return {"message": "Nenhuma música tocando"}
        except Exception as e:
            raise ValueError(f"Erro ao obter música atual: {str(e)}")
    
    def play_music(self, track_uri: Optional[str] = None, playlist_uri: Optional[str] = None, album_uri: Optional[str] = None) -> Dict[str, str]:
        """Tocar música"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            # Verificar se há dispositivos ativos
            devices = self.client.devices()
            active_devices = [d for d in devices["devices"] if d["is_active"]]
            
            if not active_devices:
                # Se não há dispositivos ativos, tentar transferir para o primeiro disponível
                available_devices = [d for d in devices["devices"] if d["type"] in ["Computer", "Smartphone", "Tablet"]]
                if available_devices:
                    # Transferir para o primeiro dispositivo disponível
                    device_id = available_devices[0]["id"]
                    self.client.transfer_playback(device_id=device_id)
                    logger.info(f"Playback transferido para: {available_devices[0]['name']}")
                else:
                    raise ValueError("Nenhum dispositivo disponível para reprodução")
            
            # Agora tentar tocar a música
            if track_uri:
                self.client.start_playback(uris=[track_uri])
            elif playlist_uri:
                self.client.start_playback(context_uri=playlist_uri)
            elif album_uri:
                self.client.start_playback(context_uri=album_uri)
            else:
                self.client.start_playback()
            
            return {"message": "Música iniciada"}
        except Exception as e:
            raise ValueError(f"Erro ao tocar música: {str(e)}")
    
    def pause_music(self) -> Dict[str, str]:
        """Pausar música"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.pause_playback()
            return {"message": "Música pausada"}
        except Exception as e:
            raise ValueError(f"Erro ao pausar música: {str(e)}")
    
    def next_track(self) -> Dict[str, str]:
        """Próxima música"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.next_track()
            return {"message": "Próxima música"}
        except Exception as e:
            raise ValueError(f"Erro ao avançar música: {str(e)}")
    
    def previous_track(self) -> Dict[str, str]:
        """Música anterior"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.previous_track()
            return {"message": "Música anterior"}
        except Exception as e:
            raise ValueError(f"Erro ao voltar música: {str(e)}")
    
    def skip_to_next(self) -> Dict[str, str]:
        """Pular para próxima música"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.next_track()
            return {"message": "Pulou para próxima música"}
        except Exception as e:
            error_msg = str(e).lower()
            if "restriction violated" in error_msg or "403" in error_msg:
                return {"message": "Não é possível pular para próxima música neste momento", "warning": "Restrição do Spotify"}
            else:
                raise ValueError(f"Erro ao pular para próxima música: {str(e)}")
    
    def skip_to_previous(self) -> Dict[str, str]:
        """Pular para música anterior"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.previous_track()
            return {"message": "Pulou para música anterior"}
        except Exception as e:
            error_msg = str(e).lower()
            if "restriction violated" in error_msg or "403" in error_msg:
                return {"message": "Não é possível voltar para música anterior neste momento", "warning": "Restrição do Spotify"}
            else:
                raise ValueError(f"Erro ao pular para música anterior: {str(e)}")
    
    def set_volume(self, volume: int) -> Dict[str, str]:
        """Ajustar volume (0-100)"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        if not 0 <= volume <= 100:
            raise ValueError("Volume deve estar entre 0 e 100")
        
        try:
            self.client.volume(volume)
            return {"message": f"Volume ajustado para {volume}%"}
        except Exception as e:
            raise ValueError(f"Erro ao ajustar volume: {str(e)}")
    
    def search_tracks(self, query: str, limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Buscar músicas"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            results = self.client.search(q=query, type="track", limit=limit)
            tracks = []
            for track in results["tracks"]["items"]:
                tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"]
                })
            return {"tracks": tracks}
        except Exception as e:
            raise ValueError(f"Erro na busca: {str(e)}")
    
    def get_playlists(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obter playlists do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            playlists = self.client.current_user_playlists()
            return {"playlists": playlists["items"]}
        except Exception as e:
            raise ValueError(f"Erro ao obter playlists: {str(e)}")
    
    def get_playlist_tracks(self, playlist_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Obter músicas de uma playlist específica"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            playlist = self.client.playlist_tracks(playlist_id)
            tracks = []
            for item in playlist["items"]:
                track = item["track"]
                if track:
                    tracks.append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"],
                        "album": track["album"]["name"],
                        "uri": track["uri"],
                        "duration_ms": track["duration_ms"]
                    })
            return {"tracks": tracks}
        except Exception as e:
            raise ValueError(f"Erro ao obter músicas da playlist: {str(e)}")
    
    def get_user_albums(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obter álbuns salvos do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            albums = self.client.current_user_saved_albums()
            return {"albums": albums["items"]}
        except Exception as e:
            raise ValueError(f"Erro ao obter álbuns: {str(e)}")
    
    def get_saved_tracks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obter músicas salvas do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            tracks = self.client.current_user_saved_tracks()
            saved_tracks = []
            for item in tracks["items"]:
                track = item["track"]
                saved_tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"]
                })
            return {"tracks": saved_tracks}
        except Exception as e:
            raise ValueError(f"Erro ao obter músicas salvas: {str(e)}")
    
    def get_top_artists(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obter artistas favoritos do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            artists = self.client.current_user_top_artists()
            return {"artists": artists["items"]}
        except Exception as e:
            if "403" in str(e) or "Insufficient client scope" in str(e):
                raise ValueError("Permissão insuficiente. Reautentique com escopo 'user-top-read'")
            raise ValueError(f"Erro ao obter artistas: {str(e)}")
    
    def get_top_tracks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obter músicas mais tocadas do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            tracks = self.client.current_user_top_tracks()
            top_tracks = []
            for track in tracks["items"]:
                top_tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"]
                })
            return {"tracks": top_tracks}
        except Exception as e:
            if "403" in str(e) or "Insufficient client scope" in str(e):
                raise ValueError("Permissão insuficiente. Reautentique com escopo 'user-top-read'")
            raise ValueError(f"Erro ao obter top tracks: {str(e)}")
    
    def get_devices(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obter dispositivos disponíveis"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            devices = self.client.devices()
            return {"devices": devices["devices"]}
        except Exception as e:
            raise ValueError(f"Erro ao obter dispositivos: {str(e)}")
    
    def transfer_playback(self, device_id: str) -> Dict[str, str]:
        """Transferir playback para outro dispositivo"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.transfer_playback(device_id=device_id)
            return {"message": f"Playback transferido para dispositivo {device_id}"}
        except Exception as e:
            raise ValueError(f"Erro ao transferir playback: {str(e)}")
    
    def auto_transfer_playback(self) -> Dict[str, str]:
        """Transferir playback automaticamente para um dispositivo disponível"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            devices = self.client.devices()
            available_devices = [d for d in devices["devices"] if d["type"] in ["Computer", "Smartphone", "Tablet"]]
            
            if not available_devices:
                raise ValueError("Nenhum dispositivo disponível para reprodução")
            
            # Transferir para o primeiro dispositivo disponível
            device_id = available_devices[0]["id"]
            device_name = available_devices[0]["name"]
            
            self.client.transfer_playback(device_id=device_id)
            return {"message": f"Playback transferido automaticamente para: {device_name}"}
        except Exception as e:
            raise ValueError(f"Erro ao transferir playback automaticamente: {str(e)}")
    
    def toggle_shuffle(self) -> Dict[str, str]:
        """Alternar modo shuffle"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            current_state = self.client.current_playback()
            if current_state:
                new_state = not current_state["shuffle_state"]
                self.client.shuffle(new_state)
                return {"message": f"Shuffle {'ativado' if new_state else 'desativado'}"}
            return {"message": "Nenhuma música tocando"}
        except Exception as e:
            raise ValueError(f"Erro ao alternar shuffle: {str(e)}")
    
    def toggle_repeat(self) -> Dict[str, str]:
        """Alternar modo repeat"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            current_state = self.client.current_playback()
            if current_state:
                current_repeat = current_state["repeat_state"]
                if current_repeat == "off":
                    new_repeat = "track"
                elif current_repeat == "track":
                    new_repeat = "context"
                else:
                    new_repeat = "off"
                
                self.client.repeat(new_repeat)
                return {"message": f"Repeat: {new_repeat}"}
            return {"message": "Nenhuma música tocando"}
        except Exception as e:
            raise ValueError(f"Erro ao alternar repeat: {str(e)}")
    
    def seek_to_position(self, position_ms: int) -> Dict[str, str]:
        """Pular para posição específica na música (em milissegundos)"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        if position_ms < 0:
            raise ValueError("Posição deve ser maior ou igual a 0")
        
        try:
            self.client.seek_track(position_ms)
            return {"message": f"Pulado para {position_ms}ms"}
        except Exception as e:
            raise ValueError(f"Erro ao pular posição: {str(e)}")
    
    def get_queue(self) -> Dict[str, Any]:
        """Obter fila de reprodução atual"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            queue = self.client.queue()
            return {"queue": queue}
        except Exception as e:
            raise ValueError(f"Erro ao obter fila: {str(e)}")
    
    def add_to_queue(self, track_uri: str) -> Dict[str, str]:
        """Adicionar música à fila de reprodução"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.add_to_queue(track_uri)
            return {"message": "Música adicionada à fila"}
        except Exception as e:
            raise ValueError(f"Erro ao adicionar à fila: {str(e)}")
    
    def get_recommendations(self, seed_artists: Optional[str] = None, seed_tracks: Optional[str] = None, 
                          seed_genres: Optional[str] = None, limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """Obter recomendações baseadas em artistas, músicas ou gêneros"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            seeds = {}
            if seed_artists:
                artists = seed_artists.split(",")[:5]
                seeds["seed_artists"] = artists
            if seed_tracks:
                tracks = seed_tracks.split(",")[:5]
                seeds["seed_tracks"] = tracks
            if seed_genres:
                genres = seed_genres.split(",")[:5]
                seeds["seed_genres"] = genres
            
            if not seeds:
                raise ValueError("Pelo menos um seed deve ser fornecido")
            
            # Verificar se o total de seeds não excede 5 (limite da API)
            total_seeds = sum(len(seed_list) for seed_list in seeds.values())
            if total_seeds > 5:
                raise ValueError("Máximo de 5 seeds permitido no total")
            
            recommendations = self.client.recommendations(**seeds, limit=limit)
            tracks = []
            for track in recommendations["tracks"]:
                tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"]
                })
            return {"tracks": tracks}
        except Exception as e:
            if "403" in str(e) or "Insufficient client scope" in str(e):
                raise ValueError("Permissão insuficiente. Reautentique com o endpoint /auth/reauth")
            elif "404" in str(e):
                raise ValueError("API de recomendações temporariamente indisponível. Tente novamente mais tarde.")
            raise ValueError(f"Erro interno: {str(e)}")
    
    def get_genres(self) -> Dict[str, List[str]]:
        """Obter gêneros musicais disponíveis"""
        # Lista de gêneros musicais comuns do Spotify
        common_genres = [
            "acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", 
            "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", 
            "chicago-house", "children", "chill", "classical", "club", "comedy", "country", 
            "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", 
            "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", 
            "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", 
            "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", 
            "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", 
            "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", 
            "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", 
            "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", 
            "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop", 
            "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", 
            "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", 
            "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", 
            "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", 
            "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", 
            "trip-hop", "turkish", "work-out", "world-music"
        ]
        return {"genres": common_genres}
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Obter perfil do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            user = self.client.current_user()
            return {"user": user}
        except Exception as e:
            raise ValueError(f"Erro ao obter perfil: {str(e)}")
    
    def get_audio_features(self, track_id: str) -> Dict[str, Any]:
        """Obter características de áudio de uma música
        
        Nota: Este endpoint pode requerer Spotify Premium ou ter limitações específicas.
        Se retornar erro 403, as características de áudio podem não estar disponíveis para sua conta.
        """
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            features = self.client.audio_features(track_id)
            if not features or not features[0]:
                return {"features": None, "message": "Características de áudio não disponíveis"}
            
            feature = features[0]
            return {
                "features": {
                    "tempo": feature.get("tempo"),  # Batida (BPM)
                    "danceability": feature.get("danceability"),  # Dançabilidade (0-1)
                    "energy": feature.get("energy"),  # Energia (0-1)
                    "valence": feature.get("valence"),  # Positividade (0-1)
                    "acousticness": feature.get("acousticness"),  # Acústica (0-1)
                    "instrumentalness": feature.get("instrumentalness"),  # Instrumental (0-1)
                    "liveness": feature.get("liveness"),  # Ao vivo (0-1)
                    "speechiness": feature.get("speechiness"),  # Fala (0-1)
                    "key": feature.get("key"),  # Tom musical
                    "mode": feature.get("mode"),  # Modo (maior/menor)
                    "time_signature": feature.get("time_signature"),  # Compasso
                    "duration_ms": feature.get("duration_ms"),  # Duração em ms
                    "loudness": feature.get("loudness"),  # Volume (dB)
                },
                "track_id": track_id
            }
        except Exception as e:
            error_text = str(e)
            if "403" in error_text or "forbidden" in error_text.lower():
                return {
                    "features": None,
                    "message": "Características de áudio não disponíveis (erro 403). Pode requerer Spotify Premium.",
                    "error": {"status": 403, "type": "forbidden"}
                }
            raise ValueError(f"Erro ao obter características de áudio: {error_text}")
    
    def get_track_tempo(self, track_id: str) -> Dict[str, Any]:
        """Obter especificamente a batida (tempo) de uma música
        
        Nota: Este endpoint pode requerer Spotify Premium ou ter limitações específicas.
        Se retornar erro 403, o tempo pode não estar disponível para sua conta.
        """
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            features = self.client.audio_features(track_id)
            if not features or not features[0]:
                return {"tempo": None, "message": "Tempo não disponível"}
            
            tempo = features[0].get("tempo")
            return {
                "tempo": tempo,
                "bpm": tempo,  # BPM (Beats Per Minute)
                "track_id": track_id,
                "description": f"Batida: {tempo} BPM" if tempo else "Tempo não disponível"
            }
        except Exception as e:
            error_text = str(e)
            if "403" in error_text or "forbidden" in error_text.lower():
                return {
                    "tempo": None,
                    "message": "Tempo não disponível (erro 403). Pode requerer Spotify Premium.",
                    "error": {"status": 403, "type": "forbidden"}
                }
            raise ValueError(f"Erro ao obter tempo: {error_text}")
    
    def get_audio_features_by_uri(self, track_uri: str) -> Dict[str, Any]:
        """Obter características de áudio usando URI da música"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            track_id = self._extract_track_id(track_uri)
            
            return self.get_audio_features(track_id)
        except Exception as e:
            raise ValueError(f"Erro ao obter características de áudio por URI: {str(e)}")
    
    def get_track_tempo_by_uri(self, track_uri: str) -> Dict[str, Any]:
        """Obter batida (tempo) usando URI da música"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            track_id = self._extract_track_id(track_uri)
            
            return self.get_track_tempo(track_id)
        except Exception as e:
            raise ValueError(f"Erro ao obter tempo por URI: {str(e)}")
    
    def add_track_to_favorites(self, track_id: str) -> Dict[str, str]:
        """Adicionar música aos favoritos (liked songs)"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.current_user_saved_tracks_add(tracks=[track_id])
            return {"message": f"Música adicionada aos favoritos com sucesso"}
        except Exception as e:
            raise ValueError(f"Erro ao adicionar aos favoritos: {str(e)}")
    
    def remove_track_from_favorites(self, track_id: str) -> Dict[str, str]:
        """Remover música dos favoritos (liked songs)"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            self.client.current_user_saved_tracks_delete(tracks=[track_id])
            return {"message": f"Música removida dos favoritos com sucesso"}
        except Exception as e:
            raise ValueError(f"Erro ao remover dos favoritos: {str(e)}")
    
    def add_track_to_favorites_by_uri(self, track_uri: str) -> Dict[str, str]:
        """Adicionar música aos favoritos usando URI"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            track_id = self._extract_track_id(track_uri)
            
            return self.add_track_to_favorites(track_id)
        except Exception as e:
            raise ValueError(f"Erro ao adicionar aos favoritos por URI: {str(e)}")
    
    def remove_track_from_favorites_by_uri(self, track_uri: str) -> Dict[str, str]:
        """Remover música dos favoritos usando URI"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            track_id = self._extract_track_id(track_uri)
            
            return self.remove_track_from_favorites(track_id)
        except Exception as e:
            raise ValueError(f"Erro ao remover dos favoritos por URI: {str(e)}")
    
    def check_track_in_favorites(self, track_id: str) -> Dict[str, Any]:
        """Verificar se uma música está nos favoritos"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            result = self.client.current_user_saved_tracks_contains(tracks=[track_id])
            is_saved = result[0] if result else False
            
            return {
                "is_saved": is_saved,
                "track_id": track_id,
                "message": f"Música {'está' if is_saved else 'não está'} nos favoritos"
            }
        except Exception as e:
            raise ValueError(f"Erro ao verificar favoritos: {str(e)}")
    
    def check_track_in_favorites_by_uri(self, track_uri: str) -> Dict[str, Any]:
        """Verificar se uma música está nos favoritos usando URI"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            track_id = self._extract_track_id(track_uri)
            
            return self.check_track_in_favorites(track_id)
        except Exception as e:
            raise ValueError(f"Erro ao verificar favoritos por URI: {str(e)}")
    
    def get_listening_analytics(self, limit: int = 50) -> Dict[str, Any]:
        """Obter dados analíticos de escuta para gerar gráficos"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            analytics = {
                "recently_played": [],
                "top_tracks": [],
                "top_artists": [],
                "saved_tracks": [],
                "playlists": [],
                "summary": {}
            }
            
            # Músicas reproduzidas recentemente
            try:
                recent = self.client.current_user_recently_played(limit=limit)
                for item in recent["items"]:
                    track = item["track"]
                    analytics["recently_played"].append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"],
                        "album": track["album"]["name"],
                        "played_at": item["played_at"],
                        "uri": track["uri"],
                        "duration_ms": track["duration_ms"]
                    })
            except Exception as e:
                logger.warning(f"Erro ao obter músicas recentes: {e}")
            
            # Top músicas
            try:
                top_tracks = self.client.current_user_top_tracks(limit=limit)
                for track in top_tracks["items"]:
                    analytics["top_tracks"].append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"],
                        "album": track["album"]["name"],
                        "uri": track["uri"],
                        "duration_ms": track["duration_ms"],
                        "popularity": track["popularity"]
                    })
            except Exception as e:
                logger.warning(f"Erro ao obter top tracks: {e}")
            
            # Top artistas
            try:
                top_artists = self.client.current_user_top_artists(limit=limit)
                for artist in top_artists["items"]:
                    analytics["top_artists"].append({
                        "name": artist["name"],
                        "uri": artist["uri"],
                        "genres": artist["genres"],
                        "popularity": artist["popularity"]
                    })
            except Exception as e:
                logger.warning(f"Erro ao obter top artists: {e}")
            
            # Músicas salvas
            try:
                saved = self.client.current_user_saved_tracks(limit=limit)
                for item in saved["items"]:
                    track = item["track"]
                    analytics["saved_tracks"].append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"],
                        "album": track["album"]["name"],
                        "uri": track["uri"],
                        "duration_ms": track["duration_ms"]
                    })
            except Exception as e:
                logger.warning(f"Erro ao obter músicas salvas: {e}")
            
            # Playlists
            try:
                playlists = self.client.current_user_playlists(limit=limit)
                for playlist in playlists["items"]:
                    analytics["playlists"].append({
                        "name": playlist["name"],
                        "uri": playlist["uri"],
                        "tracks_total": playlist["tracks"]["total"],
                        "owner": playlist["owner"]["display_name"]
                    })
            except Exception as e:
                logger.warning(f"Erro ao obter playlists: {e}")
            
            # Resumo estatístico
            analytics["summary"] = {
                "total_recently_played": len(analytics["recently_played"]),
                "total_top_tracks": len(analytics["top_tracks"]),
                "total_top_artists": len(analytics["top_artists"]),
                "total_saved_tracks": len(analytics["saved_tracks"]),
                "total_playlists": len(analytics["playlists"]),
                "most_played_artist": self._get_most_played_artist(analytics["recently_played"]),
                "most_played_track": self._get_most_played_track(analytics["recently_played"])
            }
            
            return analytics
            
        except Exception as e:
            raise ValueError(f"Erro ao obter dados analíticos: {str(e)}")
    
    def _get_most_played_artist(self, tracks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Obter artista mais reproduzido"""
        artist_counts = {}
        for track in tracks:
            artist = track["artist"]
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
        
        if artist_counts:
            most_played = max(artist_counts.items(), key=lambda x: x[1])
            return {"name": most_played[0], "count": most_played[1]}
        return {"name": "N/A", "count": 0}
    
    def _get_most_played_track(self, tracks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Obter música mais reproduzida"""
        track_counts = {}
        for track in tracks:
            track_key = f"{track['name']} - {track['artist']}"
            track_counts[track_key] = track_counts.get(track_key, 0) + 1
        
        if track_counts:
            most_played = max(track_counts.items(), key=lambda x: x[1])
            return {"name": most_played[0], "count": most_played[1]}
        return {"name": "N/A", "count": 0}
    
    def search_and_add_to_queue(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Buscar músicas e adicionar todas à fila de reprodução"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            # Buscar músicas
            search_result = self.search_tracks(query, limit)
            tracks = search_result.get("tracks", [])
            
            if not tracks:
                return {
                    "message": f"Nenhuma música encontrada para: '{query}'",
                    "tracks_added": 0,
                    "tracks_found": 0
                }
            
            # Adicionar cada música à fila
            added_count = 0
            failed_tracks = []
            
            for track in tracks:
                try:
                    track_uri = track["uri"]
                    self.client.add_to_queue(uri=track_uri)
                    added_count += 1
                except Exception as e:
                    failed_tracks.append({
                        "name": track["name"],
                        "artist": track["artist"],
                        "error": str(e)
                    })
            
            # Preparar resultado
            result = {
                "message": f"Adicionadas {added_count} de {len(tracks)} músicas à fila",
                "tracks_added": added_count,
                "tracks_found": len(tracks),
                "query": query,
                "added_tracks": tracks[:added_count],
                "failed_tracks": failed_tracks
            }
            
            if failed_tracks:
                result["message"] += f" ({len(failed_tracks)} falharam)"
            
            return result
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar e adicionar à fila: {str(e)}")
    
    def search_and_add_to_favorites(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Buscar músicas e adicionar todas aos favoritos"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            # Buscar músicas
            search_result = self.search_tracks(query, limit)
            tracks = search_result.get("tracks", [])
            
            if not tracks:
                return {
                    "message": f"Nenhuma música encontrada para: '{query}'",
                    "tracks_added": 0,
                    "tracks_found": 0
                }
            
            # Adicionar cada música aos favoritos
            added_count = 0
            already_saved = 0
            failed_tracks = []
            
            for track in tracks:
                try:
                    track_id = track["uri"].split(":")[-1]
                    
                    # Verificar se já está nos favoritos
                    check_result = self.check_track_in_favorites(track_id)
                    if check_result.get("is_saved", False):
                        already_saved += 1
                        continue
                    
                    # Adicionar aos favoritos
                    self.add_track_to_favorites(track_id)
                    added_count += 1
                    
                except Exception as e:
                    failed_tracks.append({
                        "name": track["name"],
                        "artist": track["artist"],
                        "error": str(e)
                    })
            
            # Preparar resultado
            result = {
                "message": f"Adicionadas {added_count} músicas aos favoritos",
                "tracks_added": added_count,
                "tracks_found": len(tracks),
                "already_saved": already_saved,
                "query": query,
                "added_tracks": tracks[:added_count],
                "failed_tracks": failed_tracks
            }
            
            if already_saved > 0:
                result["message"] += f" ({already_saved} já estavam salvas)"
            
            if failed_tracks:
                result["message"] += f" ({len(failed_tracks)} falharam)"
            
            return result
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar e adicionar aos favoritos: {str(e)}")
    
    def search_and_play_all(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Buscar músicas e reproduzir todas em sequência"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            # Buscar músicas
            search_result = self.search_tracks(query, limit)
            tracks = search_result.get("tracks", [])
            
            if not tracks:
                return {
                    "message": f"Nenhuma música encontrada para: '{query}'",
                    "tracks_queued": 0,
                    "tracks_found": 0
                }
            
            # Reproduzir a primeira música
            first_track = tracks[0]
            play_result = self.play_music(first_track["uri"])
            
            # Adicionar as demais à fila
            queued_count = 0
            failed_tracks = []
            
            for track in tracks[1:]:
                try:
                    track_uri = track["uri"]
                    self.client.add_to_queue(uri=track_uri)
                    queued_count += 1
                except Exception as e:
                    failed_tracks.append({
                        "name": track["name"],
                        "artist": track["artist"],
                        "error": str(e)
                    })
            
            # Preparar resultado
            result = {
                "message": f"Reproduzindo '{first_track['name']}' e adicionadas {queued_count} músicas à fila",
                "now_playing": first_track,
                "tracks_queued": queued_count,
                "tracks_found": len(tracks),
                "query": query,
                "queued_tracks": tracks[1:queued_count+1],
                "failed_tracks": failed_tracks
            }
            
            if failed_tracks:
                result["message"] += f" ({len(failed_tracks)} falharam)"
            
            return result
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar e reproduzir: {str(e)}")

    def get_recently_played(self, limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """Obter músicas reproduzidas recentemente"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            recent = self.client.current_user_recently_played(limit=limit)
            tracks = []
            for item in recent["items"]:
                track = item["track"]
                tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"],
                    "played_at": item["played_at"]
                })
            return {"tracks": tracks}
        except Exception as e:
            if "403" in str(e) or "Insufficient client scope" in str(e):
                raise ValueError("Permissão insuficiente. Reautentique com escopo 'user-read-recently-played'")
            raise ValueError(f"Erro ao obter histórico: {str(e)}")

    def get_top_tracks(self, limit: int = 20, time_range: str = "medium_term") -> Dict[str, List[Dict[str, Any]]]:
        """Obter músicas mais tocadas do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            tracks = self.client.current_user_top_tracks(limit=limit, time_range=time_range)
            top_tracks = []
            for track in tracks["items"]:
                top_tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"]
                })
            return {"tracks": top_tracks}
        except Exception as e:
            if "403" in str(e) or "Insufficient client scope" in str(e):
                raise ValueError("Permissão insuficiente. Reautentique com escopo 'user-top-read'")
            raise ValueError(f"Erro ao obter top tracks: {str(e)}")

    def get_top_artists(self, limit: int = 20, time_range: str = "medium_term") -> Dict[str, List[Dict[str, Any]]]:
        """Obter artistas mais ouvidos do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            artists = self.client.current_user_top_artists(limit=limit, time_range=time_range)
            top_artists = []
            for artist in artists["items"]:
                top_artists.append({
                    "name": artist["name"],
                    "uri": artist["uri"],
                    "genres": artist["genres"],
                    "popularity": artist["popularity"]
                })
            return {"artists": top_artists}
        except Exception as e:
            if "403" in str(e) or "Insufficient client scope" in str(e):
                raise ValueError("Permissão insuficiente. Reautentique com escopo 'user-top-read'")
            raise ValueError(f"Erro ao obter top artists: {str(e)}")

    def get_saved_tracks(self, limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """Obter músicas salvas do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            tracks = self.client.current_user_saved_tracks(limit=limit)
            saved_tracks = []
            for item in tracks["items"]:
                track = item["track"]
                saved_tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"]
                })
            return {"tracks": saved_tracks}
        except Exception as e:
            raise ValueError(f"Erro ao obter músicas salvas: {str(e)}")

    def get_saved_albums(self, limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """Obter álbuns salvos do usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            albums = self.client.current_user_saved_albums(limit=limit)
            saved_albums = []
            for item in albums["items"]:
                album = item["album"]
                saved_albums.append({
                    "name": album["name"],
                    "artist": album["artists"][0]["name"],
                    "uri": album["uri"],
                    "release_date": album["release_date"]
                })
            return {"albums": saved_albums}
        except Exception as e:
            raise ValueError(f"Erro ao obter álbuns salvos: {str(e)}")

    def get_followed_artists(self, limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """Obter artistas seguidos pelo usuário"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            artists = self.client.current_user_followed_artists(limit=limit)
            followed_artists = []
            for artist in artists["artists"]["items"]:
                followed_artists.append({
                    "name": artist["name"],
                    "uri": artist["uri"],
                    "genres": artist["genres"],
                    "popularity": artist["popularity"]
                })
            return {"artists": followed_artists}
        except Exception as e:
            if "403" in str(e) or "Insufficient client scope" in str(e):
                raise ValueError("Permissão insuficiente. Reautentique com escopo 'user-follow-read'")
            raise ValueError(f"Erro ao obter artistas seguidos: {str(e)}")

    def search_artists(self, query: str, limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Buscar artistas por nome"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            results = self.client.search(q=query, type="artist", limit=limit)
            artists = []
            for artist in results["artists"]["items"]:
                artists.append({
                    "name": artist["name"],
                    "uri": artist["uri"],
                    "genres": artist["genres"],
                    "popularity": artist["popularity"]
                })
            return {"artists": artists}
        except Exception as e:
            raise ValueError(f"Erro na busca de artistas: {str(e)}")

    def search_albums(self, query: str, limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Buscar álbuns por nome"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            results = self.client.search(q=query, type="album", limit=limit)
            albums = []
            for album in results["albums"]["items"]:
                albums.append({
                    "name": album["name"],
                    "artist": album["artists"][0]["name"],
                    "uri": album["uri"],
                    "release_date": album["release_date"]
                })
            return {"albums": albums}
        except Exception as e:
            raise ValueError(f"Erro na busca de álbuns: {str(e)}")

    def search_playlists(self, query: str, limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Buscar playlists por nome"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            results = self.client.search(q=query, type="playlist", limit=limit)
            playlists = []
            for playlist in results["playlists"]["items"]:
                playlists.append({
                    "name": playlist["name"],
                    "owner": playlist["owner"]["display_name"],
                    "uri": playlist["uri"],
                    "tracks_total": playlist["tracks"]["total"]
                })
            return {"playlists": playlists}
        except Exception as e:
            raise ValueError(f"Erro na busca de playlists: {str(e)}")

    def get_album_tracks(self, album_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Obter músicas de um álbum específico"""
        if not self.client:
            raise ValueError("Cliente Spotipy não inicializado")
        
        try:
            album = self.client.album_tracks(album_id)
            tracks = []
            for track in album["items"]:
                tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"]
                })
            return {"tracks": tracks}
        except Exception as e:
            raise ValueError(f"Erro ao obter músicas do álbum: {str(e)}")


# Instância global do serviço
spotify_service = SpotifyService()
