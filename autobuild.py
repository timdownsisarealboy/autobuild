import sys
import time
import logging
from watchdog.observers import Observer
from subprocess import call
import os
from watchdog.events import FileSystemEventHandler


update_dir = None


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_any_event(self, event):
        if ".git" not in event.src_path and not event.is_directory and not os.path.basename(os.path.abspath(event.src_path)).startswith('.'):
            module = update_dir.split("/")[-1]
            src_parts = event.src_path.split("/")
            i = 1
            for part in src_parts:
                if part == module:
                    break
                else:
                    i = i + 1
            destination = update_dir + "/" + "/".join(src_parts[i:])
            if event.event_type is "deleted":
                print "removing %s" % (destination)
                call(["rm", destination])
            else:
                print "copying %s to %s" % (event.src_path, destination)
                call(["cp", event.src_path, destination])

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
