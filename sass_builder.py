# builtin
import os
import subprocess
from glob import glob


class Builder(object):

    def __init__(self, assets_dir, output_dir):
        self.assets_dir = assets_dir
        self.output_dir = output_dir

    def compile_sass(self, *args, **kwargs):
        for sass_file_path in glob(self.assets_dir+'*.*'):
            filename = sass_file_path.split(self.assets_dir)[-1].split('.')[0]
            css_path = self.output_dir + filename + '.css'

            print('Building \'{}\''.format(css_path))

            sass_args = {
                'source': '{}'.format(sass_file_path),
                'output': '{}'.format(css_path),
            }
            subprocess.call('''
                sassc -m {source} {output} -s compressed
                '''.format(**sass_args),
                shell=True,
                preexec_fn=os.setsid,
                stdout=subprocess.PIPE
            )
        print('Completed Build')

    def start(self):
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        handler = FileSystemEventHandler()
        handler.on_modified = self.compile_sass

        watch = Observer()
        watch.schedule(handler, self.assets_dir, recursive=True)
        watch.start()
        print('Watching \'{}\' for changes'.format(self.assets_dir))
