# scripts/i18n.py

# Полный словарь для интернационализации (i18n)
MESSAGES = {
    'ru': {
        'title': 'Официальные курсы валют НБ РК | TengeHub',
        'description': 'Интеграция с официальным SOAP-сервисом Национального Банка РК. Курсы обновляются ежедневно.',
        'data_actual_on': 'Курсы валют актуальны на',
        
        # Заголовки таблицы
        'currency_name': 'Валюта (Название)',
        'rate_name': 'Курс (KZT)',
        'change': 'Изменение',

        # Навигация 
        'nav_main': 'Главная',
        'nav_all_rates': 'Все курсы',
        'nav_about': 'О платформе',

        # Секция партнерства
        'partner_title': 'Сотрудничество',
        'partner_text': 'Заинтересованы в партнерстве или хотите разместить рекламу? Свяжитесь с нами для обсуждения условий.',
        'partner_cta': 'Связаться',
        
        # --- НОВЫЕ КЛЮЧИ ДЛЯ ABOUT.HTML ---
        'title_about': 'О платформе | TengeHub',
        'about_h2': 'О проекте TengeHub',
        'about_p1': 'TengeHub — это независимый проект, созданный для предоставления актуальных и надежных курсов валют Национального Банка Республики Казахстан в удобном, современном формате API и веб-сайта.',
        'tech_h3': 'Механизм обновления данных',
        'tech_step1_h': '1. Источник данных:',
        'tech_step1_p': 'Курсы валют в режиме реального времени запрашиваются напрямую через SOAP-сервис Национального Банка РК.',
        'tech_step2_h': '2. Автоматизация:',
        'tech_step2_p': 'Обновление данных и генерация сайта происходят полностью автоматически благодаря GitHub Actions, которые запускают скрипт ежедневно.',
        'tech_step3_h': '3. Генерация:',
        'tech_step3_p': 'После получения данных Python-скрипты генерируют статический API-файл (latest.json) и HTML-страницы (index.html, about.html и т.д.) с помощью шаблонизатора Jinja2.',
        'source_h3': 'Открытый исходный код',
        'source_p': 'Весь код проекта TengeHub является открытым (Open Source). Вы можете изучить, как работает система, и предложить улучшения на нашем репозитории GitHub.'
    },
    'kz': {
        'title': 'ҚР Ұлттық Банкінің ресми валюта бағамдары | TengeHub',
        'description': 'ҚР Ұлттық Банкінің ресми SOAP-қызметімен интеграция. Бағамдар күнделікті жаңартылады.',
        'data_actual_on': 'Валюта бағамдары мына күнге өзекті',
        
        # Заголовки таблицы
        'currency_name': 'Валюта (Атауы)',
        'rate_name': 'Бағам (KZT)',
        'change': 'Өзгеріс',

        # Навигация
        'nav_main': 'Басты',
        'nav_all_rates': 'Барлық бағамдар',
        'nav_about': 'Платформа туралы',

        # Секция партнерства
        'partner_title': 'Ынтымақтастық',
        'partner_text': 'Әріптестікке қызығушылық танытасыз ба немесе жарнама орналастырғыңыз келе ме? Шарттарды талқылау үшін бізге хабарласыңыз.',
        'partner_cta': 'Хабарласу',
        
        # --- НОВЫЕ КЛЮЧИ ДЛЯ ABOUT.HTML ---
        'title_about': 'Платформа туралы | TengeHub',
        'about_h2': 'TengeHub жобасы туралы',
        'about_p1': 'TengeHub — бұл Қазақстан Республикасы Ұлттық Банкінің нақты және сенімді валюта бағамдарын ыңғайлы, заманауи API және веб-сайт форматында ұсыну үшін құрылған тәуелсіз жоба.',
        'tech_h3': 'Деректерді жаңарту механизмі',
        'tech_step1_h': '1. Дерек көзі:',
        'tech_step1_p': 'Валюта бағамдары ҚР Ұлттық Банкінің SOAP-қызметі арқылы нақты уақыт режимінде сұратылады.',
        'tech_step2_h': '2. Автоматтандыру:',
        'tech_step2_p': 'Деректерді жаңарту және сайтты генерациялау GitHub Actions арқылы толығымен автоматты түрде жүзеге асады, ол скриптті күн сайын іске қосады.',
        'tech_step3_h': '3. Генерациялау:',
        'tech_step3_p': 'Деректер алынғаннан кейін Python скрипттері Jinja2 шаблондау құралын пайдаланып статикалық API файлын (latest.json) және HTML беттерін (index.html, about.html және т.б.) жасайды.',
        'source_h3': 'Ашық бастапқы код',
        'source_p': 'TengeHub жобасының барлық коды ашық (Open Source) болып табылады. Сіз жүйенің қалай жұмыс істейтінін зерттеп, GitHub репозиторийімізде жақсартулар ұсына аласыз.'
    },
    'en': {
        'title': 'Official Exchange Rates of NB RK | TengeHub',
        'description': 'Integration with the official SOAP service of the National Bank of Kazakhstan. Rates are updated daily.',
        'data_actual_on': 'Exchange rates are actual as of',

        # Заголовки таблицы
        'currency_name': 'Currency (Name)',
        'rate_name': 'Rate (KZT)',
        'change': 'Change',

        # Навигация
        'nav_main': 'Home',
        'nav_all_rates': 'All Rates',
        'nav_about': 'About Platform',
        
        # Секция партнерства
        'partner_title': 'Partnership',
        'partner_text': 'Interested in partnership or want to place advertising? Contact us to discuss terms.',
        'partner_cta': 'Contact Us',
        
        # --- НОВЫЕ КЛЮЧИ ДЛЯ ABOUT.HTML ---
        'title_about': 'About Platform | TengeHub',
        'about_h2': 'About the TengeHub Project',
        'about_p1': 'TengeHub is an independent project created to provide up-to-date and reliable exchange rates from the National Bank of the Republic of Kazakhstan in a convenient, modern API and website format.',
        'tech_h3': 'Data Update Mechanism',
        'tech_step1_h': '1. Data Source:',
        'tech_step1_p': 'Real-time exchange rates are requested directly through the National Bank of Kazakhstan’s official SOAP service.',
        'tech_step2_h': '2. Automation:',
        'tech_step2_p': 'Data refresh and site generation are fully automatic, powered by GitHub Actions which execute the script daily.',
        'tech_step3_h': '3. Generation:',
        'tech_step3_p': 'After receiving the data, Python scripts generate a static API file (latest.json) and HTML pages (index.html, about.html, etc.) using the Jinja2 templating engine.',
        'source_h3': 'Open Source Code',
        'source_p': 'The entire code for the TengeHub project is Open Source. You can review how the system works and suggest improvements on our GitHub repository.'
    }
}
