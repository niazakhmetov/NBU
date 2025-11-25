# scripts/data_fetcher.py
import requests
from zeep import Client
from zeep.exceptions import Fault
from datetime import datetime, timedelta

# --- Константы ---
WSDL_URL = 'https://nbportal.nationalbank.kz:443/WebService/NSI_NBRK?wsdl'
TARGET_GUIDE_CODE = 'NSI_NBRK_CRCY_COURSE'
DATE_FORMAT = '%Y-%m-%d'

def get_latest_exchange_rates():
    """Получает актуальный XML-ответ от SOAP-сервиса НБ РК."""
    client = Client(WSDL_URL)
    end_date = datetime.now()
    begin_date = end_date - timedelta(days=3)

    print("Подключение к SOAP-сервису НБ РК...")
    
    try:
        response = client.service.GET_GUIDE(
            guideCode=TARGET_GUIDE_CODE,
            type='FULL',
            beginDate=begin_date.strftime(DATE_FORMAT),
            endDate=end_date.strftime(DATE_FORMAT)
        )
    except Fault as e:
        print(f"SOAP Fault: {e}")
        return None

    if response.errCode != 0:
        print(f"Service Error: {response.errMsg}")
        return None

    print("Данные успешно получены.")
    return response.result

if __name__ == '__main__':
    # Пример использования для тестирования
    xml_data = get_latest_exchange_rates()
    if xml_data:
        print(f"Получено {len(xml_data)} байт XML-данных.")
