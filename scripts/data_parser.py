# scripts/data_parser.py

import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

def parse_rates_xml(xml_data: str) -> Optional[Dict]:
    """
    Парсит XML-данные курсов валют НБ РК.

    Извлекает дату курсов и список валют с их полным именем, курсом и изменением.
    """
    
    rates_list: List[Dict] = []
    
    try:
        # Парсинг XML-строки
        root = ET.fromstring(xml_data)
        
        # 1. ИСПРАВЛЕНИЕ: Извлечение даты из дочернего элемента <date>, а не атрибута
        date_element = root.find('date')
        course_date = date_element.text if date_element is not None else None

        if not course_date:
            print("Ошибка парсинга: Не найдена дата курсов в элементе <date>.")
            return None

        # 2. Парсинг каждого элемента <item>
        for item in root.findall('item'):
            try:
                # Извлечение текста элементов
                code = item.find('title').text # Код валюты из <title> [cite: 158]
                
                # ⭐ ИСПРАВЛЕНИЕ: Курс находится в <description> 
                rate_str = item.find('description').text
                
                quant_str = item.find('quant').text
                change_str = item.find('change').text
                
                # Дополнительные поля
                full_name = item.find('fullname').text if item.find('fullname') is not None else code
                index = item.find('index').text if item.find('index') is not None else 'NO'

                # Преобразование в числа. Используем replace(',', '.')
                course = float(rate_str.replace(',', '.'))
                quant = int(quant_str)
                change = float(change_str.replace(',', '.')) if change_str else 0.0

                rates_list.append({
                    'code': code,
                    'full_name': full_name,
                    'course': course,
                    'quant': quant, 
                    'change': change,
                    'rate_diff': change, 
                    'index': index
                })
            except (AttributeError, ValueError) as item_e:
                # Пропускаем некорректно сформированный элемент или ошибку преобразования
                item_title = item.find('title').text if item.find('title') is not None else 'Unknown'
                print(f"Ошибка парсинга элемента '{item_title}': {item_e}")
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
