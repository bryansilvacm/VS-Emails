import smtplib #biblioteca para enviar emails usando o protocolo smtp
from email.mime.multipart import MIMEMultipart #classe para manipular diferentes partes de uma mensagem email
from email.mime.text import MIMEText #classe para manipular diferentes partes de uma mensagem email
from email.mime.base import MIMEBase #classe para manipular diferentes partes de uma mensagem email
from email import encoders #classe para manipular diferentes partes de uma mensagem email
import os #biblioteca para interagir com o sistema operacional manipulando arquivos
import re
from tkinter import Tk, Label, Text, Button, filedialog #componentes para criar interfaces gráficas

#função para enviar email com anexo
def enviaremailcomarquivo(email_remetente, senha_remetente, email_destinatario, assunto, body, caminho_do_arquivo):
    smtp_server = 'smtp.gmail.com' #acessando o servidor do gmail
    smtp_port = 587 #acessando a porta

    msg = MIMEMultipart() #cria mensagem do tipo multipart
    msg['From'] = email_remetente #define o campo do email remetente
    msg['To'] = email_destinatario #define o campo do email destinatário
    msg['Subject'] = assunto #define o campo do assunto

    msg.attach(MIMEText(body, 'plain')) #anexa o corpo do email á mensagem como texto simples

    filename = os.path.basename(caminho_do_arquivo) #define o nome do arquivo de acordo com o caminho
    print(f"Lendo o arquivo: {caminho_do_arquivo}")

    try: 
        attachment = open(caminho_do_arquivo, 'rb') #tenta abrir o arquivo em binario
    except FileNotFoundError: #caso não consiga abri exibe mensagem de erro
        print(f"Erro: Arquivo {caminho_do_arquivo} não encontrado.")
        return
    
    part = MIMEBase('application', 'octet-stream') #cria uma parte MIME base para o anexo
    part.set_payload(attachment.read()) #define  o payload(conteúdo) como o conteúdo do arquivo lido
    encoders.encode_base64(part) #condifica o payload em base64 (que é necessário para anexos em emails)
    part.add_header('Content-Disposition', f'attachment; filename={filename}') #adiciona um cabeçalho de disposição de conteúdo para indicar que é um anexo
    msg.attach(part) #adiciona a parte MIME ao email
    attachment.close() #fecha o arquivo

    try:
        server = smtplib.SMTP(smtp_server, smtp_port) # tenta enviar o email
        server.starttls() #usa tls para segurança
        server.login(email_remetente, senha_remetente) #faz login no gmail
        text = msg.as_string() #transforma a mensagem em tipo string
        server.sendmail(email_remetente, email_destinatario, text) #envia o email
        print(f'Email enviado com sucesso para {email_destinatario}')
    except Exception as e: #caso haja erros imprime mensagem de falha
        print(f'Falha ao enviar email para {email_destinatario}: {e}')
    finally: 
        server.quit() #fecha a conexão com o servidor

#função para enviar vários emails

def enviar_emails():
    email_remetente = 'brayanaugusto2003@gmail.com'
    senha_remetente = 'xjrw iyjz vswk euro'
    assunto = 'COBRANÇA DE SERVIÇOS'
    body = message_text.get("1.0", "end-1c")

    for caminho_do_arquivo in file_paths: #para cada caminho de arquivo em filepaths vai definir os seguintes elementos 
        filename = os.path.basename(caminho_do_arquivo) #obtem o nome do arquico
        match = re.match(r'(.+?)_.+', filename) #usa uma expressão regular para extrair o email do nome do arquivo
        if match:
            email_destinatario = match.group(1)
            enviaremailcomarquivo(email_remetente, senha_remetente, email_destinatario, assunto, body, caminho_do_arquivo )
        # se o nome do arquico corresponder ao padrão esperado, chama a função enviaremailcomarquivo
        else:
            print(f'Nome do arquico {filename} não está no formato esperado.')

#função para adicionar arquivos
def add_files():
    files = filedialog.askopenfilenames()
    file_paths.extend(files)
    for file in files:
        print(f'Arquivo adicionado: {file}')
    
#inteface grafica
root = Tk()
root.title("Enviar Emails com Anexos")
Label(root, text="Mensagem do Email:").pack()
message_text= Text(root, height=10, width=50)
message_text.pack()

Button(root, text="Adicionar Arquivos", command=add_files).pack()
Button(root, text="Enviar Emails", command=enviar_emails).pack()

file_paths = []

root.mainloop()
