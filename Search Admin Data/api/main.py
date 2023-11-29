from flask import Flask, url_for, render_template, request, flash
import requests
import re
import json
from json import dumps


class Cnpj:
    def __init__(self, cnpj):
        self.cnpj = cnpj

    def eh_cnpj(self):
        if len(self.cnpj) == 14:
            return True
        else:
            return False

app = Flask(__name__)

app.config['SECRET_KEY'] = "teset"

@app.route('/robots.txt', methods=['POST', 'GET'])
def robots():    
    return render_template('robots.txt')

@app.route('/', methods=['POST', 'GET'])
def index():    
    return render_template('home.html')

@app.route('/consulta', methods=['POST', 'GET'])
def consulta():

    entrada_cnpj = request.form['cnpj']
    entrada_cnpj = re.sub('[../-]', '', entrada_cnpj)
    entrada_cnpj = Cnpj(entrada_cnpj)

    if len(entrada_cnpj.cnpj) == 14:
        request_cnpj = requests.get('https://receitaws.com.br/v1/cnpj/{}'.format(entrada_cnpj.cnpj))

        status_api = request_cnpj.text
        print(status_api)
        erro_muitas_requisicoes = "CNPJ inválido" 
        if erro_muitas_requisicoes in status_api:
            flash("CNPJ inválido!")
            return render_template('index.html')
        if status_api == "Too many requests, please try again later.":
            flash("Muitas requisições solicitadas, tente novamente dentro do período de 1 minuto")
            return render_template('index.html')

        consulta_data = request_cnpj.json()
        # Cartão CNPJ
        cnpj = consulta_data['cnpj']
        nome = consulta_data['nome']
        fantasia = consulta_data['fantasia']
        tipo = consulta_data['tipo']
        if tipo == 'MATRIZ':
            tipo = 'Matriz'
        atividade_principal = consulta_data['atividade_principal']
        atividade_principal_texto = atividade_principal[0]['text']

        abertura = str(consulta_data['abertura'])
        status = str(consulta_data['status'])
        situacao = str(consulta_data['situacao'])
        if situacao == 'ATIVA':
            situacao = 'Ativa'
        ult = consulta_data['ultima_atualizacao']
        natureza = consulta_data['natureza_juridica']
        capital = str(consulta_data['capital_social'])
        porte = str(consulta_data['porte'])
        if porte == 'DEMAIS':
            porte = 'Demais'

        tel = consulta_data['telefone']
        email = consulta_data['email']

        presidente = consulta_data['qsa']
        if len(presidente) == 0:
            presidente = "Não possui"
        else:
            presidente = presidente[0]['nome']

        # ENDEREÇO
        cep = consulta_data['cep']
        logradouro = consulta_data['logradouro']
        complemento = consulta_data['complemento']
        bairro = consulta_data['bairro']
        municipio = consulta_data['municipio']
        estado = consulta_data['uf']
        numero = consulta_data['numero']

        return render_template('index.html', cnpj_empresa=cnpj, nome_empresa=nome,nome_fantasia=fantasia,
                                tipo_empresa=tipo ,atividade_principal=atividade_principal_texto,
                                abertura_empresa=abertura.lower(), status_empresa=status.lower(), situacao_empresa=situacao,
                                capital_empresa=capital.lower(), porte_empresa=porte, presidente_empresa=presidente, cep_empresa=cep,
                                logradouro_empresa=logradouro, compremento_empresa=complemento, bairro_empresa=bairro, cidade_empresa=municipio,
                                estado_empresa=estado, natureza_empresa=natureza, ultima_atualizacao=ult[:10], numero_empresa=numero, tel_empresa=tel, email_empresa=email)
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)