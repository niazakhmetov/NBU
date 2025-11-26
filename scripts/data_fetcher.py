# scripts/data_fetcher.py

import requests
from requests.exceptions import RequestException

def fetch_rates_xml(fdate: str = None) -> str:
    """
    Получает сырой XML-ответ с курсами валют НБ РК.

    Используется URL-сервис с параметром даты, который позволяет
    получать курсы на любую историческую дату.

    Args:
        fdate (str, optional): Дата в формате 'DD.MM.YYYY'. 
                               Если None, сервис вернет курсы на последнюю доступную дату.

    Returns:
        str: Сырой XML-ответ от сервиса.

    Raises:
        RequestException: Если произошла ошибка при запросе (таймаут, ошибка HTTP).
    """
    
    # 🟢 Используем HTTPS и URL-сервис, указанный в документации
    BASE_URL = "https://nationalbank.kz/rss/get_rates.cfm"
    
    params = {}
    if fdate:
        # Дата должна быть в формате день.месяц.год
        params['fdate'] = fdate
    
    TIMEOUT = 15 # Установим разумный таймаут
    
    print(f"Подключение к сервису НБ РК (Дата: {fdate or 'Последняя доступная'})...")

    try:
        # Успешно решает проблему с HTTPConnectionPool: Max retries, используя HTTPS
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status() # Вызывает исключение для 4xx/5xx ошибок

        # НБ РК часто использует кодировку 'windows-1251', установим ее, если не определена
        if response.apparent_encoding.lower() not in ['utf-8', 'windows-1251', 'cp1251']:
            response.encoding = 'windows-1251' 
        
        return response.text
        
    except RequestException as e:
        print(f"Ошибка при запросе к сервису: {e}")
        raise
