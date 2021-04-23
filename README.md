# vacina_fortaleza
Bot para verificar a listagem das pessoas a serem vacinadas em Fortaleza. 


1) Pacotes python usados:
=======================================
import requests
from bs4 import BeautifulSoup
import PyPDF2
import wget
import os
from datetime import datetime
=======================================

2) É utilizado um arquivo .txt para salvar a data da última checagem. Então antes de executar crie um arquivo "ultimo.txt" e passe no espaço de variáveis no script vacina.py

3) É possível enviar os alertas através de bot pelo aplicativo Telegram, caso queira utilizar, crie seu bot https://core.telegram.org/bots.
