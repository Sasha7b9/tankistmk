import os
import time
import sys
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Добавляем путь к проекту
sys.path.append('/home/sasha/sites/tankistmk/site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Импортируем settings после настройки окружения
from django.conf import settings

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.jpg'):
            filename = os.path.basename(event.src_path)
            print(f"🔔 Найдено новое изображение: {filename}")
            
            # Сохраняем информацию о новом файле (для polling)
            info_file = os.path.join(settings.BASE_DIR, 'downloads', 'screens', '.last_image.json')
            try:
                with open(info_file, 'w') as f:
                    json.dump({'filename': filename, 'timestamp': time.time()}, f)
                print(f"✅ Информация о {filename} сохранена")
            except Exception as e:
                print(f"❌ Ошибка сохранения: {e}")

def start_monitoring():
    # Определяем путь к папке screens
    screens_dir = os.path.join(settings.BASE_DIR, 'downloads', 'screens')
    
    # Создаем папку если её нет
    os.makedirs(screens_dir, exist_ok=True)
    print(f"📁 Мониторинг папки: {screens_dir}")
    
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, screens_dir, recursive=False)
    observer.start()
    print(f"✅ Мониторинг запущен. Ожидание новых JPG файлов...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n⏹️ Мониторинг остановлен")
    observer.join()

if __name__ == "__main__":
    start_monitoring()
