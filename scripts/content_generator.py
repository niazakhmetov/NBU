# scripts/content_generator.py
import os
from jinja2 import Environment, FileSystemLoader

# --- Настройка окружения Jinja2 ---
# Предполагаем, что шаблоны находятся в текущей директории или в 'templates'
file_loader = FileSystemLoader('.') 
env = Environment(loader=file_loader)


def generate_page(template_file: str, output_file: str, context: dict):
    """
    Основная функция для генерации статической HTML-страницы из шаблона.

    Args:
        template_file (str): Имя файла шаблона Jinja2 (напр., 'index_template.html').
        output_file (str): Имя выходного HTML-файла (напр., 'index.html').
        context (dict): Словарь данных для заполнения шаблона (курсы, дата, переводы, QR-код).
    """
    try:
        # 1. Загрузка шаблона
        template = env.get_template(template_file)
        
        # 2. Рендеринг (заполнение шаблона данными из контекста)
        output = template.render(context)
        
        # 3. Сохранение результата в выходной файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
            
        print(f"Файл {output_file} успешно сгенерирован (шаблон: {template_file}).")
        
    except FileNotFoundError:
        print(f"Ошибка: Шаблон {template_file} не найден. Проверьте путь.")
    except Exception as e:
        print(f"Критическая ошибка генерации {output_file}: {e}")

# Функции generate_json_api, generate_html_page, generate_about_page 
# удалены, так как их логика теперь должна быть реализована в scripts/main_workflow.py.
