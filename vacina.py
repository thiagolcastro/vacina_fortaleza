#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import PyPDF2
import wget
import os
from datetime import datetime

#declaracao de variaveis

#pessoas que o script deve checar se exitem na listagem. 
# OBS: O espaço entro os sobrenomes deve ser representado com '€' como mostrado no exemplo abaixo
pessoas = ['CHICO€LINGUICA€DA€SILVA','MOZO€DO€NASCIMENTO€PEREIRA','CABECA€DE€CEBOLA']

#caminho completo de um arquivo .txt que vai armazenar a ultima data de checagem
arquivo_ultima_data = '/tmp/ultimo.txt'

#Caso queira usar o telegram para enviar alertas, passe os valores do seu bot
bot_token = 'SEU TOKEN'
bot_chatID = 'SEU ID'
########### FIM DE DECLARACAO



def baixar_arquivo(url):
    #Baixando arquivo do site
    arquivo = wget.download(url)
    return str(arquivo)

def procura_link_download():
    url = "https://vacineja.sepog.fortaleza.ce.gov.br/relatorios/lista_agendamentos"
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')

    contador = 0
    for a in soup.find_all('a',target="_blank",href=True):
        if contador == 1:# Pegar  o ultimo arquivo
            #print ('https://vacineja.sepog.fortaleza.ce.gov.br'+a['href'],a.get_text())
            nome_arquivo = baixar_arquivo('https://vacineja.sepog.fortaleza.ce.gov.br'+a['href'])
            print(nome_arquivo)
            buscar_nome_pdf(nome_arquivo,a.get_text())
        contador += 1

def buscar_nome_pdf(arquivo_pdf,data_arquivo):
    global pessoas
    global arquivo_ultima_data
    read_pdf = PyPDF2.PdfFileReader(arquivo_pdf,'rb')
    numero_paginas = read_pdf.getNumPages()
    contador_paginas = 0
    mensagem = ''

    arquivo = open(arquivo_ultima_data, "r")
    ultima_data = (arquivo.readline(10))
    arquivo.close()

    ultima_data_conv = datetime.strptime(ultima_data, '%d/%m/%Y').date()
    data_arquivo_conv = datetime.strptime(data_arquivo[-10::], '%d/%m/%Y').date()

    print(ultima_data_conv)
    print(data_arquivo_conv)
    #Verifica se foi adicionado um novo ar:quivo no site
    if ultima_data_conv != data_arquivo_conv:
        mensagem = 'Novo arquivo com lista de vacinacao inserido! \n '+ data_arquivo[-10::]
        arquivo = open(arquivo_ultima_data, "w")
        arquivo.write(data_arquivo[-10::])
        arquivo.close()

        print('Novo arquivo de vacina encontrado. Verificando lista de pessoas...')
        while contador_paginas < numero_paginas:
            p = read_pdf.getPage(contador_paginas)
            text = p.extractText()
            #print('Verificando página'+str(contador_paginas))

            for x in pessoas:
                if text.find(x) >= 0:
                    #print (x.replace('€',' ')+' - Encontrado na Lista - pagina',contador_paginas+1)
                    mensagem = mensagem + x.replace('€',' ')+' - Encontrado na Lista - pagina'+ str(contador_paginas+1) + '\n'
            contador_paginas += 1

        mensagem = mensagem + '\n'
    else:
        mensagem = 'Nenhum arquivo novo. Ultima data:'+data_arquivo[-10::]

    os.remove(arquivo_pdf)
    telegram_bot_sendtext(mensagem)
    print(mensagem)

def telegram_bot_sendtext(bot_message):

    global bot_token
    global bot_chatID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    
 
    
# Inicio da execucao do programa

print ("Iniciando programa")

#Lista de pessoas para buscar a vacina
procura_link_download()
