# scripts/data_parser.py

import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

def parse_rates_xml(xml_data: str) -> Optional[Dict]:
    """
    Парсит XML-данные курсов валют НБ РК, извлекая дату курсов и список валют.
    
    Включает устойчивую логику для очистки "грязного" XML и проверки на отсутствие данных.
    
    Returns:
        Optional[Dict]: Словарь с датой и списком курсов ('date', 'rates') или None в случае ошибки/отсутствия данных.
    """
    
    # --- КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ ДЛЯ ОШИБКИ 'not well-formed' ---
    # 1. Убираем BOM (Byte Order Mark), если присутствует, и обрезаем лишние пробелы.
    if xml_data.startswith('\ufeff'):
        xml_data = xml_data.lstrip('\ufeff')
    
    # 2. Находим начало корневого элемента <rates> и обрезаем весь посторонний текст.
    rates_start_index = xml_data.find('<rates>')
    
    if rates_start_index != -1:
        xml_data = xml_data[rates_start_index:].strip()
    else:
        print("Критическая ошибка: Не удалось найти корневой элемент <rates> в ответе API.")
        return None
    # --- КОНЕЦ ИСПРАВЛЕНИЯ ---

    rates_list: List[Dict] = []
    
    try:
        # Парсинг очищенной XML-строки
        root = ET.fromstring(xml_data)
        
        # 1.5. ✅ Улучшение: Проверка на тег <info> (отсутствие данных)
        info_element = root.find('info')
        if info_element is not None and info_element.text:
            print(f"Парсинг завершен: Ответ НБК гласит: '{info_element.text}'. Курсов нет.")
            # Возвращаем None, чтобы main_workflow знал, что данные невалидны
            return None 
            
        # 1. Извлечение даты
        date_element = root.find('date')
        course_date = date_element.text if date_element is not None else None

        if not course_date:
            print("Ошибка парсинга: Не найдена дата курсов в элементе <date>.")
            return None

        # 2. Парсинг каждого элемента <item>
        for item in root.findall('item'):
            try:
                # Извлечение текста элементов
                code = item.find('title').text          # Код валюты (KZT)
                rate_str = item.find('description').text # Курс (например, 450,12)
                quant_str = item.find('quant').text      # Номинал (например, 100)
                change_str = item.find('change').text    # Изменение относительно предыдущего дня
                
                # Дополнительные поля
                full_name = item.find('fullname').text if item.find('fullname') is not None else code
                index = item.find('index').text if item.find('index') is not None else 'NO'

                # Преобразование в числа. Используем replace(',', '.') для корректного парсинга
                course = float(rate_str.replace(',', '.'))
                quant = int(quant_str)
                # change_str может быть пустым или '0,00'
                change = float(change_str.replace(',', '.')) if change_str else 0.0

                rates_list.append({
                    'code': code,
                    'full_name': full_name,
                    'course': course,
                    'quant': quant, 
                    'change': change, # ✅ Используем 'change' для курсовой разницы за предыдущий день
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
        print(f"Критическая ошибка парсинга XML (внутренняя): {parse_e}")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при парсинге: {e}")
        return None
