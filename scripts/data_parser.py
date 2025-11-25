# scripts/data_parser.py
from lxml import etree
import math

# --- Справочник русских названий валют (39 курсов НБ РК) ---
CURRENCY_NAMES_RU = {
    'USD': 'Доллар США',
    'EUR': 'Евро',
    'RUB': 'Российский рубль',
    'AED': 'Дирхам ОАЭ',
    'AMD': 'Армянский драм',
    'AUD': 'Австралийский доллар',
    'AZN': 'Азербайджанский манат',
    'BRL': 'Бразильский реал',
    'BYN': 'Белорусский рубль',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'CZK': 'Чешская крона',
    'DKK': 'Датская крона',
    'GBP': 'Фунт стерлингов',
    'GEL': 'Грузинский лари',
    'HKD': 'Гонконгский доллар',
    'HUF': 'Венгерский форинт',
    'INR': 'Индийская рупия',
    'JPY': 'Японская иена',
    'KGS': 'Киргизский сом',
    'KRW': 'Вон Республики Корея',
    'KWD': 'Кувейтский динар',
    'MDL': 'Молдавский лей',
    'MYR': 'Малайзийский ринггит',
    'NOK': 'Норвежская крона',
    'PLN': 'Польский злотый',
    'QAR': 'Катарский риал',
    'SAR': 'Саудовский риал',
    'SEK': 'Шведская крона',
    'SGD': 'Сингапурский доллар',
    'THB': 'Тайский бат',
    'TJS': 'Таджикский сомони',
    'TMT': 'Туркменский манат',
    'TRY': 'Турецкая лира',
    'UAH': 'Украинская гривна',
    'UZS': 'Узбекский сум',
    'ZAR': 'Рэнд ЮАР',
    'XDR': 'СДР (Специальные права заимствования)',
}


def parse_xml_data(xml_data):
    """
    Разбирает XML-ответ и извлекает курсы валют.
    Добавляет русское название (`ru`) к каждому курсу.
    """
    if not xml_data:
        return {}

    root = etree.fromstring(xml_data.encode('utf-8'))
    # Namespace для элементов Envelope и Body
    ns_map = {'s': 'http://www.w3.org/2003/05/soap-envelope'}
    rates_data = {}
    
    # ИСПРАВЛЕНИЕ: Используем префикс s: для всех элементов
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
        
        # Расчет и округление
        try:
            course = float(course_value_str) / corellation_value
            course = round(course, 4)
        except ValueError:
            course = 0.0

        if curr_code == 'KZT':
            continue

        rates_data[curr_code] = {
            'code': curr_code,
            'course': course,
            'corellation': corellation_value,
            'course_date': course_date_str,
            # ДОБАВЛЕНО: Русское название из справочника
            'ru': CURRENCY_NAMES_RU.get(curr_code, curr_code) 
        }
    
    print(f"Успешно разобрано {len(rates_data)} курсов валют.")
    return rates_data
