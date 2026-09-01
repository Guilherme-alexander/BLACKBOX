#!/bin/bash
# install.sh - Script de instalação do BLACKBOX Dropper (Linux)
# https://github.com/Guilherme-alexander

set -e  # Para a execução em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              BLACKBOX DROPPER - INSTALADOR               ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se é root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[!] Execute como root: sudo ./install.sh${NC}"
    exit 1
fi

echo -e "${GREEN}[*] Iniciando instalação do BLACKBOX Dropper...${NC}"

# 1. Atualizar sistema e instalar dependências
echo -e "${YELLOW}[1/6] Instalando dependências do sistema...${NC}"
sudo dpkg --add-architecture i386
sudo apt-get update -qq
sudo apt-get install -y -qq wine wine32 wine64 wget python3 python3-pip

# 2. Verificar Wine
echo -e "${YELLOW}[2/6] Configurando Wine...${NC}"
export WINEARCH=win32
export WINEPREFIX=/root/.wine

# 3. Baixar Python 2.7
echo -e "${YELLOW}[3/6] Baixando Python 2.7.18...${NC}"
if [ ! -f "python-2.7.18.msi" ]; then
    wget -q https://www.python.org/ftp/python/2.7.18/python-2.7.18.msi
else
    echo -e "${GREEN}[✓] Arquivo python-2.7.18.msi já existe${NC}"
fi

# 4. Instalar Python 2.7 no Wine
echo -e "${YELLOW}[4/6] Instalando Python 2.7 no Wine (pode demorar)...${NC}"
sudo wine msiexec /i python-2.7.18.msi /quiet /qn

# 5. Baixar e instalar pywin32
echo -e "${YELLOW}[5/6] Baixando e instalando pywin32...${NC}"
if [ ! -f "pywin32-220.win32-py2.7.exe" ]; then
    wget -q https://github.com/mhammond/pywin32/releases/download/b220/pywin32-220.win32-py2.7.exe
else
    echo -e "${GREEN}[✓] Arquivo pywin32-220.win32-py2.7.exe já existe${NC}"
fi

sudo wine pywin32-220.win32-py2.7.exe /quiet /qn

# 6. Instalar PyInstaller no Wine
echo -e "${YELLOW}[6/6] Instalando PyInstaller no Wine...${NC}"
sudo wine /root/.wine/drive_c/Python27/python.exe -m pip install pyinstaller

# 7. Instalar PyInstaller para Python 3 (sistema)
echo -e "${YELLOW}[6/6] Instalando PyInstaller para Python 3...${NC}"
pip3 install pyinstaller

# 8. Limpeza
echo -e "${YELLOW}[*] Limpando arquivos temporários...${NC}"
rm -f python-2.7.18.msi pywin32-220.win32-py2.7.exe

# 9. Verificação final
echo -e "${YELLOW}[*] Verificando instalação...${NC}"
echo -e "${GREEN}[✓] Python 3:${NC} $(python3 --version)"
echo -e "${GREEN}[✓] PyInstaller (Python 3):${NC} $(pip3 show pyinstaller | grep Version)"
echo -e "${GREEN}[✓] Wine:${NC} $(wine --version)"
echo -e "${GREEN}[✓] Python 2.7 (Wine):${NC} $(wine /root/.wine/drive_c/Python27/python.exe --version 2>&1)"
echo -e "${GREEN}[✓] PyInstaller (Wine):${NC} $(wine /root/.wine/drive_c/Python27/python.exe -c "import PyInstaller; print(PyInstaller.__version__)" 2>&1)"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║        [✓] INSTALAÇÃO CONCLUÍDA COM SUCESSO!             ║"
echo "║                                                          ║"
echo "║  Para executar o BLACKBOX Dropper:                       ║"
echo "║  sudo python3 main.py                                    ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
