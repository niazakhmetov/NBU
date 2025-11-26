# scripts/content_generator.py

from jinja2 import Environment, FileSystemLoader, select_autoescape, exceptions
import datetime
import os

def generate_page(template_file: str, output_file: str, context: dict):
    """
    Генерирует статическую HTML страницу на основе Jinja2 шаблона и контекста.
    """
    # Шаблоны ищутся в текущей директории
    env = Environment(
        loader=FileSystemLoader(os.getcwd()),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # ⭐ КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ:
    # Регистрируем функцию datetime.datetime.now как глобальную функцию 'now'.
    # Это позволяет использовать ее в шаблонах как {{ now().year }} или {{ now().date() }}
    env.globals.update(
        now=datetime.datetime.now,
    )
    
    # Регистрируем функцию os.path.basename для удобства в статусе/отладке
    env.globals.update(
        basename=os.path.basename,
    )

    print(f"Генерация {output_file} (шаблон: {template_file})...")
    
    try:
        template = env.get_template(template_file)
        
        # Генерация и сохранение
        html_content = template.render(context)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Файл {output_file} успешно сгенерирован (шаблон: {template_file}).")
        
    except exceptions.TemplateNotFound as e:
        print(f"Критическая ошибка генерации {output_file}: Шаблон '{e.name}' не найден.")
    except Exception as e:
        print(f"Критическая ошибка генерации {output_file}: {e}")

# Пример использования:
if __name__ == '__main__':
    # Эта часть не должна запускаться в workflow, только для локального теста
    pass
