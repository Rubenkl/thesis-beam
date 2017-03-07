from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher(FileSystemEventHandler):
  def __init__(self, observer, callback):
    self.observer = observer
    self.callback = callback


  def on_created(self, event):
    self.callback(event.src_path)
    self.observer.stop()


  

class FolderWatch(object):
  

  def __init__(self, folder, callback):
    self.folder = folder
    self.observer = Observer()
    eventHandler = Watcher(self.observer, callback)

    self.observer.schedule(eventHandler, folder, recursive=False)
    self.observer.start()
    self.observer.join()







  