# scripts/data_fetcher.py

import requests
import json 
from datetime import datetime, date, timedelta, time # Добавлены datetime, timedelta, time
from requests.exceptions import RequestException
from zoneinfo import ZoneInfo # Используем для работы с часовыми поясами (Python 3.9+)

# --- КОНСТАНТЫ ЧАСОВОГО ПОЯСА И ПРАВИЛ НБК ---
# Официальный часовой пояс Казахстана (Астана)
ASTANA_TZ = ZoneInfo("Asia/Almaty") 
# Официальное время отсечки (после которого курс на следующий день уже утвержден)
# Устанавливаем 17:00 KZT, чтобы дать НБК запас времени после 15:30.
CUTOFF_TIME = time(hour=17, minute=0, second=0)


def fetch_rates_xml(fdate: str = None) -> str:
    """
    Получает сырой XML-ответ с курсами валют НБ РК.

    Если дата не указана (fdate=None), функция автоматически определяет целевую дату
    (сегодня или завтра) на основе текущего времени в Астане (17:00 KZT).
    
    Args:
        fdate (str, optional): Дата в формате 'DD.MM.YYYY'. 
                               Если None, используется логика смещения даты.

    Returns:
        str: Сырой XML-ответ от сервиса.

    Raises:
        RequestException: Если произошла ошибка при запросе (таймаут, ошибка HTTP) 
                          или API вернул некорректный ответ.
    """
    
    BASE_URL = "https://nationalbank.kz/rss/get_rates.cfm"
    
    if fdate is None:
        # 1. Определяем текущее время в часовом поясе Астаны
        now_astana = datetime.now(ASTANA_TZ)
        
        # 2. Сравниваем текущее время с временем отсечки (17:00 KZT)
        # Если время now_astana больше или равно 17:00: запрашиваем курс на ЗАВТРА.
        if now_astana.time() >= CUTOFF_TIME:
            target_date = now_astana.date() + timedelta(days=1)
            print(f"Текущее время ({now_astana.strftime('%H:%M')} KZT) после {CUTOFF_TIME}. Запрашиваем курс на ЗАВТРА.")
        else:
            # Иначе: запрашиваем курс на СЕГОДНЯ.
            target_date = now_astana.date()
            print(f"Текущее время ({now_astana.strftime('%H:%M')} KZT) до {CUTOFF_TIME}. Запрашиваем курс на СЕГОДНЯ.")
            
        # 3. Форматируем целевую дату для запроса
        fdate = target_date.strftime("%d.%m.%Y")
    
    # Теперь params['fdate'] всегда содержит дату, определенную логикой или пользователем
    params = {'fdate': fdate}
    
    TIMEOUT = 15
    
    print(f"Подключение к сервису НБ РК (Целевая дата: {fdate})...")

    try:
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status() 

        # ⭐ ИСПРАВЛЕНИЕ 2: Проверка на JSON-ответ с ошибкой
        raw_text = response.text.strip()
        if raw_text.startswith('{') and raw_text.endswith('}'):
            try:
                error_json = json.loads(raw_text)
                if 'message' in error_json:
                    error_msg = f"API Ошибка: {error_json['message']} (Code: {error_json.get('code', 'N/A')})"
                    raise RequestException(f"Некорректный ответ от API: {error_msg}")
            except json.JSONDecodeError:
                pass
        
        # НБ РК часто использует кодировку 'windows-1251', установим ее, если не определена
        if response.apparent_encoding.lower() not in ['utf-8', 'windows-1251', 'cp1251']:
            response.encoding = 'windows-1251'
        
        return response.text
        
    except RequestException as e:
        print(f"Ошибка при запросе к сервису: {e}")
        raise
