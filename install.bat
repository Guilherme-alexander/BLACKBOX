@echo off
REM install.bat - Script de instalação do BLACKBOX Dropper (Windows)
REM https://github.com/Guilherme-alexander

title BLACKBOX Dropper - Instalador
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║             [!] BLACKBOX DROPPER - INSTALADOR            ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo [*] Verificando Python...

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python nao encontrado!
    echo.
    echo [*] Baixando Python 3.11...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile python-installer.exe"
    echo [*] Instalando Python (aguarde)...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo [✓] Python instalado!
) else (
    echo [✓] Python ja esta instalado
    python --version
)

echo.
echo [*] Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Instalando pip...
    python -m ensurepip --upgrade
) else (
    echo [✓] pip ja esta instalado
)

echo.
echo [*] Instalando PyInstaller...
python -m pip install --upgrade pip
python -m pip install pyinstaller

echo.
echo [*] Verificando instalação...
python -c "import PyInstaller; print('PyInstaller versao:', PyInstaller.__version__)" 2>nul
if %errorlevel% equ 0 (
    echo [✓] PyInstaller instalado com sucesso!
) else (
    echo [!] Erro ao instalar PyInstaller
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║           [✓] INSTALAÇÃO CONCLUÍDA COM SUCESSO!          ║
echo ║                                                          ║
echo ║  Para executar o BLACKBOX Dropper:                       ║
echo ║  python main.py                                          ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

pause
