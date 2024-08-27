import smtplib # biblioteca para enviar emails usando o protocolo smtp
from email.mime.multipart import MIMEMultipart # classe para manipular diferentes partes de uma mensagem email
from email.mime.text import MIMEText # classe para manipular diferentes partes de uma mensagem email
from email.mime.base import MIMEBase # classe para manipular diferentes partes de uma mensagem email
from email import encoders # classe para manipular diferentes partes de uma mensagem email
import os # biblioteca para interagir com o sistema operacional manipulando arquivos
import re
from tkinter import Tk, Label, Text, Button, filedialog # componentes para criar interfaces gráficas

totalArquivos = 0

# Função para enviar email com anexos
def enviaremailcomarquivos(email_remetente, senha_remetente, email_destinatario, assunto, body, arquivos):
    
    global totalArquivos
    
    smtp_server = 'smtp.gmail.com' # acessando o servidor do gmail
    smtp_port = 587 # acessando a porta

    msg = MIMEMultipart() # cria mensagem do tipo multipart
    msg['From'] = email_remetente # define o campo do email remetente
    msg['To'] = email_destinatario # define o campo do email destinatário
    msg['Subject'] = assunto # define o campo do assunto

    msg.attach(MIMEText(body, 'plain')) # anexa o corpo do email à mensagem como texto simples

    for caminho_do_arquivo in arquivos:
        filename = os.path.basename(caminho_do_arquivo) # define o nome do arquivo de acordo com o caminho
        print(f"Lendo o arquivo: {caminho_do_arquivo}")

        try:
            with open(caminho_do_arquivo, 'rb') as attachment: # tenta abrir o arquivo em binário
                part = MIMEBase('application', 'octet-stream') # cria uma parte MIME base para o anexo
                part.set_payload(attachment.read()) # define o payload (conteúdo) como o conteúdo do arquivo lido
                encoders.encode_base64(part) # codifica o payload em base64 (necessário para anexos em emails)
                part.add_header('Content-Disposition', f'attachment; filename={filename}') # adiciona um cabeçalho de disposição de conteúdo para indicar que é um anexo
                msg.attach(part) # adiciona a parte MIME ao email
                totalArquivos += 1
        except FileNotFoundError: # caso não consiga abrir o arquivo, exibe mensagem de erro
            print(f"Erro: Arquivo {caminho_do_arquivo} não encontrado.")
            continue

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server: # tenta enviar o email
            server.starttls() # usa TLS para segurança
            server.login(email_remetente, senha_remetente) # faz login no Gmail
            text = msg.as_string() # transforma a mensagem em tipo string
            server.sendmail(email_remetente, email_destinatario, text) # envia o email
            print(f'Email enviado com sucesso para {email_destinatario}')


    except Exception as e: # caso haja erros, imprime mensagem de falha
        print(f'Falha ao enviar email para {email_destinatario}: {e}')
    
# Função para enviar vários emails
def enviar_emails():
    email_remetente = 'silolencois@camda.com.br'
    senha_remetente = 'silosojalencois'
    assunto = 'COBRANÇA DE SERVIÇOS'
    body = message_text.get("1.0", "end-1c")

    emails_to_files = {}

    for caminho_do_arquivo in file_paths:
        filename = os.path.basename(caminho_do_arquivo)
        match = re.match(r'([a-zA-Z0-9]+)@([a-zA-Z]+\.\w+)_([a-zA-Z]+\d+)', filename) # usa uma expressão regular para extrair o email do nome do arquivo
        if match:
            part1 = match.group(1)
            part2 = match.group(2)

            email_destinatario = part1 + '@' + part2

            if email_destinatario not in emails_to_files:
                emails_to_files[email_destinatario] = []
            emails_to_files[email_destinatario].append(caminho_do_arquivo)
        else:
            print(f'Nome do arquivo {filename} não está no formato esperado.')

    for email, arquivos in emails_to_files.items():
        enviaremailcomarquivos(email_remetente, senha_remetente, email, assunto, body, arquivos)

    print(f'Foram enviados {totalArquivos} arquivos com sucesso')

# Função para adicionar arquivos
def add_files():
    files = filedialog.askopenfilenames()
    file_paths.extend(files)
    for file in files:
        print(f'Arquivo adicionado: {file}')

# Interface gráfica
root = Tk()
root.title("Enviar Emails com Anexos")
Label(root, text="Mensagem do Email:").pack()
message_text = Text(root, height=10, width=50)
message_text.pack()

Button(root, text="Adicionar Arquivos", command=add_files).pack()
Button(root, text="Enviar Emails", command=enviar_emails).pack()

file_paths = []

root.mainloop()
