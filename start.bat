@echo off
REM Script para iniciar o Sistema Simples com Docker (Windows)

echo ==================================================
echo Sistema Simples - Iniciando Aplicacao
echo ==================================================

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Docker nao esta instalado.
    pause
    exit /b 1
)

REM Verificar se Docker Compose está instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Docker Compose nao esta instalado.
    pause
    exit /b 1
)

REM Build e inicie os containers
echo.
echo Construindo e iniciando containers...
docker-compose up -d

REM Aguardar inicialização
echo.
echo Aguardando inicializacao do PostgreSQL...
timeout /t 10

REM Informações
echo.
echo ==================================================
echo Sistema Simples - PRONTO PARA USAR
echo ==================================================
echo.
echo Acessar a aplicacao:
echo   Frontend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Banco de Dados:
echo   Host: localhost:5432
echo   Usuario: postgres
echo   Senha: postgres
echo   Database: sistema_simples
echo.
echo Para parar a aplicacao:
echo   docker-compose down
echo.
echo Ver logs:
echo   docker-compose logs -f backend
echo   docker-compose logs -f postgres
echo.
echo ==================================================
echo.
pause
