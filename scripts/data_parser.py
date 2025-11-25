# scripts/data_parser.py
from lxml import etree
import math

def parse_xml_data(xml_data):
    """Разбирает XML-ответ и извлекает курсы валют."""
    if not xml_data:
        return {}

    root = etree.fromstring(xml_data.encode('utf-8'))
    ns_map = {'s': 'http://www.w3.org/2003/05/soap-envelope'}
    rates_data = {}
    
    entities = root.xpath('./s:Body/s:Entity', namespaces=ns_map)

    for entity in entities:
        try:
            custom = entity.xpath('./s:EntityCustom', namespaces=ns_map)[0]
        except IndexError:
            continue
        
        # Извлечение данных с учетом Namespaces
        try:
            curr_code = custom.xpath('./s:CurrCode', namespaces=ns_map)[0].text.strip()
            course_date_str = custom.xpath('./s:CourseDate', namespaces=ns_map)[0].text.strip()
            course_value_str = custom.xpath('./s:Course', namespaces=ns_map)[0].text.strip().replace(',', '.')
            corellation_value = int(custom.xpath('./s:Corellation', namespaces=ns_map)[0].text.strip())
        except (IndexError, AttributeError):
            print(f"Предупреждение: Пропущен неполный элемент курса.")
            continue
        
        # Расчет и преобразование
        try:
            course = float(course_value_str) / corellation_value
            # Округляем до 4 знаков после запятой
            course = round(course, 4)
        except ValueError:
            course = 0.0

        if curr_code == 'KZT':
            continue

        rates_data[curr_code] = {
            'code': curr_code,
            'course': course,
            'corellation': corellation_value,
            'course_date': course_date_str
        }
    
    print(f"Успешно разобрано {len(rates_data)} курсов валют.")
    return rates_data
