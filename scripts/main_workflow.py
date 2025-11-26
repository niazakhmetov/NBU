# scripts/main_workflow.py

import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем все необходимые модули
from scripts.data_fetcher import fetch_xml_data
from scripts.data_parser import parse_xml_data
from scripts.content_generator import generate_json_api, generate_html_page, generate_about_page

print("--- Запуск автоматического обновления курсов (Фаза 2) ---")

try:
    # 1. Загрузка данных
    print("Подключение к SOAP-сервису НБ РК...")
    xml_data = fetch_xml_data()
    
    # ⚠️ КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ 1: Проверка наличия XML данных
    if not xml_data:
        # Если данные пусты, генерируем статическую страницу, но пропускаем генерацию курсов
        print("Критическая ошибка: Не удалось получить XML-данные. Пропускаем генерацию курсов.")
        generate_about_page() # Генерируем about.html (он не зависит от данных)
        raise Exception("Нет данных курсов для продолжения. Скрипт остановлен.")
    
    print("Данные успешно получены.")

    # 2. Парсинг данных
    all_rates = parse_xml_data(xml_data)
    
    # ⚠️ КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ 2: Проверка, что парсинг дал результаты
    if not all_rates:
        print("Критическая ошибка: Данные получены, но парсинг вернул пустой список курсов. Пропускаем генерацию курсов.")
        generate_about_page()
        raise Exception("Курсы не были разобраны. Скрипт остановлен.")


    # 3. Генерация выходных файлов
    
    # 3.1 Генерация API (latest.json)
    generate_json_api(all_rates)
    
    # 3.2 Генерация главной страницы (index.html)
    generate_html_page(all_rates)
    
    # 3.3 Генерация страницы "О платформе" (about.html)
    generate_about_page()

    print("--- Обновление завершено успешно! ---")

# ⚠️ КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ 3: Более чистая обработка исключений
except Exception as e:
    # Обработка исключений, которые мы сами сгенерировали, чтобы не выводить полный Traceback
    if "Нет данных курсов для продолжения" in str(e) or "Курсы не были разобраны" in str(e):
        print(f"--- Обновление завершено с ошибками: {e} ---")
    else:
        # В случае других критических ошибок
        print(f"Критическая ошибка Workflow: {e}")
