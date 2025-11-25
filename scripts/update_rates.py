import os
import requests
from zeep import Client
from zeep.exceptions import Fault
from lxml import etree
from datetime import datetime, timedelta
import json
from jinja2 import Environment, FileSystemLoader

# --- Константы и настройки ---
WSDL_URL = 'https://nbportal.nationalbank.kz:443/WebService/NSI_NBRK?wsdl'
TARGET_GUIDE_CODE = 'NSI_NBRK_CRCY_COURSE'
# Формат даты в SOAP-запросе: YYYY-MM-DD
DATE_FORMAT = '%Y-%m-%d'

# Основные валюты для главной страницы (Фаза 1.3)
MAIN_CURRENCIES = ['USD', 'EUR', 'RUB', 'AED', 'AMD', 'AUD', 'AZN', 'BRL', 'BYN', 'CAD']

# --- Основные функции ---

def get_latest_exchange_rates():
    """
    Получает актуальный справочник курсов валют из НБ РК за последние 3 дня.
    """
    client = Client(WSDL_URL)

    # Запрашиваем данные за короткий период
    end_date = datetime.now()
    begin_date = end_date - timedelta(days=3)

    try:
        # Формируем SOAP-запрос
        response = client.service.GET_GUIDE(
            guideCode=TARGET_GUIDE_CODE,
            type='FULL',
            beginDate=begin_date.strftime(DATE_FORMAT),
            endDate=end_date.strftime(DATE_FORMAT)
        )
    except Fault as e:
        print(f"SOAP Fault: {e}")
        return None

    # Проверка на ошибку в ответе сервиса
    if response.errCode != 0:
        print(f"Service Error: {response.errMsg}")
        return None

    # Результат - это строка с XML (CDATA)
    xml_data = response.result
    return xml_data


def parse_xml_data(xml_data):
    """
    Разбирает XML-ответ и извлекает курсы валют. (Исправлено для работы с Namespaces)
    """
    root = etree.fromstring(xml_data.encode('utf-8'))
    
    # Namespace для элементов Envelope и Body
    ns_map = {'s': 'http://www.w3.org/2003/05/soap-envelope'}
    
    # 1. Извлечение данных курсов
    rates_data = {}
    
    # Используем префикс s: для всех элементов, принадлежащих пространству имен.
    entities = root.xpath('./s:Body/s:Entity', namespaces=ns_map)

    # Перебираем все сущности (курсы)
    for entity in entities:
        # Получение пользовательских реквизитов 
        try:
            custom = entity.xpath('./s:EntityCustom', namespaces=ns_map)[0]
        except IndexError:
            continue
        
        # Извлечение данных
        curr_code = custom.xpath('./s:CurrCode', namespaces=ns_map)[0].text.strip()
        course_date_str = custom.xpath('./s:CourseDate', namespaces=ns_map)[0].text.strip()
        course_value_str = custom.xpath('./s:Course', namespaces=ns_map)[0].text.strip().replace(',', '.')
        corellation_value = int(custom.xpath('./s:Corellation', namespaces=ns_map)[0].text.strip())
        
        # Преобразование значений
        try:
            course = float(course_value_str) / corellation_value
        except ValueError:
            course = 0.0

        # Если валюта KZT (тенге), пропускаем ее
        if curr_code == 'KZT':
            continue

        # Сохраняем данные
        rates_data[curr_code] = {
            'code': curr_code,
            'course': course,
            'corellation': corellation_value,
            'course_date': course_date_str
        }
    
    return rates_data

# --- Функции для генерации контента ---

def generate_json_api(all_rates):
    """
    Генерирует и сохраняет файл api/latest.json (Фаза 1.2).
    """
    
    # Получаем дату курса из первого элемента
    first_rate = next(iter(all_rates.values()), None)
    course_date = first_rate['course_date'] if first_rate else datetime.now().strftime(DATE_FORMAT)

    # Форматирование данных для JSON
    json_output = {
        'metadata': {
            'source': 'National Bank of Kazakhstan (NSI_NBRK_CRCY_COURSE)',
            'updated_at': datetime.now().isoformat(), 
            'course_date': course_date 
        },
        'rates': all_rates
    }
    
    # Создаем папку api, если она не существует
    os.makedirs('api', exist_ok=True)
    
    # Сохраняем файл
    with open('api/latest.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=4)
    
    print("Файл api/latest.json успешно сгенерирован.")


def main():
    """
    Основная логика: получение, парсинг, фильтрация и генерация файлов.
    """
    print("Запуск скрипта обновления курсов...")
    
    xml_data = get_latest_exchange_rates()
    
    if not xml_data:
        print("Не удалось получить XML-данные. Работа завершена.")
        return

    all_rates = parse_xml_data(xml_data)
    
    if not all_rates:
        print("Не удалось разобрать курсы валют. Работа завершена.")
        return

    # 1.2. Создание JSON API
    generate_json_api(all_rates)
    
    # 1.3. Фильтрация для главной страницы
    main_rates = {
        code: data for code, data in all_rates.items() if code in MAIN_CURRENCIES
    }
    
    # 1.1. Получение даты курса для отображения
    first_rate = next(iter(all_rates.values()))
    course_date_str = first_rate['course_date']
    
    # Контекст для Jinja2
    context = {
        'rates': main_rates.values(),
        'course_date': course_date_str
    }
    
    # Генерация index.html
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    
    template = env.get_template('index_template.html')
    output = template.render(context)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print("Файл index.html успешно обновлен.")


if __name__ == '__main__':
    main()
