import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.jpg'):
            filename = os.path.basename(event.src_path)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "image_updates",
                {
                    "type": "send_image",
                    "filename": filename
                }
            )
            print(f"Новое изображение: {filename}")

def start_monitoring():
    path = os.path.join(settings.BASE_DIR, 'downloads', 'screens')
    os.makedirs(path, exist_ok=True)
    
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Мониторинг папки {path} запущен")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
