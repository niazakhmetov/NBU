# scripts/main_workflow.py
import os
import sys

# Добавляем корневую директорию к PATH для импорта других модулей scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import data_fetcher
import data_parser
import content_generator

def main():
    """
    Основная логика: получение, парсинг и генерация файлов.
    """
    print("--- Запуск автоматического обновления курсов (Фаза 2) ---")
    
    # 1. Получение XML-данных
    xml_data = data_fetcher.get_latest_exchange_rates()
    
    if not xml_data:
        print("Не удалось получить XML-данные. Работа завершена.")
        return

    # 2. Парсинг данных
    all_rates = data_parser.parse_xml_data(xml_data)
    
    if not all_rates:
        print("Не удалось разобрать курсы валют. Работа завершена.")
        return

    # 3. Генерация контента
    content_generator.generate_json_api(all_rates)
    content_generator.generate_html_page(all_rates)
    
    print("--- Обновление завершено успешно! ---")


if __name__ == '__main__':
    main()
