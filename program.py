from PyQt5.QtCore import *
import subprocess
from datetime import datetime
import time
import sys
from flags import FlagIO


class SubProgramWatcher(QThread, FlagIO):
    def __init__(self, proc, flags):
        super(SubProgramWatcher, self).__init__()
        self.proc = proc
        self.flags = flags
        self.send_flags()
        time.sleep(1)

    def run(self):
        count = 0
        limit = 500
        while self.proc.poll() is None and not self.read_flags()['kill'] or not self.read_flags()['done']:  # While the process is running read flags
            if self.read_flags()['progress'] < 1.0 and self.read_flags()['started']:
                print(self.READ_MSG.format(datetime.now(), type(self).__name__, self.read_flags()))
                time.sleep(.1)
                count += 1
                if count > limit:
                    self.flags['kill'] = True
                    self.send_flags()
                    break
        print("[{}] Finished!".format(datetime.now()))


def cleanup():
    FlagIO.cleanup_ramdisk(SubProgramWatcher)


def main():
    app = QCoreApplication([])
    flags = {'done': False, "progress": 0.0, 'kill': False, 'started': False}
    cleanup()
    proc = subprocess.Popen([sys.executable, "subprogram.py"], stdout=subprocess.PIPE, shell=False)
    thread = SubProgramWatcher(proc, flags)
    thread.finished.connect(app.exit)
    thread.finished.connect(cleanup)
    thread.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

