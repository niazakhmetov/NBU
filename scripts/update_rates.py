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

# --- Функции ---

def get_latest_exchange_rates():
    """
    Получает актуальный справочник курсов валют из НБ РК за последние 3 дня.
    """
    client = Client(WSDL_URL)

    # Запрашиваем данные за короткий период, чтобы получить последний курс
    end_date = datetime.now()
    begin_date = end_date - timedelta(days=3)

    try:
        # Формируем SOAP-запрос
        response = client.service.GET_GUIDE(
            arg0={
                'beginDate': begin_date.strftime(DATE_FORMAT),
                'endDate': end_date.strftime(DATE_FORMAT),
                'guideCode': TARGET_GUIDE_CODE,
                # Используем FULL, чтобы получить все записи за период
                'type': 'FULL'
            }
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
    Разбирает XML-ответ и извлекает курсы валют.
    """
    root = etree.fromstring(xml_data.encode('utf-8'))
    
    # Namespace для элементов CommonInfo и Entity
    ns_map = {'s': 'http://www.w3.org/2003/05/soap-envelope'}
    
    # 1. Извлечение данных курсов
    rates_data = {}
    
    # XPath для Entity: /Envelope/Body/Entity
    entities = root.xpath('./s:Body/Entity', namespaces=ns_map)

    # Перебираем все сущности (курсы)
    for entity in entities:
        # Получение пользовательских реквизитов 
        custom = entity.xpath('./EntityCustom', namespaces=ns_map)[0]
        
        # Извлечение данных
        curr_code = custom.xpath('./CurrCode', namespaces=ns_map)[0].text.strip()
        
        # Строка, которая ранее вызывала ошибку:
        course_date_str = custom.xpath('./CourseDate', namespaces=ns_map)[0].text.strip()
        
        course_value_str = custom.xpath('./Course', namespaces=ns_map)[0].text.strip().replace(',', '.')
        corellation_value = int(custom.xpath('./Corellation', namespaces=ns_map)[0].text.strip())
        
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
            'course_date': course_date_str # (Фаза 1.1)
        }
    
    return rates_data

# --- Новые функции для Фазы 1 ---

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
            'updated_at': datetime.now().isoformat(), # Дата обновления самого файла
            'course_date': course_date # Дата установки курса
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
