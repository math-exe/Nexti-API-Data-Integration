import os
import json
import time
import logging
import requests
import pandas as pd
from time import sleep
from datetime import datetime
from requests.exceptions import RequestException

def get_csv_file_path():
    output_path = r'\output'
    csv_file_path = os.path.join(output_path, 'persons.csv')
    return csv_file_path

# Configurar o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_access_token():
    # Carrega as configurações do arquivo config.json
    with open('config.json') as config_file:
        config = json.load(config_file)

    # Verifica se já existe um token de acesso armazenado e sua data de expiração
    access_token = config.get('access_token')
    token_expiration = config.get('token_expiration')

    if access_token and token_expiration and time.time() < token_expiration:
        return access_token

    token_url = "https://api.nexti.com/security/oauth/token"

    # Parâmetros da solicitação
    params = {
        "grant_type": config['grant_type'],
        "client_id": config['client_id'],
        "client_secret": config['client_secret']
    }

    # Cabeçalhos da solicitação
    headers = {
        "Content-Type": config["Content-Type"],
        "Authorization": config["Authorization"]
    }

    try:
        # Realizar a solicitação para obter o token de acesso
        response = requests.post(token_url, params=params, headers=headers)
        response.raise_for_status()  # Lança um erro se a solicitação não for bem-sucedida

        # Extrai o token de acesso da resposta
        token_data = response.json()
        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in')

        if access_token and expires_in:
            # Armazena o novo token de acesso e seu tempo de expiração
            config['access_token'] = access_token
            config['token_expiration'] = time.time() + expires_in

            with open('config.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)

        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter o token de acesso: {e}")
        return None

def get_employee_table(access_token):
    url = 'https://api.nexti.com/persons/all'

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "filter": "",
        "page": 0,
        "size": 150000
    }

    output_path = 'output'
    csv_file_path = os.path.join(output_path, 'persons.csv')

    if os.path.exists(csv_file_path):
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(csv_file_path))
        current_date = datetime.now().date()

        if file_modified_time.date() == current_date:
            df_persons = pd.read_csv(csv_file_path)
            return df_persons

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # Extrair os dados da resposta da API
        data = response.json().get("content")
        # Criar o DataFrame com os dados
        employee_table = pd.DataFrame(data)
        employee_table.to_csv(csv_file_path, index=False)
        if 'externalId' in employee_table.columns:
                external_ids = employee_table['externalId'].tolist()
                return external_ids
    else:
        # Erro na solicitação
        print('Erro na solicitação:', response.status_code)
        return None

def get_clockings(acess_token, externalId, period, max_retries=3, backoff_factor=2):
    retry = 0

    while retry < max_retries:
        try:
            headers = {
                "Authorization": f"Bearer {acess_token}"
            }

            url = f'https://api.nexti.com/clockings/person/externalid/{externalId}/period/{period}'
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            clockings_response = response.json()
            return clockings_response
        except RequestException as e:
            logging.warning(f"Tentativa {retry + 1} - Erro: {e}")
            retry += 1
            sleep(backoff_factor * retry)  # Backoff entre as tentativas
    return None
