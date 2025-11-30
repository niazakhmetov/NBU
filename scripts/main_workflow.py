# scripts/main_workflow.py

import os
import json
from datetime import datetime
from requests.exceptions import RequestException

# Импорты модулей платформы
from i18n import MESSAGES
from data_fetcher import fetch_rates_xml
from data_parser import parse_rates_xml
from qrcode_generator import generate_verification_url, generate_qr_base64
from content_generator import generate_page 


# --- Константы ---
# Список основных валют для отображения на главной странице (index.html)
MAIN_CURRENCIES = ['USD', 'EUR', 'RUB', 'GBP', 'JPY', 'CNY', 'AED', 'TRY', 'KGS', 'UZS'] 
# Формат времени для отображения на status.html
DATE_FORMAT_DISPLAY = '%H:%M:%S %d.%m.%Y' 


def generate_json_api_file(course_data: dict, rates: list):
    """
    Генерирует и сохраняет файл api/latest.json для машинного чтения.
    """
    # Преобразуем список rates в словарь с кодом валюты в качестве ключа
    rates_dict = {rate['code']: rate for rate in rates}
    
    json_output = {
        'metadata': {
            'source': 'National Bank of Kazakhstan (get_rates.cfm)',
            'updated_at': datetime.now().isoformat(),
            'course_date': course_data.get('date'),
        },
        'rates': rates_dict
    }
    
    # Создаем папку api, если она не существует
    os.makedirs('api', exist_ok=True)
    
    # Сохраняем файл
    with open('api/latest.json', 'w', encoding='utf-8') as f:
        # ensure_ascii=False для корректного отображения кириллицы
        json.dump(json_output, f, ensure_ascii=False, indent=4)
        
    print("Файл api/latest.json успешно сгенерирован.")


def load_fallback_data():
    """
    Загружает последние успешные официальные данные из api/latest.json в случае сбоя.
    Конвертирует словарь курсов обратно в список для совместимости с основной логикой.
    """
    try:
        with open('api/latest.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Конвертируем словарь курсов обратно в список
            rates_list = list(data['rates'].values())
            
            return {
                'course_date': data['metadata']['course_date'],
                'rates': rates_list
            }
    except FileNotFoundError:
        print("❌ Fallback: Файл кэша api/latest.json не найден. Невозможно использовать Fallback.")
        return None
    except Exception as e:
        print(f"❌ Fallback: Ошибка при чтении или парсинге файла кэша: {e}")
        return None


def run_workflow():
    print("--- Запуск автоматического обновления курсов ---")
    
    # Фиксируем время запуска и устанавливаем начальный статус
    last_updated_time = datetime.now().strftime(DATE_FORMAT_DISPLAY)
    system_status = "ERROR"  
    course_date = "N/A"
    rates = []
    global_qr_code_base64 = ""
    using_fallback = False # НОВАЯ ПЕРЕМЕННАЯ
    
    try:
        # 1. Получение и парсинг данных (ОСНОВНАЯ ЛОГИКА)
        # ⭐ ИСПРАВЛЕНИЕ КОММЕНТАРИЯ: Вызов без fdate теперь использует текущую системную дату 
        xml_data = fetch_rates_xml()  
        course_data = parse_rates_xml(xml_data)
        
        if not course_data or not course_data.get('rates'):
            raise ValueError("Парсер не вернул данных или список курсов пуст.")

        course_date = course_data['date']
        rates = course_data['rates']
        
        # Обновляем статус, если данные успешно получены
        system_status = "OK"
        print(f"✅ УСПЕХ: Данные успешно получены на {course_date}. Курсов обработано: {len(rates)}")

        # 2. Генерация глобального QR-кода для верификации даты
        global_verify_url = generate_verification_url(course_date)
        global_qr_code_base64 = generate_qr_base64(global_verify_url)
        print("QR-код сгенерирован.")
        
        # 3. Генерация JSON API (Сохраняем новые данные в кэш)
        generate_json_api_file(course_data, rates)
        
    except (RequestException, ValueError, Exception) as e:
        # --- ЛОГИКА FALLBACK (АВАРИЙНЫЙ КЭШ) ---
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: Не удалось получить или обработать данные. {e}")
        system_status = "ERROR" # Сохраняем статус ошибки
        
        # 1. Попытка загрузить кэш
        fallback_data = load_fallback_data()
        
        if fallback_data:
            # 2. Используем данные из кэша, но сохраняем статус ошибки
            course_date = fallback_data['course_date']
            rates = fallback_data['rates']
            using_fallback = True
            
            # 3. Перегенерируем QR-код, чтобы он ссылался на дату из кэша
            global_verify_url = generate_verification_url(course_date)
            global_qr_code_base64 = generate_qr_base64(global_verify_url)
            print(f"⭐ FALLBACK АКТИВИРОВАН: Отображаем курсы от {course_date}.")

    # --- 4. Подготовка общего контекста для Jinja2 ---
    
    # Фильтруем курсы для главной страницы (Top-10)
    # Если rates пуст (из-за ошибки и отсутствия кэша), main_rates будет пустым
    main_rates = [rate for rate in rates if rate['code'] in MAIN_CURRENCIES]
    
    # Общий контекст для всех страниц
    base_context = {
        # Данные для локализации и общие переменные
        'L': MESSAGES['ru'], 
        'MESSAGES': MESSAGES,
        'course_date': course_date,
        'global_qr_code_base64': global_qr_code_base64,
        'now': datetime.now, 
        
        # Данные для status.html
        'last_updated_time': last_updated_time,
        'system_status': system_status,
        'using_fallback': using_fallback, # НОВАЯ ПЕРЕМЕННАЯ ДЛЯ ИНДИКАЦИИ
        
        # Полный и отфильтрованный список курсов
        'rates': rates, 
        'main_rates': main_rates 
    }
    
    # --- 5. Генерация всех страниц (Координация) ---
    print("--- Начинаем генерацию HTML-страниц ---")
    
    try:
        # 5.1. Главная страница (index.html) - использует main_rates
        index_context = {**base_context, 'rates': main_rates}
        generate_page('index_template.html', 'index.html', index_context)

        # 5.2. Полный список курсов (full_rates.html) - использует полный список rates
        full_rates_context = {**base_context, 'rates': rates}
        generate_page('full_rates_template.html', 'full_rates.html', full_rates_context)

        # 5.3. О платформе (about.html)
        generate_page('about_template.html', 'about.html', base_context)

        # 5.4. Статус системы (status.html) - использует last_updated_time и system_status
        generate_page('status_template.html', 'status.html', base_context)
        
        # 5.5. Страница верификации (verify.html)
        generate_page('verify_template.html', 'verify.html', base_context)
        
    except Exception as e:
        print(f"❌ Критическая ошибка при генерации HTML: {e}")
        
    print("--- Генерация всех статических страниц завершена. ---")
    
    if system_status == "OK":
        print(f"--- Обновление завершено успешно на {last_updated_time}. ---")
    else:
        # Примечание: Это сообщение выводится, даже если Fallback был успешен,
        # так как основная цель - уведомить о сбое API НБК.
        print(f"--- Обновление завершено с ошибками. Статус: {system_status}. ---")


if __name__ == "__main__":
    run_workflow()
