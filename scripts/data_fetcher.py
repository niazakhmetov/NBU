# scripts/data_fetcher.py
import requests
import datetime

# --- Константы SOAP-сервиса НБ РК ---
SOAP_URL = "http://www.nationalbank.kz/rss/get_rates"
SOAP_HEADERS = {'Content-Type': 'text/xml; charset=utf-8'}
SOAP_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <get_rates xmlns="http://nationalbank.kz/">
      <date>{date}</date>
    </get_rates>
  </soap:Body>
</soap:Envelope>"""


def fetch_xml_data():
    """
    Запрашивает актуальные курсы валют у SOAP-сервиса НБ РК.
    Возвращает XML-ответ в виде строки или None при ошибке.
    """
    # Форматируем текущую дату в требуемом формате YYYY-MM-DD
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    soap_body = SOAP_TEMPLATE.format(date=today)
    
    try:
        # ⚠️ ИСПРАВЛЕНИЕ: Добавлен явный таймаут (10 секунд)
        response = requests.post(
            SOAP_URL, 
            headers=SOAP_HEADERS, 
            data=soap_body.encode('utf-8'),
            timeout=10 
        )
        response.raise_for_status() # Вызывает исключение для плохих ответов (4xx или 5xx)
        
        # Так как это просто получение XML, мы возвращаем его для дальнейшего парсинга
        return response.text
        
    except requests.exceptions.RequestException as e:
        # Вывод ошибки в лог, чтобы видеть, что пошло не так
        print(f"Ошибка при запросе к SOAP-сервису: {e}")
        # При ошибке возвращаем None
        return None
