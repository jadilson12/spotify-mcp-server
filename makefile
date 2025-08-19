.PHONY: dev install clean test lint format start

# Comando principal para desenvolvimento
dev:
	@echo "🚀 Iniciando servidor MCP com Spotipy..."
	python main.py

# Instalar dependências
install:
	@echo "📦 Instalando dependências..."
	pip install -e .

# Instalar MCP Inspector
install-inspector:
	@echo "🔧 Instalando MCP Inspector..."
	npm install -g @modelcontextprotocol/inspector

# Verificações de segurança
security:
	@echo "🔒 Executando verificações de segurança..."
	@echo "🔍 Verificando padrões sensíveis..."
	@if grep -rE "password\s*=\s*['\"][^'\"]{3,}" . \
		--exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=.git \
		--exclude="*.pyc" --exclude="*.log" | \
		grep -v "your_client_id_here\|example\|placeholder"; then \
		echo "❌ Possível senha encontrada!"; exit 1; \
	else echo "✅ Nenhuma senha encontrada"; fi
	@echo "🔍 Verificando arquivos .env..."
	@if [ -f ".env" ]; then echo "❌ Arquivo .env encontrado!"; exit 1; else echo "✅ Nenhum arquivo .env encontrado"; fi
	@echo "✅ Verificações de segurança concluídas"

# Limpar cache e arquivos temporários
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -f trufflehog_results.json security_report.txt

# Executar testes
test:
	@echo "🧪 Executando todos os testes..."
	python run_tests.py

# Executar testes específicos
test-tools:
	@echo "🔧 Executando testes de tools..."
	python run_tests.py tools

test-prompts:
	@echo "💬 Executando testes de prompts..."
	python run_tests.py prompts

test-resources:
	@echo "📚 Executando testes de resources..."
	python run_tests.py resources

test-integration:
	@echo "🔗 Executando testes de integração..."
	python run_tests.py integration

# Verificar cobertura de testes
test-coverage:
	@echo "📊 Verificando cobertura de testes..."
	python run_tests.py coverage

# Executar testes com pytest diretamente
test-pytest:
	@echo "🧪 Executando testes com pytest..."
	python -m pytest tests/ -v --tb=short --color=yes

# Verificar linting
lint:
	@echo "🔍 Verificando código..."
	flake8 src/ tests/
	black --check src/ tests/

# Formatar código
format:
	@echo "✨ Formatando código..."
	black src/ tests/
	isort src/ tests/

# Iniciar servidor FastAPI
api:
	@echo "🚀 Iniciando API FastAPI..."
	python -m server.main

# Iniciar servidor MCP
mcp:
	@echo "🎵 Iniciando MCP Server..."
	python main.py

# Testar com MCP Inspector
test-inspector:
	@echo "🔍 Testando servidor MCP com Inspector..."
	@echo "📋 Certifique-se de que o servidor MCP está rodando em outro terminal"
	@echo "🌐 Acesse: https://modelcontextprotocol.io/inspector"
	@echo "📡 URL do servidor: http://localhost:8000"
	@echo ""
	@echo "Ou use o comando:"
	@echo "npx @modelcontextprotocol/inspector"

# Executar MCP Inspector localmente
run-inspector:
	@echo "🚀 Executando MCP Inspector..."
	npx @modelcontextprotocol/inspector

# Iniciar servidor MCP e Inspector (em background)
dev-full:
	@echo "🎵 Iniciando servidor MCP e Inspector..."
	@echo "📡 Servidor MCP: http://localhost:8000"
	@echo "🔍 Inspector: https://modelcontextprotocol.io/inspector"
	@echo ""
	@echo "Pressione Ctrl+C para parar ambos"
	@echo ""
	@(make mcp &) && sleep 3 && make run-inspector

# Iniciar com script de configuração
start:
	@echo "🎵 Iniciando Spotipy MCP Server com configuração automática..."
	./start.sh

# Comandos de recuperação e diagnóstico
test-connection:
	@echo "🔍 Testando conectividade..."
	@python -c "import requests; print('✅ Conectividade OK' if requests.get('https://api.spotify.com/v1', timeout=5).status_code == 401 else '❌ Problema de conectividade')" 2>/dev/null || echo "❌ Erro de conectividade"

status:
	@echo "📊 Status dos serviços..."
	@echo "Spotify API: $(shell curl -s -o /dev/null -w '%{http_code}' https://api.spotify.com/v1 2>/dev/null || echo 'offline')"

diagnostic:
	@echo "🔍 Executando diagnóstico básico..."
	@make test-connection

recovery:
	@echo "🔄 Executando recuperação básica..."
	@make auto-recovery

full-recovery:
	@echo "🔄 Executando recuperação completa..."
	@make auto-recovery

restart-with-retry:
	@echo "🔄 Reiniciando com retry automático..."
	@make clean
	@make install
	@make dev

auto-recovery:
	@echo "🔧 Recuperação automática..."
	@make clean
	@rm -f .spotify_token_cache .cache
	@make install
	@echo "✅ Recuperação concluída. Execute 'make dev' para iniciar"

reauth:
	@echo "🔐 Reautenticando com Spotify..."
	@rm -f .spotify_token_cache
	@python -c "from src.service import spotify_service; spotify_service.authenticate()"



# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "🚀 Desenvolvimento:"
	@echo "  make start      - Iniciar servidor com configuração automática"
	@echo "  make dev        - Iniciar servidor MCP (padrão)"
	@echo "  make dev-full   - Iniciar servidor MCP + Inspector"
	@echo "  make api        - Iniciar servidor FastAPI"
	@echo "  make mcp        - Iniciar servidor MCP"
	@echo ""
	@echo "🧪 Testes:"
	@echo "  make test       - Executar todos os testes"
	@echo "  make test-tools - Executar testes de tools"
	@echo "  make test-prompts - Executar testes de prompts"
	@echo "  make test-resources - Executar testes de resources"
	@echo "  make test-integration - Executar testes de integração"
	@echo "  make test-coverage - Verificar cobertura de testes"
	@echo "  make test-pytest - Executar testes com pytest"
	@echo ""
	@echo "🔧 Ferramentas:"
	@echo "  make test-inspector - Testar com MCP Inspector"
	@echo "  make run-inspector  - Executar MCP Inspector localmente"
	@echo "  make install-inspector - Instalar MCP Inspector"
	@echo "  make install    - Instalar dependências"
	@echo "  make security   - Executar verificações de segurança"
	@echo "  make clean      - Limpar arquivos temporários"
	@echo "  make lint       - Verificar qualidade do código"
	@echo "  make format     - Formatar código"
	@echo ""
	@echo "🆘 Recuperação:"
	@echo "  make diagnostic      - Diagnóstico completo das APIs"
	@echo "  make recovery        - Recuperação automática"
	@echo "  make full-recovery   - Diagnóstico + recuperação"
	@echo "  make test-connection - Testar conectividade"
	@echo "  make status          - Verificar status dos serviços"
	@echo "  make restart-with-retry - Reiniciar com retry"
	@echo "  make auto-recovery   - Recuperação automática"
	@echo "  make reauth          - Reautenticar Spotify"

	@echo "  make help            - Mostrar esta ajuda"
