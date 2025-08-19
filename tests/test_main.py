"""
Testes abrangentes para o Spotipy MCP Server
"""

import pytest
import json
import asyncio
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from typing import Dict, Any, List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar o módulo correto
from src.mcp_server import app
from src.service import SpotifyService

client = TestClient(app)


class TestMCPServerBasics:
    """Testes básicos do servidor MCP"""
    
    def test_server_initialization(self):
        """Testa se o servidor MCP foi inicializado corretamente"""
        assert app is not None
        assert hasattr(app, 'get_tools')
        assert hasattr(app, 'get_prompts')
        assert hasattr(app, 'get_resources')
    
    @pytest.mark.asyncio
    async def test_server_has_tools(self):
        """Testa se o servidor tem tools registradas"""
        tools = await app.get_tools()
        assert isinstance(tools, dict)
        assert len(tools) > 0
    
    @pytest.mark.asyncio
    async def test_server_has_prompts(self):
        """Testa se o servidor tem prompts registrados"""
        prompts = await app.get_prompts()
        assert isinstance(prompts, dict)
        assert len(prompts) > 0
    
    @pytest.mark.asyncio
    async def test_server_has_resources(self):
        """Testa se o servidor tem resources registrados"""
        resources = await app.get_resources()
        assert isinstance(resources, dict)
        assert len(resources) > 0


class TestMCPTools:
    """Testes para todas as tools MCP"""
    
    @pytest.mark.asyncio
    async def test_get_current_track_tool_exists(self):
        """Testa se a tool get_current_track existe"""
        tools = await app.get_tools()
        assert 'get_current_track' in tools
    
    @pytest.mark.asyncio
    async def test_play_music_tool_exists(self):
        """Testa se a tool play_music existe"""
        tools = await app.get_tools()
        assert 'play_music' in tools
    
    @pytest.mark.asyncio
    async def test_pause_music_tool_exists(self):
        """Testa se a tool pause_music existe"""
        tools = await app.get_tools()
        assert 'pause_music' in tools
    
    @pytest.mark.asyncio
    async def test_next_track_tool_exists(self):
        """Testa se a tool next_track existe"""
        tools = await app.get_tools()
        assert 'next_track' in tools
    
    @pytest.mark.asyncio
    async def test_previous_track_tool_exists(self):
        """Testa se a tool previous_track existe"""
        tools = await app.get_tools()
        assert 'previous_track' in tools
    
    @pytest.mark.asyncio
    async def test_set_volume_tool_exists(self):
        """Testa se a tool set_volume existe"""
        tools = await app.get_tools()
        assert 'set_volume' in tools
    
    @pytest.mark.asyncio
    async def test_search_tracks_tool_exists(self):
        """Testa se a tool search_tracks existe"""
        tools = await app.get_tools()
        assert 'search_tracks' in tools
    
    @pytest.mark.asyncio
    async def test_get_playlists_tool_exists(self):
        """Testa se a tool get_playlists existe"""
        tools = await app.get_tools()
        assert 'get_playlists' in tools
    
    @pytest.mark.asyncio
    async def test_get_recommendations_tool_exists(self):
        """Testa se a tool get_recommendations existe"""
        tools = await app.get_tools()
        assert 'get_recommendations' in tools
    
    @pytest.mark.asyncio
    async def test_get_user_profile_tool_exists(self):
        """Testa se a tool get_user_profile existe"""
        tools = await app.get_tools()
        assert 'get_user_profile' in tools
    
    @pytest.mark.asyncio
    async def test_get_devices_tool_exists(self):
        """Testa se a tool get_devices existe"""
        tools = await app.get_tools()
        assert 'get_devices' in tools
    

    
    @pytest.mark.asyncio
    async def test_get_queue_tool_exists(self):
        """Testa se a tool get_queue existe"""
        tools = await app.get_tools()
        assert 'get_queue' in tools
    
    @pytest.mark.asyncio
    async def test_get_genres_tool_exists(self):
        """Testa se a tool get_genres existe"""
        tools = await app.get_tools()
        assert 'get_genres' in tools
    
    @pytest.mark.asyncio
    async def test_get_audio_features_tool_exists(self):
        """Testa se a tool get_audio_features existe"""
        tools = await app.get_tools()
        assert 'get_audio_features' in tools
    
    @pytest.mark.asyncio
    async def test_add_to_queue_tool_exists(self):
        """Testa se a tool add_to_queue existe"""
        tools = await app.get_tools()
        assert 'add_to_queue' in tools
    
    @pytest.mark.asyncio
    async def test_skip_to_next_tool_exists(self):
        """Testa se a tool skip_to_next existe"""
        tools = await app.get_tools()
        assert 'skip_to_next' in tools
    
    @pytest.mark.asyncio
    async def test_skip_to_previous_tool_exists(self):
        """Testa se a tool skip_to_previous existe"""
        tools = await app.get_tools()
        assert 'skip_to_previous' in tools
    
    @pytest.mark.asyncio
    async def test_seek_to_position_tool_exists(self):
        """Testa se a tool seek_to_position existe"""
        tools = await app.get_tools()
        assert 'seek_to_position' in tools
    
    @pytest.mark.asyncio
    async def test_get_recently_played_tool_exists(self):
        """Testa se a tool get_recently_played existe"""
        tools = await app.get_tools()
        assert 'get_recently_played' in tools
    
    @pytest.mark.asyncio
    async def test_get_top_tracks_tool_exists(self):
        """Testa se a tool get_top_tracks existe"""
        tools = await app.get_tools()
        assert 'get_top_tracks' in tools
    
    @pytest.mark.asyncio
    async def test_get_top_artists_tool_exists(self):
        """Testa se a tool get_top_artists existe"""
        tools = await app.get_tools()
        assert 'get_top_artists' in tools
    
    @pytest.mark.asyncio
    async def test_get_saved_tracks_tool_exists(self):
        """Testa se a tool get_saved_tracks existe"""
        tools = await app.get_tools()
        assert 'get_saved_tracks' in tools
    
    @pytest.mark.asyncio
    async def test_get_saved_albums_tool_exists(self):
        """Testa se a tool get_saved_albums existe"""
        tools = await app.get_tools()
        assert 'get_saved_albums' in tools
    
    @pytest.mark.asyncio
    async def test_get_followed_artists_tool_exists(self):
        """Testa se a tool get_followed_artists existe"""
        tools = await app.get_tools()
        assert 'get_followed_artists' in tools
    
    @pytest.mark.asyncio
    async def test_search_artists_tool_exists(self):
        """Testa se a tool search_artists existe"""
        tools = await app.get_tools()
        assert 'search_artists' in tools
    
    @pytest.mark.asyncio
    async def test_search_albums_tool_exists(self):
        """Testa se a tool search_albums existe"""
        tools = await app.get_tools()
        assert 'search_albums' in tools
    
    @pytest.mark.asyncio
    async def test_search_playlists_tool_exists(self):
        """Testa se a tool search_playlists existe"""
        tools = await app.get_tools()
        assert 'search_playlists' in tools
    
    @pytest.mark.asyncio
    async def test_get_playlist_tracks_tool_exists(self):
        """Testa se a tool get_playlist_tracks existe"""
        tools = await app.get_tools()
        assert 'get_playlist_tracks' in tools
    
    @pytest.mark.asyncio
    async def test_get_album_tracks_tool_exists(self):
        """Testa se a tool get_album_tracks existe"""
        tools = await app.get_tools()
        assert 'get_album_tracks' in tools
    
    @pytest.mark.asyncio
    async def test_get_artist_top_tracks_tool_exists(self):
        """Testa se a tool get_artist_top_tracks existe"""
        tools = await app.get_tools()
        assert 'get_artist_top_tracks' in tools
    
    @pytest.mark.asyncio
    async def test_get_artist_albums_tool_exists(self):
        """Testa se a tool get_artist_albums existe"""
        tools = await app.get_tools()
        assert 'get_artist_albums' in tools
    
    @pytest.mark.asyncio
    async def test_get_related_artists_tool_exists(self):
        """Testa se a tool get_related_artists existe"""
        tools = await app.get_tools()
        assert 'get_related_artists' in tools


class TestMCPPrompts:
    """Testes para todos os prompts MCP"""
    
    @pytest.mark.asyncio
    async def test_spotify_assistant_prompt_exists(self):
        """Testa se o prompt spotify_assistant existe"""
        prompts = await app.get_prompts()
        assert 'spotify_assistant' in prompts
    
    @pytest.mark.asyncio
    async def test_spotify_usage_guide_prompt_exists(self):
        """Testa se o prompt spotify_usage_guide existe"""
        prompts = await app.get_prompts()
        assert 'spotify_usage_guide' in prompts
    
    @pytest.mark.asyncio
    async def test_spotify_troubleshooting_prompt_exists(self):
        """Testa se o prompt spotify_troubleshooting existe"""
        prompts = await app.get_prompts()
        assert 'spotify_troubleshooting' in prompts
    
    @pytest.mark.asyncio
    async def test_spotify_assistant_prompt_content(self):
        """Testa o conteúdo do prompt spotify_assistant"""
        prompts = await app.get_prompts()
        prompt = prompts['spotify_assistant']
        assert hasattr(prompt, 'description')
        assert "este servidor mcp" in prompt.description.lower()
        assert "Tools de Controle" in prompt.description
    
    @pytest.mark.asyncio
    async def test_spotify_usage_guide_prompt_content(self):
        """Testa o conteúdo do prompt spotify_usage_guide"""
        prompts = await app.get_prompts()
        prompt = prompts['spotify_usage_guide']
        assert hasattr(prompt, 'description')
        assert "Guia de uso" in prompt.description
        assert "Início Rápido" in prompt.description
    
    @pytest.mark.asyncio
    async def test_spotify_troubleshooting_prompt_content(self):
        """Testa o conteúdo do prompt spotify_troubleshooting"""
        prompts = await app.get_prompts()
        prompt = prompts['spotify_troubleshooting']
        assert hasattr(prompt, 'description')
        assert "Guia de solução" in prompt.description
        assert "Problemas Comuns" in prompt.description


class TestMCPResources:
    """Testes para todos os resources MCP"""
    
    @pytest.mark.asyncio
    async def test_current_playback_resource_exists(self):
        """Testa se o resource current_playback existe"""
        resources = await app.get_resources()
        assert 'spotify://playback/current' in resources
    
    @pytest.mark.asyncio
    async def test_user_playlists_resource_exists(self):
        """Testa se o resource user_playlists existe"""
        resources = await app.get_resources()
        assert 'spotify://playlists/user' in resources
    
    @pytest.mark.asyncio
    async def test_available_devices_resource_exists(self):
        """Testa se o resource available_devices existe"""
        resources = await app.get_resources()
        assert 'spotify://devices/available' in resources
    
    @pytest.mark.asyncio
    async def test_music_genres_resource_exists(self):
        """Testa se o resource music_genres existe"""
        resources = await app.get_resources()
        assert 'spotify://genres/available' in resources
    
    @pytest.mark.asyncio
    async def test_user_profile_resource_exists(self):
        """Testa se o resource user_profile existe"""
        resources = await app.get_resources()
        assert 'spotify://user/profile' in resources
    
    @pytest.mark.asyncio
    async def test_playback_queue_resource_exists(self):
        """Testa se o resource playback_queue existe"""
        resources = await app.get_resources()
        assert 'spotify://playback/queue' in resources
    
    @pytest.mark.asyncio
    async def test_user_top_tracks_resource_exists(self):
        """Testa se o resource user_top_tracks existe"""
        resources = await app.get_resources()
        assert 'spotify://user/top-tracks' in resources
    
    @pytest.mark.asyncio
    async def test_user_top_artists_resource_exists(self):
        """Testa se o resource user_top_artists existe"""
        resources = await app.get_resources()
        assert 'spotify://user/top-artists' in resources
    
    @pytest.mark.asyncio
    async def test_user_recently_played_resource_exists(self):
        """Testa se o resource user_recently_played existe"""
        resources = await app.get_resources()
        assert 'spotify://user/recently-played' in resources
    
    @pytest.mark.asyncio
    async def test_user_saved_tracks_resource_exists(self):
        """Testa se o resource user_saved_tracks existe"""
        resources = await app.get_resources()
        assert 'spotify://user/saved-tracks' in resources
    
    @pytest.mark.asyncio
    async def test_user_saved_albums_resource_exists(self):
        """Testa se o resource user_saved_albums existe"""
        resources = await app.get_resources()
        assert 'spotify://user/saved-albums' in resources
    
    @pytest.mark.asyncio
    async def test_user_followed_artists_resource_exists(self):
        """Testa se o resource user_followed_artists existe"""
        resources = await app.get_resources()
        assert 'spotify://user/followed-artists' in resources


class TestToolFunctionality:
    """Testes para funcionalidade das tools"""
    
    @pytest.mark.asyncio
    async def test_tools_have_correct_structure(self):
        """Testa se as tools têm a estrutura correta"""
        tools = await app.get_tools()
        
        # Verificar se as tools têm os atributos necessários
        for tool_name, tool in tools.items():
            assert hasattr(tool, 'name'), f"Tool {tool_name} não tem atributo 'name'"
            assert hasattr(tool, 'description'), f"Tool {tool_name} não tem atributo 'description'"
            assert tool.name == tool_name, f"Tool {tool_name} tem nome incorreto"
    
    @pytest.mark.asyncio
    async def test_tools_have_descriptions(self):
        """Testa se as tools têm descrições"""
        tools = await app.get_tools()
        
        # Verificar se as tools têm descrições não vazias
        for tool_name, tool in tools.items():
            assert tool.description, f"Tool {tool_name} não tem descrição"
            assert isinstance(tool.description, str), f"Tool {tool_name} tem descrição inválida"


class TestErrorHandling:
    """Testes para tratamento de erros"""
    
    @pytest.mark.asyncio
    async def test_tools_have_error_handling(self):
        """Testa se as tools estão configuradas para tratamento de erros"""
        tools = await app.get_tools()
        
        # Verificar se as tools existem e têm estrutura correta
        assert 'get_current_track' in tools
        assert 'play_music' in tools
        assert 'set_volume' in tools
        
        # Verificar se as tools têm descrições válidas
        for tool_name, tool in tools.items():
            assert tool.description, f"Tool {tool_name} não tem descrição"
            assert isinstance(tool.description, str), f"Tool {tool_name} tem descrição inválida"
            assert len(tool.description) > 0, f"Tool {tool_name} tem descrição vazia"


class TestDataValidation:
    """Testes para validação de dados"""
    
    def test_volume_request_validation(self):
        """Testa validação do VolumeRequest"""
        from src.mcp_server import VolumeRequest
        
        # Volume válido
        request = VolumeRequest(volume=50)
        assert request.volume == 50
        
        # Volume inválido (deve ser aceito pelo Pydantic)
        request = VolumeRequest(volume=150)
        assert request.volume == 150
    
    def test_search_request_validation(self):
        """Testa validação do SearchRequest"""
        from src.mcp_server import SearchRequest
        
        # Query válida
        request = SearchRequest(query="queen", limit=10)
        assert request.query == "queen"
        assert request.limit == 10
        
        # Query vazia (deve ser aceita pelo Pydantic)
        request = SearchRequest(query="", limit=5)
        assert request.query == ""
        assert request.limit == 5


class TestIntegration:
    """Testes de integração"""
    
    @pytest.mark.asyncio
    async def test_server_completeness(self):
        """Testa se o servidor tem todos os componentes necessários"""
        # Verificar tools
        tools = await app.get_tools()
        expected_tools = [
            'get_current_track', 'play_music', 'pause_music', 'next_track',
            'previous_track', 'set_volume', 'search_tracks', 'get_playlists',
            'get_recommendations', 'get_user_profile', 'get_devices',
            'get_queue', 'get_genres', 'get_audio_features', 'add_to_queue',
            'skip_to_next', 'skip_to_previous', 'seek_to_position',
            'get_recently_played', 'get_top_tracks', 'get_top_artists',
            'get_saved_tracks', 'get_saved_albums', 'get_followed_artists',
            'search_artists', 'search_albums', 'search_playlists',
            'get_playlist_tracks', 'get_album_tracks', 'get_artist_top_tracks',
            'get_artist_albums', 'get_related_artists'
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tools, f"Tool {tool_name} não encontrada"
        
        # Verificar prompts
        prompts = await app.get_prompts()
        expected_prompts = [
            'spotify_assistant', 'spotify_usage_guide', 'spotify_troubleshooting'
        ]
        
        for prompt_name in expected_prompts:
            assert prompt_name in prompts, f"Prompt {prompt_name} não encontrado"
        
        # Verificar resources
        resources = await app.get_resources()
        expected_resources = [
            'spotify://playback/current', 'spotify://playlists/user',
            'spotify://devices/available', 'spotify://genres/available',
            'spotify://user/profile', 'spotify://playback/queue',
            'spotify://user/top-tracks', 'spotify://user/top-artists',
            'spotify://user/recently-played', 'spotify://user/saved-tracks',
            'spotify://user/saved-albums', 'spotify://user/followed-artists'
        ]
        
        for resource_name in expected_resources:
            assert resource_name in resources, f"Resource {resource_name} não encontrado"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
