import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.jpg'):
            filename = os.path.basename(event.src_path)
            print(f"🔔 Найдено новое изображение: {filename}")
            
            # Сохраняем информацию в файл в той же папке
            dir_path = os.path.dirname(event.src_path)
            info_file = os.path.join(dir_path, '.last_image.json')
            try:
                with open(info_file, 'w') as f:
                    json.dump({'filename': filename, 'timestamp': time.time()}, f)
                print(f"✅ Информация сохранена в {info_file}")
            except Exception as e:
                print(f"❌ Ошибка сохранения: {e}")

def start_monitoring():
    # Путь к папке screens (укажите ваш реальный путь)
    screens_dir = '/home/sasha/sites/tankistmk/site/downloads/screens'
    
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
