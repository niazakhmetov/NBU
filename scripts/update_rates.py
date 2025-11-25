import logging
from datetime import datetime, timedelta
# Импорты для работы с SOAP-сервисом
from zeep import Client, Settings
from zeep.exceptions import Fault
# Импорт для безопасного и эффективного парсинга XML
from lxml import etree 
# Импорт для генерации HTML-файла
from jinja2 import Environment, FileSystemLoader 
import json # Используется для передачи данных в JavaScript через Jinja2

# ----------------------------------------------------
# 1. КОНСТАНТЫ И НАСТРОЙКИ
# ----------------------------------------------------

# Адрес WSDL-описания веб-сервиса НБ РК
WSDL_URL = "https://nbportal.nationalbank.kz:443/WebService/NSI_NBRK?wsdl"

# Код справочника для курсов валют
GUIDE_CODE_RATES = "NSI_NBRK_CRCY_COURSE"

# Настройка zeep: strict=False может потребоваться для обхода некоторых особенностей SOAP-серверов
settings = Settings(strict=False, xml_huge_tree=True) 

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Пространство имен для парсинга XML (для lxml)
NS = {
    's': 'http://schemas.xmlsoap.org/soap/envelope/',
    'n': 'http://www.w3.org/2003/05/soap-envelope'
}

# Мультиязычные тексты для Jinja2 и JavaScript
MESSAGES = {
    'ru': {
        'title': "Официальные курсы валют НБ РК | TengeHub",
        'status_prefix': "Данные актуальны на",
        'description': "Интеграция с официальным SOAP-сервисом Национального Банка РК. Курсы обновляются ежедневно.",
        'currency_rate': "Курс",
        'currency_name': "Валюта",
        'rate_name': "Курс (KZT)",
        'change': "Изменение",
        'partner_title': "B2B API & Экспорт данных",
        'partner_text': "Получите доступ к данным в удобном формате (JSON/CSV) через наш REST API для вашей ERP, 1С или CRM.",
        'partner_cta': "Стать партнером"
    },
    'kz': {
        'title': "ҚР Ұлттық Банкінің ресми валюта бағамдары | TengeHub",
        'status_prefix': "Деректердің қолданылу мерзімі",
        'description': "ҚР Ұлттық Банкінің ресми SOAP-сервисімен интеграция. Бағамдар күн сайын жаңартылады.",
        'currency_rate': "Бағам",
        'currency_name': "Валюта",
        'rate_name': "Бағам (KZT)",
        'change': "Өзгеріс",
        'partner_title': "B2B API & Деректер экспорты",
        'partner_text': "ERP, 1С немесе CRM жүйелеріңіз үшін біздің REST API арқылы деректерге ыңғайлы форматта (JSON/CSV) қол жеткізіңіз.",
        'partner_cta': "Серіктес болу"
    },
    'en': {
        'title': "Official Exchange Rates of NBK | TengeHub",
        'status_prefix': "Data is current as of",
        'description': "Integration with the official SOAP service of the National Bank of Kazakhstan. Rates are updated daily.",
        'currency_rate': "Rate",
        'currency_name': "Currency",
        'rate_name': "Rate (KZT)",
        'change': "Change",
        'partner_title': "B2B API & Data Export",
        'partner_text': "Get access to data in a convenient format (JSON/CSV) via our REST API for your ERP, 1C, or CRM.",
        'partner_cta': "Become a partner"
    }
}


# ----------------------------------------------------
# 2. ФУНКЦИЯ ДЛЯ ЗАПРОСА ДАННЫХ
# ----------------------------------------------------

def get_exchange_rates(start_date: str, end_date: str):
    """
    Запрос официальных курсов валют НБ РК через SOAP-сервис.
    """
    logging.info(f"Подключение к WSDL по адресу: {WSDL_URL}")
    
    try:
        client = Client(WSDL_URL, settings=settings)
        
        # Форматируем даты для WSDL (dateTime) с указанием часового пояса
        begin_date_param = f"{start_date}T00:00:00.000+06:00"
        end_date_param = f"{end_date}T00:00:00.000+06:00"

        logging.info(f"Запрос данных за период: {start_date} по {end_date}")

        # Вызов SOAP-операции с явным указанием параметров
        response = client.service.GET_GUIDE(
            guideCode=GUIDE_CODE_RATES,
            type='CHAD',
            beginDate=begin_date_param,
            endDate=end_date_param
        )
        
        # Доступ к атрибутам через ТОЧКУ
        err_code = response.errCode
        err_msg = response.errMsg
        
        if err_code != 0:
            logging.error(f"Сервис НБ РК вернул ошибку. Код: {err_code}. Сообщение: {err_msg}")
            return None
        
        rates_xml_string = response.result
        
        logging.info("Данные успешно получены.")
        return rates_xml_string

    except Fault as f:
        logging.error(f"SOAP Fault при запросе: {f}")
        return None
    except Exception as e:
        logging.error(f"Критическая ошибка при работе с WSDL: {e}") 
        return None

# ----------------------------------------------------
# 3. ФУНКЦИЯ ДЛЯ ПАРСИНГА XML
# ----------------------------------------------------

def parse_rates_xml(rates_xml_string: str) -> list:
    """
    Парсит XML-строку, полученную от НБ РК, и извлекает курсы.
    """
    if not rates_xml_string:
        return []

    logging.info("Начало парсинга XML-ответа.")
    parsed_rates = []

    try:
        root = etree.fromstring(rates_xml_string.encode('utf-8'))
        
        # Используем XPath для поиска всех сущностей (Entity)
        entities = root.xpath('//n:Entity', namespaces=NS)
        if not entities:
            entities = root.xpath('//s:Entity', namespaces=NS)
            if not entities:
                 logging.warning("В XML не найдено ни одной сущности (Entity) с курсами.")
                 return []
        
        logging.info(f"Найдено {len(entities)} курсовых записей.")

        for entity in entities:
            # Ищем EntityCustom в обоих Namespace
            custom = entity.find('./n:EntityCustom', namespaces=NS) or entity.find('./s:EntityCustom', namespaces=NS)
            if custom is not None:
                try:
                    # Извлечение пользовательских реквизитов (также ищем в обоих Namespace)
                    curr_code = custom.findtext('./n:CurrCode', namespaces=NS) or custom.findtext('./s:CurrCode', namespaces=NS)
                    course_str = custom.findtext('./n:Course', namespaces=NS) or custom.findtext('./s:Course', namespaces=NS)
                    correlation_str = custom.findtext('./n:Corellation', namespaces=NS) or custom.findtext('./s:Corellation', namespaces=NS)
                    course_date = custom.findtext('./n:CourseDate', namespaces=NS) or custom.findtext('./s:CourseDate', namespaces=NS)

                    # Нормализация: замена запятой на точку и преобразование в float
                    course_value = float(course_str.replace(',', '.'))
                    correlation_value = int(correlation_str)
                    
                    # Финальный нормализованный курс (Курс / Множитель)
                    final_rate = course_value / correlation_value

                    parsed_rates.append({
                        'currency': curr_code,
                        # Убираем время из даты
                        'date': course_date.split('T')[0] if course_date else None, 
                        'rate': round(final_rate, 4),
                        'correlation': correlation_value
                    })

                except (AttributeError, ValueError) as e:
                    logging.error(f"Ошибка парсинга полей в EntityCustom: {e}")
                    continue

    except etree.XMLSyntaxError as e:
        logging.error(f"Ошибка синтаксиса XML: {e}")
        return []
    except Exception as e:
        logging.error(f"Неизвестная ошибка при парсинге: {e}")
        return []
        
    logging.info("Парсинг XML успешно завершен.")
    return parsed_rates

# ----------------------------------------------------
# 4. ФУНКЦИЯ ДЛЯ ГЕНЕРАЦИИ HTML
# ----------------------------------------------------

def generate_html(current_rates: list, prev_rates: dict, date_str: str, output_path='index.html'):
    """
    Генерирует финальный HTML-файл, используя Jinja2.
    """
    logging.info("Начало генерации HTML.")
    
    # Настраиваем Jinja2 для загрузки из текущей директории
    loader = FileSystemLoader('.')
    env = Environment(loader=loader)
    
    try:
        # Предполагаем, что шаблон называется index_template.html
        template = env.get_template('index_template.html') 
    except Exception as e:
        logging.error(f"Ошибка загрузки шаблона 'index_template.html'. Убедитесь, что файл существует: {e}")
        return

    # Подготовка данных для рендеринга (расчет разницы)
    rendered_rates = []
    
    for rate in current_rates:
        curr = rate['currency']
        
        # Находим курс за предыдущий день. Если нет (например, новая валюта), берем текущий
        prev_rate = prev_rates.get(curr, rate['rate']) 

        diff = rate['rate'] - prev_rate
        diff_str = f"{diff:+.4f}" # Формат с обязательным знаком (+ или -)
        
        # Определяем класс для стрелки
        if diff > 0.0001:
            diff_class = 'up'
        elif diff < -0.0001:
            diff_class = 'down'
        else:
            diff_class = 'neutral'
        
        rendered_rates.append({
            'currency': curr,
            'rate': f"{rate['rate']:.4f}",
            'diff': diff_str,
            'diff_class': diff_class
        })

    # Сортируем USD, EUR, RUB в начало списка для лучшего отображения в MVP
    priority_currencies = ['USD', 'EUR', 'RUB']
    
    sorted_rates = sorted(rendered_rates, 
                         key=lambda x: (0 if x['currency'] in priority_currencies else 1, 
                                        priority_currencies.index(x['currency']) if x['currency'] in priority_currencies else x['currency']))

    # Рендеринг шаблона
    # ИСПРАВЛЕНИЕ: Передаем словарь MESSAGES напрямую.
    output = template.render(
        last_update_date=date_str,
        rates=sorted_rates,
        MESSAGES=MESSAGES 
    )

    # Сохранение финального HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    logging.info(f"HTML-файл '{output_path}' успешно сгенерирован и обновлен.")


# ----------------------------------------------------
# 5. ТОЧКА ВХОДА И ЗАПУСК
# ----------------------------------------------------

if __name__ == "__main__":
    today = datetime.now().date()
    
    # Дата, которую мы показываем (T-1)
    current_date = today - timedelta(days=1)
    # Дата для сравнения (T-2)
    previous_date = today - timedelta(days=2)
    
    current_date_str = current_date.strftime('%Y-%m-%d')
    previous_date_str = previous_date.strftime('%Y-%m-%d')

    print("--- ЗАПУСК ETL-СКРИПТА TengeHub ---")

    # 1. Получаем текущие курсы (T-1)
    data_xml_current = get_exchange_rates(current_date_str, current_date_str)
    
    if not data_xml_current:
        print("Ошибка: Не удалось получить текущие курсы. Процесс остановлен.")
        exit()
        
    current_rates_list = parse_rates_xml(data_xml_current)
    
    # 2. Получаем предыдущие курсы для сравнения (T-2)
    data_xml_prev = get_exchange_rates(previous_date_str, previous_date_str)
    
    prev_rates_dict = {}
    if data_xml_prev:
        prev_rates_list = parse_rates_xml(data_xml_prev)
        # Преобразуем список в словарь для быстрого поиска: {'USD': 518.0, ...}
        prev_rates_dict = {rate['currency']: rate['rate'] for rate in prev_rates_list}
    else:
        logging.warning("Не удалось получить курсы за предыдущий день (T-2). Изменения не будут рассчитаны.")

    # 3. Генерируем HTML
    if current_rates_list:
        generate_html(
            current_rates=current_rates_list,
            prev_rates=prev_rates_dict,
            date_str=current_date.strftime('%Y-%m-%d'),
            output_path='index.html' # Записываем в основной файл
        )
    else:
        print("Не удалось извлечь курсы из XML. HTML не сгенерирован.")