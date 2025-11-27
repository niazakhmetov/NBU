# scripts/data_fetcher.py

import requests
import json # Добавлен для обработки JSON-ошибок
from requests.exceptions import RequestException
from datetime import date # Добавлен для получения текущей даты

def fetch_rates_xml(fdate: str = None) -> str:
    """
    Получает сырой XML-ответ с курсами валют НБ РК.

    Если дата не указана (fdate=None), функция автоматически использует текущую дату.
    
    Args:
        fdate (str, optional): Дата в формате 'DD.MM.YYYY'.
                               Если None, используется текущая системная дата.

    Returns:
        str: Сырой XML-ответ от сервиса.

    Raises:
        RequestException: Если произошла ошибка при запросе (таймаут, ошибка HTTP) 
                          или API вернул некорректный ответ.
    """
    
    BASE_URL = "https://nationalbank.kz/rss/get_rates.cfm"
    
    # ⭐ ИСПРАВЛЕНИЕ 1: Всегда передавать дату, используя текущую, если fdate=None.
    if fdate is None:
        fdate = date.today().strftime("%d.%m.%Y")
    
    # Теперь params['fdate'] всегда присутствует
    params = {'fdate': fdate}
    
    TIMEOUT = 15
    
    print(f"Подключение к сервису НБ РК (Дата: {fdate})...")

    try:
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status() # Вызывает исключение для 4xx/5xx ошибок

        # ⭐ ИСПРАВЛЕНИЕ 2: Проверка на JSON-ответ с ошибкой (Code: 500/Invalid format date)
        # Логи показали, что API возвращает JSON с ошибкой даже при статусе 200.
        raw_text = response.text.strip()
        if raw_text.startswith('{') and raw_text.endswith('}'):
            try:
                error_json = json.loads(raw_text)
                if 'message' in error_json:
                    # Если найдено JSON-сообщение об ошибке, вызываем исключение, 
                    # которое main_workflow.py сможет обработать как сбой получения данных.
                    error_msg = f"API Ошибка: {error_json['message']} (Code: {error_json.get('code', 'N/A')})"
                    raise RequestException(f"Некорректный ответ от API: {error_msg}")
            except json.JSONDecodeError:
                # Если это был не валидный JSON, игнорируем и предполагаем, что это XML.
                pass
        
        # НБ РК часто использует кодировку 'windows-1251', установим ее, если не определена
        if response.apparent_encoding.lower() not in ['utf-8', 'windows-1251', 'cp1251']:
            response.encoding = 'windows-1251'
        
        return response.text
        
    except RequestException as e:
        print(f"Ошибка при запросе к сервису: {e}")
        # Передаем исключение наверх
        raise
