import pyodbc
import json

def connect_to_database():
    with open('config.json') as config_file:
        config = json.load(config_file)

    server = config['server']
    database = config['database']
    user_db = config['user_db']
    password_db = config['password_db']
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'f'Server={server};Database={database};UID={user_db};PWD={password_db}')

    return connection

def insert_data_to_sql(data, external_id, period):
    # Insere os dados formatados na tabela SQL Server
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        for row in data:
            # Adicione 'externalId' e 'period' aos dados
            row['externalId'] = external_id
            row['period'] = period

            columns = [
                "externalId", "period", "adjustmentDate", "adjustmentObservation",
                "adjustmentReasonExternalId", "adjustmentReasonId", "clockingCollectorId",
                "clockingCollectorName", "clockingDate", "clockingOriginId",
                "clockingTypeId", "clockingTypeName", "companyNumber", "costCenter",
                "deviceCode", "deviceDescription", "deviceId", "directionTypeId",
                "externalPersonId", "externalWorkplaceId", "id", "identificationMethodId",
                "identificationMethodName", "ip", "lastUpdate", "latitude", "longitude",
                "online", "personEmail", "personId", "personName", "personPIS",
                "personPhone", "photo", "referenceDate", "registerDate", "removed",
                "ticketSignature", "timezone", "userAdjustmentId", "workplaceCostCenter",
                "workplaceId", "workplaceTimezone"
            ]
            
            query = f"INSERT INTO NEXTI_CLOCKINGS ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            
            values = [row[column] for column in columns]

            # Executar a query SQL
            cursor.execute(query, values)

        connection.commit()

    except pyodbc.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
    finally:
        cursor.close()
        connection.close()
