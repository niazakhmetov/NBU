# scripts/main_workflow.py

import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем все необходимые модули
from scripts.data_fetcher import fetch_xml_data
from scripts.data_parser import parse_xml_data
from scripts.content_generator import generate_json_api, generate_html_page, generate_about_page # НОВЫЙ ИМПОРТ

print("--- Запуск автоматического обновления курсов (Фаза 2) ---")

try:
    # 1. Загрузка данных
    print("Подключение к SOAP-сервису НБ РК...")
    xml_data = fetch_xml_data()
    print("Данные успешно получены.")

    # 2. Парсинг данных
    all_rates = parse_xml_data(xml_data)

    # 3. Генерация выходных файлов
    
    # 3.1 Генерация API (latest.json)
    generate_json_api(all_rates)
    
    # 3.2 Генерация главной страницы (index.html)
    generate_html_page(all_rates)
    
    # 3.3 Генерация страницы "О платформе" (about.html) (НОВЫЙ ВЫЗОВ)
    generate_about_page()

    print("--- Обновление завершено успешно! ---")

except Exception as e:
    print(f"Критическая ошибка Workflow: {e}")
