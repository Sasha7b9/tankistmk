from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.template.loader import render_to_string
from urllib.parse import quote
from django.http import JsonResponse
import os
import mimetypes
import glob

def get_last_image(request):
    """Возвращает имя последнего JPG файла в папке screens"""
    screens_dir = os.path.join(settings.BASE_DIR, 'downloads', 'screens')
    os.makedirs(screens_dir, exist_ok=True)
    
    # Проверяем сохраненную информацию о последнем файле
    info_file = os.path.join(screens_dir, '.last_image.json')
    
    if os.path.exists(info_file):
        try:
            with open(info_file, 'r') as f:
                data = json.load(f)
                return JsonResponse({'filename': data.get('filename')})
        except:
            pass
    
    # Если нет сохраненной информации, ищем последний файл
    jpg_files = glob.glob(os.path.join(screens_dir, '*.jpg'))
    if jpg_files:
        # Исключаем временные файлы
        jpg_files = [f for f in jpg_files if not os.path.basename(f).startswith('.')]
        if jpg_files:
            latest = max(jpg_files, key=os.path.getctime)
            filename = os.path.basename(latest)
            return JsonResponse({'filename': filename})
    
    return JsonResponse({'filename': None})

def download_file(request, filename):
    """Универсальная функция для скачивания любых файлов."""
    
    file_path = os.path.join(settings.BASE_DIR, 'downloads', filename)
    
    if not os.path.exists(file_path):
        raise Http404(f"Файл '{filename}' не найден")
    
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    try:
        file_handle = open(file_path, 'rb')
    except IOError:
        raise Http404("Ошибка при открытии файла")
    
    response = FileResponse(
        file_handle,
        content_type=mime_type,
        as_attachment=True,
        filename=filename
    )
    
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
    response['Content-Length'] = os.path.getsize(file_path)
    response['Cache-Control'] = 'no-cache'
    
    return response

def index(request):
    """Главная страница с тремя зонами"""
    return render(request, 'main/base.html')

def load_page(request, page_name):
    """API для загрузки страниц в правую зону из отдельных HTML-файлов"""
    
    # Словарь соответствия имени страницы и пути к шаблону
    page_templates = {
        'home': 'main/pages/home.html',
        'about': 'main/pages/about.html',
        'gallery': 'main/pages/gallery.html',
        'history': 'main/pages/history.html',
        'contact': 'main/pages/contact.html',
        'development': 'main/pages/development.html',
    }
    
    if page_name in page_templates:
        try:
            # Загружаем содержимое из отдельного HTML-файла
            html_content = render_to_string(page_templates[page_name])
            return HttpResponse(html_content)
        except Exception as e:
            return HttpResponse(f"<h2>Ошибка загрузки страницы</h2><p>{str(e)}</p>", status=500)
    else:
        return HttpResponse("<h2>Страница не найдена</h2><p>Пожалуйста, вернитесь на главную страницу.</p>", status=404)

def main_page(request):
    """Альтернативный вариант - одна страница со всем контентом"""
    return render(request, 'main/base.html')

print("DEBUG: views.py loaded")
print(f"DEBUG: get_last_image function defined: {get_last_image if 'get_last_image' in dir() else 'NOT FOUND'}")
