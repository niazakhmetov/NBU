# scripts/main_workflow.py

import os
from datetime import date
from requests.exceptions import RequestException

# Импорты модулей
from i18n import MESSAGES
from data_fetcher import fetch_rates_xml
from data_parser import parse_rates_xml
from qrcode_generator import generate_verification_url, generate_qr_base64

# ⚠️ ЗАГЛУШКА: Замените на реальную функцию content_generator
def generate_page(template_file, output_file, context):
    """Имитирует генерацию HTML-страницы с использованием Jinja2."""
    print(f"Файл {output_file} успешно сгенерирован (использован шаблон {template_file}).")


def run_workflow():
    print("--- Запуск автоматического обновления курсов ---")
    
    # 1. Получение и парсинг данных (без указания даты - получаем последние)
    course_data = None
    try:
        # Получаем данные на последнюю доступную дату
        xml_data = fetch_rates_xml()
        course_data = parse_rates_xml(xml_data)
        
        if not course_data or not course_data.get('rates'):
            raise ValueError("Парсер не вернул данных или список курсов пуст.")

        course_date = course_data['date']
        rates = course_data['rates']
        print(f"Данные успешно получены на {course_date}. Курсов обработано: {len(rates)}")

    except (RequestException, ValueError) as e:
        print(f"Критическая ошибка: Не удалось получить или обработать данные. {e}")
        print("--- Обновление завершено с ошибками: Нет данных курсов. Скрипт остановлен. ---")
        return

    # 2. Генерация глобального QR-кода для верификации даты
    global_verify_url = generate_verification_url(course_date)
    global_qr_code_base64 = generate_qr_base64(global_verify_url)
    print(f"Глобальный QR-код для верификации даты {course_date} сгенерирован.")
    
    # 3. Подготовка общего контекста для шаблонов
    base_context = {
        'MESSAGES': MESSAGES,
        'course_date': course_date,
        'global_qr_code_base64': global_qr_code_base64,
    }
    
    # 4. Генерация страниц
    
    # Контекст для Index (с ограниченным набором курсов, например, первые 8)
    index_context = {
        **base_context, 
        'rates': rates[:8], 
    }
    generate_page('index_template.html', 'index.html', index_context)

    # Контекст для About
    generate_page('about_template.html', 'about.html', base_context)

    # Контекст для Full Rates (Все курсы)
    full_rates_context = {
        **base_context,
        'rates': rates, 
    }
    # generate_page('full_rates_template.html', 'full_rates.html', full_rates_context)
    
    print("--- Обновление завершено успешно. ---")


if __name__ == "__main__":
    run_workflow()
