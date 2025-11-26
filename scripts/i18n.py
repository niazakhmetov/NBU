# scripts/i18n.py

MESSAGES = {
    'ru': {
        # Заголовок
        'title': 'Официальные курсы валют НБ РК | TengeHub',
        'title_about': 'О TengeHub | Официальные курсы НБ РК',

        # Навигация
        'nav_main': 'Главная',
        'nav_all_rates': 'Все курсы',
        'nav_about': 'О платформе',

        # Главная страница (index_template.html)
        'data_actual_on': 'Курсы валют актуальны на',
        'description': 'Интеграция с официальным SOAP-сервисом Национального Банка РК. Курсы обновляются ежедневно.',
        'CURRENCY_NAME': 'ВАЛЮТА (НАЗВАНИЕ)',
        'RATE_NAME': 'КУРС (KZT)',
        'CHANGE': 'ИЗМЕНЕНИЕ',
        
        # Раздел "Партнеры" (для примера)
        'partner_title': 'Сотрудничество',
        'partner_text': 'Если вы заинтересованы в интеграции данных или партнерстве, свяжитесь с нами.',
        'partner_cta': 'Связаться',

        # Страница "О нас" (about_template.html)
        'about_h2': 'О проекте TengeHub',
        'about_p1': 'TengeHub — это некоммерческий проект, созданный для предоставления актуальных официальных курсов валют Национального Банка Республики Казахстан в удобном и быстром формате.',
        'tech_h3': 'Как это работает',
        'tech_step1_h': '1. Источник данных:',
        'tech_step1_p': 'Мы используем официальный SOAP-сервис Национального Банка РК для получения исходных данных.',
        'tech_step2_h': '2. Автоматизация:',
        'tech_step2_p': 'Ежедневно GitHub Actions запускает Python-скрипт, который извлекает, обрабатывает и преобразует данные.',
        'tech_step3_h': '3. Генерация:',
        'tech_step3_p': 'С помощью шаблонизатора Jinja2 создаются статические HTML-страницы, готовые к публикации.',
        'source_h3': 'Надежность источника',
        'source_p': 'Все данные поступают исключительно из официального источника (Национальный Банк РК), что гарантирует их достоверность.',
        'contact_cta': 'Свяжитесь с нами для сотрудничества.',
    },
    'kz': {
        # Заголовок
        'title': 'ҚР ҰБ ресми валюта бағамдары | TengeHub',
        'title_about': 'TengeHub туралы | ҚР ҰБ ресми бағамдары',

        # Навигация
        'nav_main': 'Басты бет',
        'nav_all_rates': 'Барлық бағамдар',
        'nav_about': 'Платформа туралы',

        # Главная страница (index_template.html)
        'data_actual_on': 'Валюта бағамдары мына күнге өзекті',
        'description': 'ҚР Ұлттық Банкінің ресми SOAP-сервисімен интеграция. Бағамдар күн сайын жаңартылады.',
        'CURRENCY_NAME': 'ВАЛЮТА (АТАУЫ)',
        'RATE_NAME': 'БАҒАМ (KZT)',
        'CHANGE': 'ӨЗГЕРІС',

        # Раздел "Партнеры"
        'partner_title': 'Ынтымақтастық',
        'partner_text': 'Егер сіз деректерді біріктіруге немесе серіктестікке қызығушылық танытсаңыз, бізге хабарласыңыз.',
        'partner_cta': 'Хабарласу',
        
        # Страница "О нас" (about_template.html)
        'about_h2': 'TengeHub жобасы туралы',
        'about_p1': 'TengeHub — Қазақстан Республикасы Ұлттық Банкінің нақты ресми валюта бағамдарын ыңғайлы және жылдам форматта ұсыну үшін құрылған коммерциялық емес жоба.',
        'tech_h3': 'Қалай жұмыс істейді',
        'tech_step1_h': '1. Дереккөз:',
        'tech_step1_p': 'Біз бастапқы деректерді алу үшін ҚР Ұлттық Банкінің ресми SOAP-сервисін қолданамыз.',
        'tech_step2_h': '2. Автоматтандыру:',
        'tech_step2_p': 'Күн сайын GitHub Actions скриптті іске қосады, ол деректерді өңдейді және түрлендіреді.',
        'tech_step3_h': '3. Генерациялау:',
        'tech_step3_p': 'Jinja2 шаблонизаторы арқылы жариялауға дайын статикалық HTML-беттер жасалады.',
        'source_h3': 'Дереккөз сенімділігі',
        'source_p': 'Барлық деректер тек ресми көзден (ҚР Ұлттық Банкі) алынады, бұл олардың дұрыстығына кепілдік береді.',
        'contact_cta': 'Ынтымақтастық үшін бізге хабарласыңыз.',
    },
    'en': {
        # Заголовок
        'title': 'Official Exchange Rates of NBK | TengeHub',
        'title_about': 'About TengeHub | Official NBK Rates',
        
        # Навигация
        'nav_main': 'Main',
        'nav_all_rates': 'All Rates',
        'nav_about': 'About Platform',

        # Главная страница (index_template.html)
        'data_actual_on': 'Exchange rates are actual as of',
        'description': 'Integration with the official SOAP service of the National Bank of Kazakhstan. Rates are updated daily.',
        'CURRENCY_NAME': 'CURRENCY (NAME)',
        'RATE_NAME': 'RATE (KZT)',
        'CHANGE': 'CHANGE',
        
        # Раздел "Партнеры"
        'partner_title': 'Partnership',
        'partner_text': 'If you are interested in data integration or partnership, feel free to contact us.',
        'partner_cta': 'Contact Us',

        # Страница "О нас" (about_template.html)
        'about_h2': 'About the TengeHub Project',
        'about_p1': 'TengeHub is a non-commercial project created to provide the current official exchange rates of the National Bank of the Republic of Kazakhstan in a convenient and fast format.',
        'tech_h3': 'How It Works',
        'tech_step1_h': '1. Data Source:',
        'tech_step1_p': 'We use the official SOAP service of the National Bank of Kazakhstan to retrieve the raw data.',
        'tech_step2_h': '2. Automation:',
        'tech_step2_p': 'GitHub Actions runs a Python script daily which extracts, processes, and transforms the data.',
        'tech_step3_h': '3. Generation:',
        'tech_step3_p': 'Static HTML pages, ready for publication, are created using the Jinja2 templating engine.',
        'source_h3': 'Source Reliability',
        'source_p': 'All data comes exclusively from the official source (National Bank of Kazakhstan), guaranteeing its accuracy.',
        'contact_cta': 'Contact us for partnership.',
    },
}
