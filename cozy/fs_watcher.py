import pyinotify

import logging
log = logging.getLogger("fs_watcher")

from gi.repository import Gio

import cozy.db as db
import cozy.tools as tools

class Watcher():
    wds = []
    def __init__(self):
        self.wm = pyinotify.WatchManager()
        self.mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_UNMOUNT | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_DELETE_SELF
        self.notifier = pyinotify.ThreadedNotifier(self.wm, EventHandler())
        self.notifier.start()

        #for location in db.Storage.select():
            #print(tools.find_mount_point(location.path))
        #    self.watch_directory(location.path)

        vm = Gio.VolumeMonitor.get()
        vm.connect("mount-removed", self.__on_mount_removed)
        vm.connect("mount-added", self.__on_mount_added)

    def watch_directory(self, dir):
        log.info("Adding directory watch for " + dir)
        self.wds.append(self.wm.add_watch(dir, self.mask, rec=True))

    def stop_watching_directory(self, dir):
        pass

    def stop_notifier(self):
        self.notifier.stop()

    def __on_mount_removed(self, volume_monitor, mount):
        log.info("Volume unmounted: " + mount.get_default_location().get_path())

    def __on_mount_added(self, volume_monitor, mount):
        log.info("Volume mounted: " + mount.get_default_location().get_path())

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        log.info("Creating: " + event.pathname)

    def process_IN_DELETE(self, event):
        log.info("Removing: " + event.pathname)

    def process_IN_MODIFY(self, event):
        log.info("Modified: " + event.pathname)

    def process_IN_UNMOUNT(self, event):
        log.info("Unmounted: " + event.pathname)

    def process_IN_MOVED_TO(self, event):
        log.info("Moved to: " + event.pathname)

    def process_IN_MOVED_FROM(self, event):
        log.info("Moved from: " + event.pathname)

    def process_IN_DELETE_SELF(self, event):
        log.info("process_IN_DELETE_SELF: " + event.pathname)