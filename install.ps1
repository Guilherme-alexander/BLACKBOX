# install.ps1 - Script de instalação do BLACKBOX Dropper (PowerShell)
# https://github.com/Guilherme-alexander

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║              BLACKBOX DROPPER - INSTALADOR               ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar se está rodando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[!] Execute como Administrador!" -ForegroundColor Red
    Write-Host "[*] Clique com botão direito e escolha 'Executar como administrador'" -ForegroundColor Yellow
    Read-Host "Pressione ENTER para sair"
    exit 1
}

Write-Host "[*] Verificando Python..." -ForegroundColor Yellow

# Verificar Python
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Host "[!] Python nao encontrado!" -ForegroundColor Red
    Write-Host "[*] Baixando Python 3.11..." -ForegroundColor Yellow
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    $pythonInstaller = "python-installer.exe"
    
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    
    Write-Host "[*] Instalando Python (aguarde)..." -ForegroundColor Yellow
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    
    Remove-Item $pythonInstaller -Force
    
    Write-Host "[✓] Python instalado!" -ForegroundColor Green
} else {
    Write-Host "[✓] Python ja esta instalado" -ForegroundColor Green
    python --version
}

Write-Host ""
Write-Host "[*] Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "[*] Instalando PyInstaller..." -ForegroundColor Yellow
python -m pip install pyinstaller

Write-Host ""
Write-Host "[*] Verificando instalacao..." -ForegroundColor Yellow
try {
    $version = python -c "import PyInstaller; print(PyInstaller.__version__)" 2>$null
    Write-Host "[✓] PyInstaller versao: $version" -ForegroundColor Green
} catch {
    Write-Host "[!] Erro ao verificar PyInstaller" -ForegroundColor Red
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║           [✓] INSTALAÇÃO CONCLUÍDA COM SUCESSO!          ║" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║  Para executar o BLACKBOX Dropper:                       ║" -ForegroundColor Green
Write-Host "║  python main.py                                          ║" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Read-Host "Pressione ENTER para sair"
