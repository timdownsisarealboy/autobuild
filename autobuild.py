import sys
import time
import logging
from watchdog.observers import Observer
from subprocess import call, check_output
import os
from watchdog.events import FileSystemEventHandler
import platform
update_dir = None


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_any_event(self, event):
        if ".git" not in event.src_path:
            ret_dir = os.getcwd()
            os.chdir(update_dir)
            composer_loc = check_output(["which","composer"])
            if "composer" in composer_loc:
                call(["composer", "update"])
            else:
                call(["/usr/bin/php", "./composer.phar", "update"])
            os.chdir(ret_dir)

if __name__ == "__main__":
    watch_dir = sys.argv[1]
    update_dir = sys.argv[2]
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    observer = Observer()
    event_handler = MyEventHandler(observer)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
