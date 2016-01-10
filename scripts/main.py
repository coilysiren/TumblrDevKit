# builtin
import time
# local
from builder import Builder


def watcher(callback, assets, themes):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    handler = FileSystemEventHandler()
    handler.on_created = callback
    handler.on_modified = callback

    observer = Observer()
    observer.schedule(handler, assets, recursive=True)
    observer.schedule(handler, themes)
    observer.start()
    return observer


if __name__ == '__main__':
    themes_dir = 'static/themes/' #ex: static/themes/cyrinsong.html
    sass_dir   = 'static/sass/'   #ex: static/sass/cyrinsong.sass

    b = Builder(themes_dir, sass_dir)

    b.create()
    observer = watcher(b.create, sass_dir, themes_dir)

    print('Watching \'{}**\' for changes'.format(sass_dir))
    print('Watching \'{}*\' for changes'.format(themes_dir))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
