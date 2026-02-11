@echo off
cls
echo ==========================================
echo   Cacador de Precos - Instalacao
echo ==========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale Python primeiro:
    echo 1. Va em: https://www.python.org/downloads/
    echo 2. Baixe a versao mais recente
    echo 3. IMPORTANTE: Marque "Add Python to PATH"
    echo 4. Execute este instalador novamente
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

REM Instalar dependencias
echo Instalando dependencias...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na instalacao
    echo.
    echo Tente:
    echo   pip install --upgrade pip
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   INSTALACAO CONCLUIDA!
echo ==========================================
echo.
echo Para executar o app:
echo   - Clique duas vezes em: run.bat
echo   - Ou execute: python main.py
echo.
echo (Opcional) Configure Google Shopping:
echo   1. Execute o app
echo   2. Va em Configuracoes
echo   3. Cole sua chave da SerpAPI
echo.
pause
