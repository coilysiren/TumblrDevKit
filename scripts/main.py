# builtin
import time
# local
from builder import Builder


def watcher(directory, callback):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    handler = FileSystemEventHandler()
    handler.on_modified = callback
    handler.on_created  = callback

    observer = Observer()
    observer.schedule(handler, directory, recursive=True)
    observer.start()
    print('Watching \'{}\' for changes'.format(directory))
    return observer


if __name__ == '__main__':
    themes_dir = 'static/themes/' #ex: static/themes/cyrinsong.html
    sass_dir   = 'static/sass/'   #ex: static/sass/cyrinsong.sass

    b = Builder(themes_dir, sass_dir)

    b.create()
    observer = watcher('static/', b.create)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
