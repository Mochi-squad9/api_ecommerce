# -*- coding: utf-8 -*-
import sys
import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def search():
    return jsonify(PRELOADED)


@app.route('/api/getProducts', methods=['POST'])
def getProducts():
    content = request.json
    product_list = []
    for each in content["cod"]:
        product_list.append(getProductDetail(each))
    return jsonify(product_list)


def initialSearch():
    s = connectContext()
    r = s.get(URL + URL_BUY)
    soup = BeautifulSoup(r.content, 'html.parser')
    res = soup.find_all('picture')
    product = []

    for each in res:
        img = each.img.get('data-src')
        if img != None:
            product_id = img.split('/')[-1].split('.')[0]
            product.append(getProductDetail(product_id))
    return product


def connectContext():
    client = requests.session()
    s = requests.Session()
    s.headers.update(AGENT)
    return s


def getProductDetail(cod):
    s = connectContext()
    r = s.get(URL + URL_PRODUCT + str(cod) + "/")
    product = r.json()
    product['produto']['image'] = "https://img.kalunga.com.br/fotosdeprodutos/" + str(cod) + ".jpg"
    return product['produto']


URL = 'https://www.kalunga.com.br/'
URL_PRODUCT = 'obterProdutoDetalhes/'
URL_BUY = 'depto/escolar/2?menuID=28'
AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
PRELOADED = initialSearch()

if __name__ == "__main__":
    app.run()
