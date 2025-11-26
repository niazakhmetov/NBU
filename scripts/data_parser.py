# scripts/data_parser.py

import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

def parse_rates_xml(xml_data: str) -> Optional[Dict]:
    """
    Парсит XML-данные курсов валют НБ РК.

    Извлекает дату курсов и список валют с их полным именем, курсом и изменением.

    Args:
        xml_data (str): Сырой XML-ответ от сервиса НБ РК.

    Returns:
        Optional[Dict]: Словарь с ключами 'date' (str) и 'rates' (List[Dict]),
                        или None в случае ошибки парсинга.
    """
    
    rates_list: List[Dict] = []
    
    try:
        # ET.fromstring автоматически обрабатывает кодировку, 
        # но лучше, если requests предоставил корректную строку.
        root = ET.fromstring(xml_data)
        
        # 1. Извлечение даты из корневого элемента <rates date="DD.MM.YYYY">
        course_date = root.get('date')
        if not course_date:
            print("Ошибка парсинга: Не найдена дата курсов в корневом элементе.")
            return None

        # 2. Парсинг каждого элемента <item>
        for item in root.findall('item'):
            try:
                # Извлечение текста элементов
                code = item.find('title').text
                rate_str = item.find('rate').text
                quant_str = item.find('quant').text
                change_str = item.find('change').text
                
                # Дополнительные поля
                full_name = item.find('fullname').text if item.find('fullname') is not None else code
                index = item.find('index').text if item.find('index') is not None else 'NO'

                # Преобразование в числа. Используем replace(',', '.') 
                # для надежного парсинга чисел
                course = float(rate_str.replace(',', '.'))
                quant = int(quant_str)
                change = float(change_str.replace(',', '.')) if change_str else 0.0

                rates_list.append({
                    'code': code,
                    'full_name': full_name,
                    'course': course,
                    'quant': quant, # Количество единиц, за которое дается курс (обычно 1, но 100 для JPY, HUF)
                    'change': change,
                    'rate_diff': change, # Изменение (разница) относительно предыдущего дня
                    'index': index
                })
            except (AttributeError, ValueError) as item_e:
                # Пропускаем некорректно сформированный элемент или ошибку преобразования
                print(f"Ошибка парсинга элемента '{item.find('title').text if item.find('title') is not None else 'Unknown'}': {item_e}")
                continue

        print(f"Парсинг завершен. Найдено {len(rates_list)} курсов на дату {course_date}.")
        
        return {
            'date': course_date,
            'rates': rates_list
        }

    except ET.ParseError as parse_e:
        print(f"Критическая ошибка парсинга XML: {parse_e}")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при парсинге: {e}")
        return None
