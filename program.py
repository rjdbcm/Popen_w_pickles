from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import subprocess
from datetime import datetime
import pickle
import time
import sys


class SubProgramWatcher(QThread):
    def __init__(self, proc, flags):
        super(SubProgramWatcher, self).__init__()
        self.flags = flags
        self.send_flags()
        self.proc = proc

    def send_flags(self):
        print("[{}] Program Flags Send: {}".format(datetime.now(), self.flags))
        with open(r".flags.pkl", "wb") as outfile:
            pickle.dump(self.flags, outfile)

    def read_flags(self):
        with open(r".flags.pkl", "rb") as inpfile:
            flags = pickle.load(inpfile)
        if flags:
            self.flags = flags
            return self.flags

    def run(self):
        count = 0
        while self.proc.poll() is None:  # While the process is running read flags
            if self.read_flags()['progress'] < 1.0:
                if not self.read_flags()['done'] or self.read_flags()['killed']:
                    time.sleep(.5)
                    print("[{}] Program Flags Read: {}".format(datetime.now(), self.read_flags()))
                    count += 1
        print("[{}] DONE!".format(datetime.now()))


def main():
    app = QCoreApplication([])
    flags = {'done': False, "progress": 0.0}
    proc = subprocess.Popen([sys.executable, "subprogram.py"], stdout=subprocess.PIPE, shell=False)
    thread = SubProgramWatcher(proc, flags)
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

