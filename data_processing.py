import os
import pandas as pd
from api_requests import get_csv_file_path
from datetime import date, datetime, timedelta

# Obter a data atual
today = date.today()

def map_clocking_fields(clocking):
    mapped_clocking = {
        'adjustmentDate': format_datetime_with_subtraction(clocking.get('adjustmentDate')),
        'adjustmentObservation': clocking.get('adjustmentObservation'),
        'adjustmentReasonExternalId': clocking.get('adjustmentReasonExternalId'),
        'adjustmentReasonId': clocking.get('adjustmentReasonId'),
        'clockingCollectorId': clocking.get('clockingCollectorId'),
        'clockingCollectorName': clocking.get('clockingCollectorName'),
        'clockingDate': format_datetime_with_subtraction(clocking.get('clockingDate')),
        'clockingOriginId': clocking.get('clockingOriginId'),
        'clockingTypeId': clocking.get('clockingTypeId'),
        'clockingTypeName': clocking.get('clockingTypeName'),
        'companyNumber': clocking.get('companyNumber'),
        'costCenter': clocking.get('costCenter'),
        'deviceCode': clocking.get('deviceCode'),
        'deviceDescription': clocking.get('deviceDescription'),
        'deviceId': clocking.get('deviceId'),
        'directionTypeId': clocking.get('directionTypeId'),
        'externalPersonId': clocking.get('externalPersonId'),
        'externalWorkplaceId': clocking.get('externalWorkplaceId'),
        'id': clocking.get('id'),
        'identificationMethodId': clocking.get('identificationMethodId'),
        'identificationMethodName': clocking.get('identificationMethodName'),
        'ip': clocking.get('ip'),
        'lastUpdate': format_datetime_with_subtraction(clocking.get('lastUpdate')),
        'latitude': clocking.get('latitude'),
        'longitude': clocking.get('longitude'),
        'online': clocking.get('online'),
        'personEmail': clocking.get('personEmail'),
        'personId': clocking.get('personId'),
        'personName': clocking.get('personName'),
        'personPIS': clocking.get('personPIS'),
        'personPhone': clocking.get('personPhone'),
        'photo': clocking.get('photo'),
        'referenceDate': format_datetime_with_subtraction(clocking.get('referenceDate')),
        'registerDate': format_datetime_with_subtraction(clocking.get('registerDate')),
        'removed': clocking.get('removed'),
        'ticketSignature': clocking.get('ticketSignature'),
        'timezone': clocking.get('timezone'),
        'userAdjustmentId': clocking.get('userAdjustmentId'),
        'workplaceCostCenter': clocking.get('workplaceCostCenter'),
        'workplaceId': clocking.get('workplaceId'),
        'workplaceTimezone': clocking.get('workplaceTimezone')
    }
    return mapped_clocking

def process_clockings_response(response):
    formatted_data = []

    for entry in response:
        clockings = entry.get('clockings', [])
        informations = entry.get('information', [])

        for clocking in clockings:
            formatted_clocking = map_clocking_fields(clocking)
            formatted_data.append(formatted_clocking)

        for information in informations:
            formatted_information = map_clocking_fields(information)
            formatted_data.append(formatted_information)

    return formatted_data

def extract_external_ids():
    csv_file_path = get_csv_file_path()  # Obtenha o caminho do arquivo CSV
    if os.path.exists(csv_file_path):
        df_persons = pd.read_csv(csv_file_path)
        external_ids = df_persons['externalId'].tolist()
        return external_ids
    else:
        print(f'O arquivo CSV {csv_file_path} não foi encontrado.')
        return []

# Função para formatar a data e hora com subtração de 3 horas (GMT-3, mas pode modificar como achar melhor)
def format_datetime_with_subtraction(datetime_str):
    if datetime_str:
        datetime_obj = datetime.strptime(datetime_str, '%d%m%Y%H%M%S')
        adjusted_datetime = datetime_obj - timedelta(hours=3)
        return adjusted_datetime.strftime('%d/%m/%Y %H:%M:%S')
    return ""

def get_periods(today):
    if today.day > 15:
        periodo1 = today.strftime("%m-%Y")
        periodo2 = str(int(periodo1[:2]) - 4).zfill(2) + periodo1[2:]
        periodo3 = str(int(periodo1[:2]) - 3).zfill(2) + periodo1[2:]
        periodo4 = str(int(periodo1[:2]) - 2).zfill(2) + periodo1[2:]
        periodo5 = str(int(periodo1[:2]) - 1).zfill(2) + periodo1[2:]
        periodo6 = str(int(periodo1[:2]) + 1).zfill(2) + periodo1[2:]
    else:
        periodo1 = today.strftime("%m-%Y")
        periodo2 = str(int(periodo1[:2]) - 5).zfill(2) + periodo1[2:]
        periodo3 = str(int(periodo1[:2]) - 4).zfill(2) + periodo1[2:]
        periodo4 = str(int(periodo1[:2]) - 3).zfill(2) + periodo1[2:]
        periodo5 = str(int(periodo1[:2]) - 2).zfill(2) + periodo1[2:]
        periodo6 = str(int(periodo1[:2]) - 1).zfill(2) + periodo1[2:]

    return {'periodo1': periodo1, 'periodo5': periodo5, 'periodo6': periodo6}
