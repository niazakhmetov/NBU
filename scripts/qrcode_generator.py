# scripts/qrcode_generator.py

import qrcode
import base64
from io import BytesIO

# ⚠️ КОРРЕКЦИЯ: Для GitHub Pages домен должен быть в формате
# https://<username>.github.io/<repository-name>
# Использование https://github.com/... не позволит правильно маршрутизировать
# запрос к странице verify.html.
BASE_DOMAIN = "https://niazakhmetov.github.io/NBU" # <--- ИСПРАВЛЕННЫЙ ФОРМАТ
VERIFY_PAGE = "verify.html"

def generate_verification_url(course_date: str, currency_code: str = None) -> str:
    """
    Формирует уникальный URL для верификации.
    Если currency_code = None, то верифицируется вся дата.
    """
    url = f"{BASE_DOMAIN}/{VERIFY_PAGE}?d={course_date}"
    if currency_code:
        url += f"&c={currency_code}"
    return url

# Вызов для главной страницы:
# url_for_main_page = generate_verification_url(current_date)


def generate_qr_base64(data_url: str) -> str:
    """
    Генерирует QR-код для заданного URL и возвращает его в формате Base64 PNG.
    
    Этот формат удобен для прямого встраивания в HTML (Data URI).
    
    Args:
        data_url (str): URL, который должен быть закодирован в QR.
        
    Returns:
        str: Строка Base64, готовая для встраивания в тег <img>.
    """
    # Создание объекта QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(data_url)
    qr.make(fit=True)

    # Создание изображения
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Сохранение изображения в байтовый поток в формате PNG
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # Кодирование байтов в Base64
    base64_encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Формирование Data URI для встраивания в HTML
    return f"data:image/png;base64,{base64_encoded}"

# Пример использования (для тестирования):
if __name__ == '__main__':
    test_date = "26.11.2025"
    test_code = "USD"
    
    url = generate_verification_url(test_date, test_code)
    print(f"Сгенерированный URL: {url}")
    
    # base64_img = generate_qr_base64(url)
    # print(f"Base64 string (truncated): {base64_img[:50]}...")
