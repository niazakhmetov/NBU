# scripts/content_generator.py
import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# --- Константы ---
DATE_FORMAT = '%Y-%m-%d'
MAIN_CURRENCIES = ['USD', 'EUR', 'RUB', 'AED', 'AMD', 'AUD', 'AZN', 'BRL', 'BYN', 'CAD']


def generate_json_api(all_rates):
    """Генерирует и сохраняет файл api/latest.json."""
    first_rate = next(iter(all_rates.values()), None)
    course_date = first_rate['course_date'] if first_rate else datetime.now().strftime(DATE_FORMAT)

    json_output = {
        'metadata': {
            'source': 'National Bank of Kazakhstan (NSI_NBRK_CRCY_COURSE)',
            'updated_at': datetime.now().isoformat(), 
            'course_date': course_date 
        },
        'rates': all_rates
    }
    
    os.makedirs('api', exist_ok=True)
    
    with open('api/latest.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=4)
    
    print("Файл api/latest.json успешно сгенерирован.")


def generate_html_page(all_rates):
    """Генерирует и сохраняет index.html с фильтрацией основных валют."""
    if not all_rates:
        print("Ошибка: Нет данных для генерации HTML.")
        return
        
    main_rates = {
        code: data for code, data in all_rates.items() if code in MAIN_CURRENCIES
    }
    
    first_rate = next(iter(all_rates.values()))
    course_date_str = first_rate['course_date']
    
    context = {
        'rates': main_rates.values(),
        'course_date': course_date_str
    }
    
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    
    try:
        template = env.get_template('index_template.html')
        output = template.render(context)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(output)
        
        print("Файл index.html успешно обновлен.")
    except Exception as e:
        print(f"Ошибка генерации index.html: {e}")
