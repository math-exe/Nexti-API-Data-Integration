# 👥 Nexti API Data Integration

Este repositório contém um conjunto de scripts em Python para integração de dados com a API da Nexti. A API da Nexti é usada para coletar informações de registro de ponto e outras informações relacionadas aos funcionários.

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter os seguintes requisitos instalados:

- Python 3.x
- Bibliotecas Python: pandas, requests, pyodbc

## ⚙️ Configuração

Antes de executar os scripts, é necessário configurar o arquivo `config.json` com as informações necessárias, como o `client_id`, `client_secret` e outras credenciais de autenticação.

## 🚀 Uso

Os scripts estão divididos em várias partes:

1. **api_requests.py**: Este script lida com as solicitações à API da Nexti para obter um token de acesso, dados de funcionários e registros de ponto.

2. **data_processing.py**: Este script processa os dados retornados pela API, formata datas e horários e prepara os dados para inserção em um banco de dados SQL Server.

3. **database.py**: Este script lida com a conexão ao banco de dados SQL Server e insere os dados formatados na tabela `NEXTI_CLOCKINGS`.

4. **main.py**: Este é o script principal que coordena todas as operações. Ele obtém um token de acesso, extrai os IDs externos dos funcionários, consulta a API da Nexti para obter registros de ponto e insere os dados no banco de dados.

## ▶️ Executando

Para executar o processo de integração de dados, simplesmente execute o script `main.py`:

```bash
python main.py
```
O script irá gerar registros de log no arquivo `log.txt` e inserir os dados na tabela `NEXTI_CLOCKINGS` do banco de dados SQL Server configurado.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar problemas ou solicitações de pull.

## 📜 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para obter detalhes.
