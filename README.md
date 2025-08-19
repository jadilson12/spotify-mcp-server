# Spotipy MCP Server

[![CI/CD Pipeline](https://github.com/your-username/mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/mcp-server/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-60%20passing-brightgreen)](https://github.com/your-username/mcp-server/actions)

MCP (Model Context Protocol) Server with Spotipy integration for music control via Spotify.

## 🚀 Features

- ✅ Playback control (play, pause, next, previous)
- ✅ Volume adjustment
- ✅ Music search
- ✅ Get current track
- ✅ Playlist management
- ✅ Complete REST API
- ✅ Automatic documentation (Swagger)
- ✅ Complete MCP integration with tools and resources

## 📋 Prerequisites

- Python 3.12+
- Spotify Developer account
- Registered application in Spotify Developer Dashboard

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone <your-repository>
cd mcp-server
```

2. **Install dependencies:**

```bash
make install
```

3. **Configure environment variables:**

```bash
cp env.example .env
```

Edit the `.env` file with your Spotify credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## 🎵 Spotify Configuration

1. Access [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Copy the `Client ID` and `Client Secret`
4. Add `http://localhost:8888/callback` to redirect URLs
5. **Important:** Configure the following scopes in your application:
   - `user-read-playback-state` - Read playback state
   - `user-modify-playback-state` - Control playback
   - `user-read-currently-playing` - Current track
   - `playlist-read-private` - Private playlists
   - `user-library-read` - User library
   - `user-top-read` - Top artists and tracks
   - `user-read-recently-played` - Recently played tracks
   - `user-follow-read` - Followed artists
   - `user-read-email` - User email
   - `user-read-private` - Private information

## 🚀 Usage

### Start the server:

```bash
make dev
```

The server will be available at:

- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛠️ **Development Guide**

### 🔄 **Essential Commands**

```bash
# Complete server restart
pkill -f "python.*mcp-server" && sleep 2 && make dev

# Kill MCP ports (REQUIRED before run-inspector)
lsof -ti:6274 | xargs kill -9 && lsof -ti:6277 | xargs kill -9

# Check ports in use
lsof -i:6274 && lsof -i:6277
```

### ⚠️ **IMPORTANT: Always Kill Ports!**

**BEFORE running `make run-inspector`, ALWAYS execute:**

```bash
# Kill MCP ports (REQUIRED)
lsof -ti:6274 | xargs kill -9 && lsof -ti:6277 | xargs kill -9
```

**Why is this necessary?**

- MCP Inspector uses ports 6274 (UI) and 6277 (Proxy)
- If ports are occupied, Inspector cannot start
- Previous processes may have left ports in use

### 🎯 **Development Workflow**

1. **After Modifying Code:**
```bash
pkill -f "python.*mcp-server" && sleep 2 && make dev
```

2. **To Test with MCP Inspector:**
```bash
lsof -ti:6274 | xargs kill -9 && lsof -ti:6277 | xargs kill -9
make run-inspector
```

### Available commands:

```bash
make dev              # Start development server
make install          # Install dependencies
make clean            # Clean temporary files
make test             # Run tests
make lint             # Check code quality
make format           # Format code
make run-inspector    # Run MCP Inspector
make help             # Show help
```

## 🎵 **MCP Features**

### **Available Tools:**

- `play_music` - Play music
- `search_tracks` - Search tracks
- `get_current_track` - Current track
- `get_playlists` - List playlists
- `get_recommendations` - Recommendations
- `get_user_profile` - User profile
- `get_devices` - Available devices
- `get_queue` - Playback queue
- `get_genres` - Music genres
- `get_audio_features` - Audio characteristics

### **Available Resources:**

- `spotify://playback/current` - Current playback
- `spotify://playlists` - User playlists
- `spotify://devices` - Devices
- `spotify://genres` - Genres
- `spotify://profile` - User profile
- `spotify://playback/queue` - Playback queue

### **Resource Templates:**

- `spotify://playlist/{playlist_id}` - Specific playlist
- `spotify://track/{track_id}` - Specific track
- `spotify://artist/{artist_id}` - Specific artist
- `spotify://album/{album_id}` - Specific album
- `spotify://search/{query}` - Search results

## 📚 API Endpoints

### Authentication

- `POST /auth` - Authenticate with Spotify
- `POST /auth/reauth` - Re-authenticate with configured credentials

### Playback

- `GET /current-track` - Get current track
- `POST /play` - Play music
- `POST /pause` - Pause music
- `POST /next` - Next track
- `POST /previous` - Previous track
- `POST /volume/{volume}` - Adjust volume (0-100)
- `POST /seek/{position_ms}` - Seek to specific position
- `POST /shuffle` - Toggle shuffle mode
- `POST /repeat` - Toggle repeat mode

### Playlists and Albums

- `GET /playlists` - Get user playlists
- `GET /playlist/{playlist_id}` - Get playlist tracks
- `GET /albums` - Get user saved albums
- `GET /tracks` - Get user saved tracks

### Artists and Top Tracks

- `GET /artists` - Get user favorite artists
- `GET /tracks/top` - Get most played tracks

### Playback Queue

- `GET /queue` - Get current playback queue
- `POST /queue/add` - Add track to queue

### Devices

- `GET /devices` - Get available devices
- `POST /devices/{device_id}/transfer` - Transfer playback

### Search and Recommendations

- `GET /search/{query}` - Search tracks
- `GET /recommendations` - Get personalized recommendations
- `GET /genres` - Get available music genres

### User and Analysis

- `GET /user/profile` - Get user profile
- `GET /audio-features/{track_id}` - Get audio features

### System

- `GET /` - Server status
- `GET /health` - Health check

## 🔧 Usage Examples

### Play a specific track:

```bash
curl -X POST "http://localhost:8000/play" \
  -H "Content-Type: application/json" \
  -d '{"track_uri": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"}'
```

### Search tracks:

```bash
curl "http://localhost:8000/search/bohemian%20rhapsody?limit=5"
```

### Adjust volume:

```bash
curl -X POST "http://localhost:8000/volume/50"
```

### Get current track:

```bash
curl "http://localhost:8000/current-track"
```

### Get user playlists:

```bash
curl "http://localhost:8000/playlists"
```

### Get tracks from a specific playlist:

```bash
curl "http://localhost:8000/playlist/37i9dQZF1DXcBWIGoYBM5M"
```

### Get saved tracks:

```bash
curl "http://localhost:8000/tracks"
```

### Get favorite artists:

```bash
curl "http://localhost:8000/artists"
```

### Get recommendations based on artists:

```bash
curl "http://localhost:8000/recommendations?seed_artists=4gzpq5DPGxSnKTe4SA8HAU&limit=10"
```

### Toggle shuffle:

```bash
curl -X POST "http://localhost:8000/shuffle"
```

### Add track to queue:

```bash
curl -X POST "http://localhost:8000/queue/add?track_uri=spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
```

### Get available devices:

```bash
curl "http://localhost:8000/devices"
```

### Seek to specific position (30 seconds):

```bash
curl -X POST "http://localhost:8000/seek/30000"
```

### Re-authenticate with Spotify:

```bash
curl -X POST "http://localhost:8000/auth/reauth"
```

## 🚀 CI/CD Pipeline

### 📊 **Pipeline Status**

Our CI/CD pipeline ensures code quality and security:

- ✅ **Tests**: 60 tests passing on Python 3.12 & 3.13
- ✅ **Linting**: Code quality checks with flake8
- ✅ **Formatting**: Black and isort formatting validation
- ✅ **Security**: Secrets detection and .env file validation
- ✅ **Build**: Package building and artifact generation

### 🔄 **Pipeline Jobs**

| Job | Description | Status |
|-----|-------------|--------|
| **Test** | Run all tests on Python 3.12 & 3.13 | ![Test](https://github.com/your-username/mcp-server/actions/workflows/ci.yml/badge.svg?job=test) |
| **Lint** | Code quality and formatting checks | ![Lint](https://github.com/your-username/mcp-server/actions/workflows/ci.yml/badge.svg?job=lint) |
| **Security** | Secrets detection and security validation | ![Security](https://github.com/your-username/mcp-server/actions/workflows/ci.yml/badge.svg?job=security) |
| **Build** | Package building and distribution | ![Build](https://github.com/your-username/mcp-server/actions/workflows/ci.yml/badge.svg?job=build) |

### 🛡️ **Security Checks**

The pipeline includes comprehensive security validation:

- **🔍 TruffleHog**: Advanced secret scanner for detecting credentials
- **🕵️ detect-secrets**: Multi-pattern secret detection with baseline
- **🔐 Pattern Matching**: Custom regex patterns for sensitive data
- **📁 File Validation**: Checks for committed sensitive files (.env, .key, .pem)
- **⚙️ Gitignore Validation**: Ensures sensitive file patterns are ignored
- **🌐 URL Scanning**: Detects hardcoded cloud service URLs
- **📊 Security Reports**: Generates detailed security scan artifacts

**Protected Patterns:**
- API keys and tokens
- Passwords and secrets
- Base64/Hex encoded strings
- AWS, Google, Azure credentials
- Private keys and certificates
- Spotify client credentials

### 📋 **Local Pipeline Testing**

Test the pipeline locally before pushing:

```bash
# Run all pipeline checks locally
make test-pytest    # Tests
make lint          # Linting
make format        # Formatting
make security      # Security checks
```

### 🔐 **Security Commands**

```bash
# Run security checks
make security       # Basic security validation

# Full security scan (requires tools)
pip install detect-secrets truffleHog3
detect-secrets scan --all-files
trufflehog3 --format json .
```

## 🧪 Tests

✅ **60 tests PASSING** | ⏱️ **~0.38s** | 🔧 **100% Functional**

### 🚀 **Run Tests**

```bash
# Run all tests (recommended)
make test-pytest

# Or use pytest directly
python -m pytest tests/ -v --tb=short --color=yes
```

### 📋 **Test Coverage**

#### 🔧 **MCP Tools Tests (36 tests)**
- ✅ Playback control (`play_music`, `pause_music`, `next_track`, `previous_track`)
- ✅ Volume management (`set_volume`)
- ✅ Search and discovery (`search_tracks`, `search_artists`, `search_albums`, `search_playlists`)
- ✅ Playlists and albums (`get_playlists`, `get_playlist_tracks`, `get_album_tracks`)
- ✅ Profile and preferences (`get_user_profile`, `get_top_tracks`, `get_top_artists`)
- ✅ Personal library (`get_saved_tracks`, `get_saved_albums`, `get_followed_artists`)
- ✅ Devices and queue (`get_devices`, `get_queue`, `add_to_queue`)
- ✅ Recommendations (`get_recommendations`, `get_genres`, `get_audio_features`)
- ✅ Navigation (`skip_to_next`, `skip_to_previous`, `seek_to_position`)
- ✅ History (`get_recently_played`)
- ✅ Related artists (`get_related_artists`, `get_artist_top_tracks`, `get_artist_albums`)

#### 💬 **MCP Prompts Tests (6 tests)**
- ✅ `spotify_assistant` - Intelligent music assistant
- ✅ `spotify_usage_guide` - Feature usage guide
- ✅ `spotify_troubleshooting` - Problem solving

#### 📚 **MCP Resources Tests (12 tests)**
- ✅ `spotify://playback/current` - Current playback state
- ✅ `spotify://playlists/user` - User playlists
- ✅ `spotify://devices/available` - Available devices
- ✅ `spotify://genres/available` - Music genres
- ✅ `spotify://user/profile` - User profile
- ✅ `spotify://playback/queue` - Playback queue
- ✅ `spotify://user/top-tracks` - Top tracks
- ✅ `spotify://user/top-artists` - Top artists
- ✅ `spotify://user/recently-played` - Recently played
- ✅ `spotify://user/saved-tracks` - Saved tracks
- ✅ `spotify://user/saved-albums` - Saved albums
- ✅ `spotify://user/followed-artists` - Followed artists

#### 🔧 **Functionality Tests (3 tests)**
- ✅ Correct tool structure
- ✅ Valid descriptions in all tools
- ✅ Error handling implemented

#### 📊 **Validation Tests (2 tests)**
- ✅ Volume request validation
- ✅ Search request validation

#### 🔗 **Integration Test (1 test)**
- ✅ Server completeness (tools, prompts, resources)

### 🎯 **Available Test Commands**

```bash
# Run all tests
make test-pytest           # Using pytest (recommended)

# Specific tests (future)
make test-tools            # Tools tests only
make test-prompts          # Prompts tests only  
make test-resources        # Resources tests only
make test-integration      # Integration tests only
make test-coverage         # Check coverage

# Test with detailed output
python -m pytest tests/ -v -s --tb=long
```

### 📈 **Latest Test Results**

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

### 🔍 **Test Structure**

```
tests/
├── test_main.py          # All MCP server tests
├── __init__.py           # Module initialization
└── README.md            # Test documentation
```

### 🧪 **How to Add New Tests**

1. **For new tool:**
```python
@pytest.mark.asyncio
async def test_new_tool_exists(self):
    """Test if new tool exists"""
    tools = await app.get_tools()
    assert 'new_tool' in tools
```

2. **For new resource:**
```python
@pytest.mark.asyncio
async def test_new_resource_exists(self):
    """Test if new resource exists"""
    resources = await app.get_resources()
    assert 'spotify://new/resource' in resources
```

### ⚠️ **Important for Tests**

- **ALWAYS** run tests after modifying code
- Use `make test-pytest` for fast and reliable execution
- Tests don't require real Spotify authentication
- Tests focus on structure and feature availability

## 🔍 Linting and Formatting

```bash
make lint    # Check code quality
make format  # Format code automatically
```

## 📝 Project Structure

```
mcp-server/
├── src/
│   ├── mcp-server.py    # Main MCP server
│   ├── service.py       # Spotify logic
│   ├── server.py        # FastAPI server
│   └── config.py        # Configuration
├── tests/               # Tests
├── makefile             # Development commands
├── pyproject.toml       # Project configuration
├── mcp-config.json      # MCP Inspector config
├── env.example          # Environment variables example
└── README.md           # This file
```

## ⚠️ **Common Issues**

### **Error: "PORT IS IN USE"**

```bash
# Quick solution
lsof -ti:6274 | xargs kill -9
lsof -ti:6277 | xargs kill -9
```

### **Error: "ModuleNotFoundError"**

```bash
# Reinstall dependencies
make install
```

### **Server not responding**

```bash
# Complete restart
pkill -f "python.*mcp-server" && sleep 2 && make dev
```

### **Error 403 - Insufficient Permission**

If you receive error 403 with message "Insufficient client scope":

1. Verify all required scopes are configured
2. Re-authenticate with Spotify using `/auth` endpoint
3. Make sure you accepted all requested permissions

### **Endpoints Requiring Specific Permissions**

- `/artists` and `/tracks/top` - Require `user-top-read`
- `/recommendations` - Require at least one valid seed
- `/user/profile` - Require `user-read-email` and `user-read-private`

### **Known Issues**

- **Recommendations (404)**: The recommendations API may return 404 in some cases. This can be due to:
  - Temporary Spotify API issues
  - Invalid or not found seeds
  - Authentication problems
- **Solution**: Use `/auth/reauth` endpoint to re-authenticate if necessary

## 🔧 **Important Tips**

1. **ALWAYS** restart server after modifying `mcp-server.py`
2. **ALWAYS** kill ports before running Inspector (6274 and 6277)
3. **ALWAYS** verify ports are free before running `make run-inspector`
4. **Check logs** to identify problems
5. **Use `make dev`** for local development
6. **Keep `.env`** properly configured

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### 🚀 **Development Workflow**

1. **Fork the project**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make your changes and test locally:**
   ```bash
   make test-pytest    # Run tests
   make lint          # Check code quality
   make format        # Format code
   ```
4. **Commit your changes:**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
5. **Push to your branch:**
   ```bash
   git push origin feature/AmazingFeature
   ```
6. **Open a Pull Request**

### ✅ **CI/CD Requirements**

All contributions must pass our CI/CD pipeline:

- **Tests**: All 60 tests must pass
- **Linting**: Code must pass flake8 checks
- **Formatting**: Code must be properly formatted with Black
- **Security**: No secrets or sensitive files committed
- **Build**: Package must build successfully

### 🛡️ **Security Guidelines**

- **Never commit** `.env` files or credentials
- **Use placeholders** in examples (e.g., `your_client_id_here`)
- **Follow** the security checklist in `SECURITY.md`
- **Test locally** before pushing

### 📋 **Code Quality Standards**

- **Python 3.12+** compatibility
- **Type hints** for all functions
- **Docstrings** for all public functions
- **Error handling** for all external API calls
- **Tests** for new functionality

## 📄 License

This project is under MIT license. See the `LICENSE` file for more details.

## 🆘 Support

If you encounter any problems or have questions:

1. Check if Spotify credentials are correct
2. Make sure Spotify is running on some device
3. Check server logs for more details
4. Open an issue in the repository

## 🔗 Useful Links

- [Spotipy Documentation](https://spotipy.readthedocs.io/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

**🎵 Music is life! Let's make an amazing MCP server! 🚀**
