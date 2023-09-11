# main.py

import database
import api_requests
import data_processing
from datetime import date, datetime

# Obter a data atual
today = date.today()

def main():
    # Abra um arquivo para escrever as informações do log
    with open('log.txt', 'a') as log_file:

        # Obter token de acesso
        access_token = api_requests.get_access_token()

        # Extrair externalIds
        external_ids = data_processing.extract_external_ids()

        # Obter os últimos 6 períodos
        periods = data_processing.get_periods(today)

        # Consultar API para cada externalId e período
        for external_id in external_ids:
            for period in periods.values():
                log_entry = f"Consultando externalId: {external_id}, período: {period}, data e hora: {datetime.now()}"
                print(log_entry)  # Exiba no terminal
                log_file.write(log_entry + '\n')  # Escreva no arquivo de log

                # Verificar se o token de acesso está prestes a expirar (por exemplo, nos próximos 5 minutos)
                if api_requests.is_token_near_expiry(access_token, threshold_minutes=5):
                    print("O token de acesso está prestes a expirar. Gerando um novo token...")
                    access_token = api_requests.get_access_token()

                clockings_response = api_requests.get_clockings(access_token, external_id, period)
                
                if clockings_response is not None:  # Verifique se a resposta da API não é nula
                    formatted_data = data_processing.process_clockings_response(clockings_response)
                    
                    # Adicione 'external_id' e 'period' ao chamar a função
                    database.insert_data_to_sql(formatted_data, external_id, period)
                    
                    # Verifique o número de linhas retornadas
                    qtde_linhas = len(formatted_data)
                    log_result = f"Quantidade de linhas retornadas: {qtde_linhas}"
                    print(log_result)  # Exiba no terminal
                    log_file.write(log_result + '\n')  # Escreva no arquivo de log
                else:
                    print("Resposta da API está vazia ou nula. Verifique a chamada à API.")

if __name__ == "__main__":
    main()
