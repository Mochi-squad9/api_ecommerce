# -*- coding: utf-8 -*-

import sys
import requests
import json
from bs4 import BeautifulSoup

from flask import Flask, jsonify

app = Flask(__name__)

URL = 'https://www.kalunga.com.br/'
URL_PRODUCT = 'obterProdutoDetalhes/'
URL_BUY = 'depto/escolar/2?menuID=28'
AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}


@app.route('/')
def hello_world():
    return jsonify(arr_img)


client = requests.session()
s = requests.Session()
s.headers.update(AGENT)
r = s.get(URL + URL_BUY)


soup = BeautifulSoup(r.content, 'html.parser')

res = soup.find_all('picture')

arr_img = []

for each in res:
    img = each.img.get('data-src')
    if img != None:
        product_id = img.split('/')[-1].split('.')[0]
        r = s.get(URL + URL_PRODUCT + str(product_id) + "/")
        product = r.json()
        product['produto']['image'] = img
        arr_img.append(product['produto'])

if __name__ == "__main__":
    app.run()
