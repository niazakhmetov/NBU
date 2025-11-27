# scripts/i18n.py

MESSAGES = {
    'ru': {
        # --- ОБЩЕЕ / НАВИГАЦИЯ ---
        'title': 'Официальные курсы валют НБ РК | TengeHub',
        'title_about': 'О TengeHub | Официальные курсы НБ РК',
        'nav_main': 'Главная',
        'nav_all_rates': 'Все курсы',
        'nav_about': 'О платформе',
        'nav_status': 'Статус',
        'nav_verify_title': 'Подтверждение курса валют',
        
        # --- ОБЩИЕ ПЕРЕМЕННЫЕ КУРСОВ / ФУТЕР ---
        'data_actual_on': 'Курсы валют актуальны на',
        'description': 'Интеграция с официальным SOAP-сервисом Национального Банка РК. Курсы обновляются ежедневно.',
        'CURRENCY_NAME': 'ВАЛЮТА (НАЗВАНИЕ)',
        'RATE_NAME': 'КУРС (KZT)',
        'CHANGE': 'ИЗМЕНЕНИЕ',
        'partner_title': 'Сотрудничество',
        'partner_text': 'Если вы заинтересованы в интеграции данных или партнерстве, свяжитесь с нами.',
        'partner_cta': 'Связаться',
        'source_p': 'Все данные поступают исключительно из официального источника (Национальный Банк РК), что гарантирует их достоверность.',
        'source_p_short': 'Источник: НБ РК.',
        'copyright_full_text': 'Ресурс создан для обеспечения бухгалтеров и экономистов официальными и точными курсами валют. Все данные поступают исключительно из официального источника (Национальный Банк РК), что гарантирует их достоверность и применимость для целей учета.', # ⭐ ДОБАВЛЕНО

        # --- index_template.html ---
        'qr_verification_text': 'Для целей бухгалтерского и налогового учета: Моментальная верификация данных с официальным источником НБ РК. Отсканируйте QR-код для подтверждения актуальности курсов на',

        # --- full_rates_template.html ---
        'nav_full_rates_title': 'Полный список курсов',
        'quant_header': 'Кол-во ед.',
        'full_list_description': 'Здесь представлен полный перечень всех курсов валют, устанавливаемых Национальным Банком РК на указанную дату.',
        'calculator_h2': 'Калькулятор курсовых разниц',
        'calculator_date1': 'Дата 1 (Операции)',
        'calculator_date2': 'Дата 2 (Отчетная)',
        'calculator_btn': 'Рассчитать разницу',
        'export_h2': 'История и Экспорт данных',
        'export_btn_csv': 'Экспорт в CSV',
        'export_btn_print': 'Распечатать справку',
        
        # --- verify_template.html ---
        'verify_h2': 'Проверка достоверности официального курса',
        'verify_source': 'Источник проверки',
        'verify_date': 'Дата курса',
        'verify_code': 'Код валюты',
        'verify_rate': 'Официальный курс НБ РК',
        'verify_status_checking': 'Выполняется запрос к официальному API НБ РК...',
        'verify_status_success': '✅ ВЕРИФИКАЦИЯ УСПЕШНА',
        'verify_status_error': '❌ ОШИБКА ВЕРИФИКАЦИИ',
        'verify_status_not_found': '⚠️ Курс на указанную дату не найден в официальном источнике.',
        'verify_disclaimer': 'Данная страница создана для подтверждения курсов валют, используемых в бухгалтерском и налоговом учете в соответствии с законодательством РК.',

        # --- status_template.html ---
        'status_h2': 'Служебная информация и статус системы',
        'status_last_updated': 'Время последнего обновления',
        'status_source_api': 'Источник данных (API)',
        'status_source_type': 'Тип сервиса',
        'status_current_date': 'Дата актуальности курсов',
        'status_system_status': 'Статус синхронизации',
        'status_note': 'Примечание',
        'status_note_text': 'Данные о статусе генерируются при каждом запуске автоматического скрипта в GitHub Actions.',
        'status_system_ok': '✅ УСПЕШНО',
        'status_system_error': '❌ ОШИБКА',
        
        # --- about_template.html ---
        'about_h2': 'О проекте TengeHub',
        'about_p1': 'TengeHub — это некоммерческий проект, созданный для предоставления актуальных официальных курсов валют Национального Банка Республики Казахстан в удобном и быстром формате.',
        'about_p2': 'Мы стремимся предоставить надежный инструмент для бухгалтерского учета, аудита и анализа рыночных данных.', # ⭐ ДОБАВЛЕНО
        'tech_h3': 'Как это работает',
        'tech_step1_h': '1. Источник данных:',
        'tech_step1_p': 'Мы используем официальный SOAP-сервис Национального Банка РК для получения исходных данных.',
        'tech_step2_h': '2. Автоматизация:',
        'tech_step2_p': 'Ежедневно GitHub Actions запускает Python-скрипт, который извлекает, обрабатывает и преобразует данные.',
        'tech_step3_h': '3. Генерация:',
        'tech_step3_p': 'С помощью шаблонизатора Jinja2 создаются статические HTML-страницы, готовые к публикации.',
        'source_h3': 'Надежность источника',
        'contact_cta': 'Свяжитесь с нами для сотрудничества.',
    },
    'kz': {
        # --- ОБЩЕЕ / НАВИГАЦИЯ ---
        'title': 'ҚР ҰБ ресми валюта бағамдары | TengeHub',
        'title_about': 'TengeHub туралы | ҚР ҰБ ресми бағамдары',
        'nav_main': 'Басты бет',
        'nav_all_rates': 'Барлық бағамдар',
        'nav_about': 'Платформа туралы',
        'nav_status': 'Мәртебе',
        'nav_verify_title': 'Валюта бағамын растау',

        # --- ОБЩИЕ ПЕРЕМЕННЫЕ КУРСОВ / ФУТЕР ---
        'data_actual_on': 'Валюта бағамдары мына күнге өзекті',
        'description': 'ҚР Ұлттық Банкінің ресми SOAP-сервисімен интеграция. Бағамдар күн сайын жаңартылады.',
        'CURRENCY_NAME': 'ВАЛЮТА (АТАУЫ)',
        'RATE_NAME': 'БАҒАМ (KZT)',
        'CHANGE': 'ӨЗГЕРІС',
        'partner_title': 'Ынтымақтастық',
        'partner_text': 'Егер сіз деректерді біріктіруге немесе серіктестікке қызығушылық танытсаңыз, бізге хабарласыңыз.',
        'partner_cta': 'Хабарласу',
        'source_p': 'Барлық деректер тек ресми көзден (ҚР Ұлттық Банкі) алынады, бұл олардың дұрыстығына кепілдік береді.',
        'source_p_short': 'Дереккөз: ҚР ҰБ.', # ⭐ ДОБАВЛЕНО
        'copyright_full_text': 'Ресурс бухгалтерлер мен экономистерді ресми және нақты валюта бағамдарымен қамтамасыз ету үшін құрылған. Барлық деректер тек ресми көзден (ҚР Ұлттық Банкі) алынады, бұл олардың дұрыстығына және есеп мақсаттарына қолданылуына кепілдік береді.', # ⭐ ДОБАВЛЕНО

        # --- index_template.html ---
        'qr_verification_text': 'Бухгалтерлік және салықтық есепке алу мақсатында: ҚР ҰБ ресми дереккөзімен деректерді тексеру. Ағымдағы бағамдардың өзектілігін растау үшін QR-кодты сканерлеңіз',

        # --- full_rates_template.html ---
        'nav_full_rates_title': 'Толық бағамдар тізімі',
        'quant_header': 'Бірлік саны',
        'full_list_description': 'Мұнда ҚР Ұлттық Банкі белгілеген валюта бағамдарының толық тізімі көрсетілген.',
        'calculator_h2': 'Бағамдық айырмашылықтар калькуляторы',
        'calculator_date1': 'Күн 1 (Операция)',
        'calculator_date2': 'Күн 2 (Есептілік)',
        'calculator_btn': 'Айырмашылықты есептеу',
        'export_h2': 'Тарих және Деректерді экспорттау',
        'export_btn_csv': 'CSV-ға экспорттау',
        'export_btn_print': 'Анықтаманы басып шығару',
        
        # --- verify_template.html ---
        'verify_h2': 'Ресми бағамның дұрыстығын тексеру',
        'verify_source': 'Тексеру көзі',
        'verify_date': 'Бағам күні',
        'verify_code': 'Валюта коды',
        'verify_rate': 'ҚР ҰБ ресми бағамы',
        'verify_status_checking': 'ҚР ҰБ ресми API-не сұрау жіберілуде...',
        'verify_status_success': '✅ РАСТАУ СӘТТІ АЯҚТАЛДЫ',
        'verify_status_error': '❌ РАСТАУ ҚАТЕСІ',
        'verify_status_not_found': '⚠️ Бағам ресми дереккөзде табылған жоқ.',
        'verify_disclaimer': 'Бұл бет ҚР заңнамасына сәйкес бухгалтерлік және салықтық есепте пайдаланылатын валюта бағамдарын растау үшін жасалған.',

        # --- status_template.html ---
        'status_h2': 'Қызметтік ақпарат және жүйе мәртебесі',
        'status_last_updated': 'Соңғы жаңарту уақыты',
        'status_source_api': 'Дереккөз (API)',
        'status_source_type': 'Сервис түрі',
        'status_current_date': 'Бағамдардың өзектілік күні',
        'status_system_status': 'Синхрондау мәртебесі',
        'status_note': 'Ескерту',
        'status_note_text': 'Мәртебе туралы деректер GitHub Actions-дағы автоматты сценарийдің әр іске қосылуы кезінде жасалады.',
        'status_system_ok': '✅ СӘТТІ',
        'status_system_error': '❌ ҚАТЕ',
        
        # --- about_template.html ---
        'about_h2': 'TengeHub жобасы туралы',
        'about_p1': 'TengeHub — Қазақстан Республикасы Ұлттық Банкінің нақты ресми валюта бағамдарын ыңғайлы және жылдам форматта ұсыну үшін құрылған коммерциялық емес жоба.',
        'about_p2': 'Біз бухгалтерлік есеп, аудит және нарықтық деректерді талдау үшін сенімді құралды ұсынуға тырысамыз.', # ⭐ ДОБАВЛЕНО
        'tech_h3': 'Қалай жұмыс істейді',
        'tech_step1_h': '1. Дереккөз:',
        'tech_step1_p': 'Біз бастапқы деректерді алу үшін ҚР Ұлттық Банкінің ресми SOAP-сервисін қолданамыз.',
        'tech_step2_h': '2. Автоматтандыру:',
        'tech_step2_p': 'Күн сайын GitHub Actions скриптті іске қосады, ол деректерді өңдейді және түрлендіреді.',
        'tech_step3_h': '3. Генерациялау:',
        'tech_step3_p': 'Jinja2 шаблонизаторы арқылы жариялауға дайын статикалық HTML-беттер жасалады.',
        'source_h3': 'Дереккөз сенімділігі',
        'contact_cta': 'Ынтымақтастық үшін бізге хабарласыңыз.',
    },
    'en': {
        # --- ОБЩЕЕ / НАВИГАЦИЯ ---
        'title': 'Official Exchange Rates of NBK | TengeHub',
        'title_about': 'About TengeHub | Official NBK Rates',
        'nav_main': 'Main',
        'nav_all_rates': 'All Rates',
        'nav_about': 'About Platform',
        'nav_status': 'Status',
        'nav_verify_title': 'Currency Rate Verification',

        # --- ОБЩИЕ ПЕРЕМЕННЫЕ КУРСОВ / ФУТЕР ---
        'data_actual_on': 'Exchange rates are actual as of',
        'description': 'Integration with the official SOAP service of the National Bank of Kazakhstan. Rates are updated daily.',
        'CURRENCY_NAME': 'CURRENCY (NAME)',
        'RATE_NAME': 'RATE (KZT)',
        'CHANGE': 'CHANGE',
        'partner_title': 'Partnership',
        'partner_text': 'If you are interested in data integration or partnership, feel free to contact us.',
        'partner_cta': 'Contact Us',
        'source_p': 'All data comes exclusively from the official source (National Bank of Kazakhstan), guaranteeing its accuracy.',
        'source_p_short': 'Source: NBK.', # ⭐ ДОБАВЛЕНО
        'copyright_full_text': 'The resource is designed to provide accountants and economists with official and accurate exchange rates. All data comes exclusively from the official source (National Bank of Kazakhstan), guaranteeing its reliability and applicability for accounting purposes.', # ⭐ ДОБАВЛЕНО

        # --- index_template.html ---
        'qr_verification_text': 'For accounting and tax purposes: Instant data verification with the official NBK source. Scan the QR code to confirm the rates are current as of',

        # --- full_rates_template.html ---
        'nav_full_rates_title': 'Full List of Rates',
        'quant_header': 'Quantity',
        'full_list_description': 'Here is the full list of all exchange rates set by the National Bank of Kazakhstan as of the specified date.',
        'calculator_h2': 'Exchange Rate Difference Calculator',
        'calculator_date1': 'Date 1 (Operation)',
        'calculator_date2': 'Date 2 (Reporting)',
        'calculator_btn': 'Calculate Difference',
        'export_h2': 'History and Data Export',
        'export_btn_csv': 'Export to CSV',
        'export_btn_print': 'Print Statement',

        # --- verify_template.html ---
        'verify_h2': 'Verification of Official Rate Authenticity',
        'verify_source': 'Verification Source',
        'verify_date': 'Rate Date',
        'verify_code': 'Currency Code',
        'verify_rate': 'Official NBK Rate',
        'verify_status_checking': 'Sending request to official NBK API...',
        'verify_status_success': '✅ VERIFICATION SUCCESSFUL',
        'verify_status_error': '❌ VERIFICATION ERROR',
        'verify_status_not_found': '⚠️ Rate for the specified date was not found in the official source.',
        'verify_disclaimer': 'This page is created to confirm exchange rates used for accounting and tax purposes in accordance with the legislation of the Republic of Kazakhstan.',

        # --- status_template.html ---
        'status_h2': 'Service Information and System Status',
        'status_last_updated': 'Last Update Time',
        'status_source_api': 'Data Source (API)',
        'status_source_type': 'Service Type',
        'status_current_date': 'Currency Rates Actuality Date',
        'status_system_status': 'Synchronization Status',
        'status_note': 'Note',
        'status_note_text': 'Status data is generated every time the automated script runs in GitHub Actions.',
        'status_system_ok': '✅ SUCCESSFUL',
        'status_system_error': '❌ ERROR',
        
        # --- about_template.html ---
        'about_h2': 'About the TengeHub Project',
        'about_p1': 'TengeHub is a non-commercial project created to provide the current official exchange rates of the National Bank of the Republic of Kazakhstan in a convenient and fast format.',
        'about_p2': 'We strive to provide a reliable tool for accounting, auditing, and market data analysis.', # ⭐ ДОБАВЛЕНО
        'tech_h3': 'How It Works',
        'tech_step1_h': '1. Data Source:',
        'tech_step1_p': 'We use the official SOAP service of the National Bank of Kazakhstan to retrieve the raw data.',
        'tech_step2_h': '2. Automation:',
        'tech_step2_p': 'GitHub Actions runs a Python script daily which extracts, processes, and transforms the data.',
        'tech_step3_h': '3. Generation:',
        'tech_step3_p': 'Static HTML pages, ready for publication, are created using the Jinja2 templating engine.',
        'source_h3': 'Source Reliability',
        'contact_cta': 'Contact us for partnership.',
    },
}
```
