from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from urllib.parse import quote
import os
import mimetypes

def download_file(request, filename):
    """
    Универсальная функция для скачивания любых файлов.
    filename - имя файла, который нужно скачать из папки downloads
    """
    
    # Безопасно строим путь к файлу
    file_path = os.path.join(settings.BASE_DIR, 'downloads', filename)
    
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        raise Http404(f"Файл '{filename}' не найден")
    
    # Определяем MIME-тип файла
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type is None:
        # Если тип не определен, используем общий бинарный тип
        mime_type = 'application/octet-stream'
    
    # Открываем файл в бинарном режиме
    try:
        file_handle = open(file_path, 'rb')
    except IOError:
        raise Http404("Ошибка при открытии файла")
    
    # Создаем ответ с файлом
    response = FileResponse(
        file_handle,
        content_type=mime_type,
        as_attachment=True,
        filename=filename
    )
    
    # Добавляем дополнительные заголовки для совместимости
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
    response['Content-Length'] = os.path.getsize(file_path)
    response['Cache-Control'] = 'no-cache'
    
    return response


def index(request):
    """Главная страница с тремя зонами"""
    return render(request, 'main/base.html')

def load_page(request, page_name):
    """API для загрузки страниц в правую зону"""
    
    pages = {
        'home': {
            'title': 'Добро пожаловать',
            'content': '''
                <h2>Добро пожаловать на портал "Танкист МК"</h2>
                <p>Здесь вы найдете самую актуальную информацию о танках, их истории и современных разработках.</p>
                <p>Используйте меню слева для навигации по разделам сайта.</p>
                <p>Наш сайт посвящен:</p>
                <ul>
                    <li>Истории танкостроения</li>
                    <li>Современным танкам</li>
                    <li>Тактике боя</li>
                    <li>Знаменитым танкистам</li>
                </ul>
            '''
        },
        'about': {
            'title': 'О танках',
            'content': '''
                <h2>О танках</h2>
                <p>Танк — это бронированная гусеничная машина, сочетающая в себе огневую мощь, защиту и подвижность.</p>
                <p>Первые танки появились во время Первой мировой войны. С тех пор они стали основным средством на поле боя.</p>
                <p>Современные танки оснащены сложными системами наведения, композитной броней и мощными двигателями.</p>
            '''
        },
        'gallery': {
            'title': 'Галерея',
            'content': '''
                <h2>Галерея танков</h2>
                <div style="display: grid; gap: 20px;">
                    <div style="background: white; padding: 15px; border-radius: 10px;">
                        <h3>T-34</h3>
                        <p>Легендарный советский танк времен Второй мировой войны.</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 10px;">
                        <h3>Leopard 2</h3>
                        <p>Немецкий основной боевой танк, один из лучших в мире.</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 10px;">
                        <h3>Abrams M1</h3>
                        <p>Американский основной боевой танк с газотурбинным двигателем.</p>
                    </div>
                </div>
            '''
        },
        'history': {
            'title': 'История танкостроения',
            'content': '''
                <h2>История танкостроения</h2>
                <p>15 сентября 1916 года - день первого применения танков в битве на Сомме.</p>
                <p>С тех пор танки прошли долгий путь развития:</p>
                <ul>
                    <li><strong>1910-е:</strong> Первые танки (Mark I, Renault FT)</li>
                    <li><strong>1930-40-е:</strong> Расцвет танкостроения (T-34, Tiger, Sherman)</li>
                    <li><strong>1950-60-е:</strong> Основные боевые танки (T-54/55, M48 Patton)</li>
                    <li><strong>1970-90-е:</strong> Современные танки (Leopard 2, M1 Abrams, T-80)</li>
                    <li><strong>2000-е и далее:</strong> Цифровые технологии и активная защита</li>
                </ul>
            '''
        },
        'contact': {
            'title': 'Контакты',
            'content': '''
                <h2>Контакты</h2>
                <p>Свяжитесь с нами для получения дополнительной информации:</p>
                <ul>
                    <li>Email: info@tankist-mk.ru</li>
                    <li>Telegram: @tankist_mk</li>
                    <li>ВКонтакте: vk.com/tankist_mk</li>
                </ul>
                <p>Мы открыты для сотрудничества и предложений!</p>
            '''
        },
                'development': {  # ← Новая страница
            'title': 'Разработка',
            'content': '''
                <h2>Разработка</h2>
                <p>В этом разделе представлена техническая документация.</p>
                <p>
                    <a href="#" onclick="openDocs()" class="docs-link">
                        📚 Документация C4 4.5
                    </a>
                </p>
                <p>Нажмите на ссылку выше, чтобы открыть документацию.</p>
                
                <script>
                    function openDocs() {
                        window.open('/downloads/C4-4.5-Docs/index.html', '_blank');
                    }
                </script>
            '''
        }
    }
    
    if page_name in pages:
        page = pages[page_name]
        html = f"""
            <div class="page-content">
                {page['content']}
            </div>
        """
        return HttpResponse(html)
    else:
        return HttpResponse("<h2>Страница не найдена</h2><p>Пожалуйста, вернитесь на главную страницу.</p>", status=404)

def main_page(request):
    """Альтернативный вариант - одна страница со всем контентом"""
    return render(request, 'main/base.html')
