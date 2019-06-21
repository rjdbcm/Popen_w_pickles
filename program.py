from PyQt5.QtCore import *
import subprocess
from datetime import datetime
from tqdm import tqdm
import time
import sys
from flags import FlagIO, Flags


class SubProgramWatcher(QThread, FlagIO):
    def __init__(self, proc, flags, timeout, rate=0.1):
        super(SubProgramWatcher, self).__init__()
        self.limit = timeout // rate
        self.rate = rate
        self.proc = proc
        self.flags = flags
        self.send_flags()
        time.sleep(1)

    def run(self):
        count = 0
        with tqdm(total=1.0, desc="SubProgram Progress", file=sys.stdout, smoothing=0.2,
                  bar_format='{l_bar}{bar}|{elapsed}/{remaining}') as pbar:
            while self.proc.poll() is None and not self.read_flags().kill or not self.read_flags().done:  # While the process is running read flags
                if self.read_flags().progress < 1.0 and self.read_flags().started:
                    # print(self.READ_MSG.format(datetime.now(), type(self).__name__, self.read_flags()))
                    f1 = self.read_flags().progress
                    time.sleep(self.rate)
                    f2 = self.read_flags().progress
                    pbar.update(round(f2-f1, 3))
                    count += 1
                    if count > self.limit:
                        self.flags.kill = True
                        self.send_flags()
                        self.proc.kill()
                        break
            if not self.flags.kill:
                while pbar.n < 1.0:
                    pbar.update(round(1.0-pbar.n, 3))
                    time.sleep(self.rate)
            pbar.clear()
        if self.flags.kill:
            print("CPU Timeout Exceeded: SubProgram Killed!")
        elif self.flags.done:
            print("Finished!")


def cleanup():
    FlagIO.cleanup_ramdisk(SubProgramWatcher)


def main():
    app = QCoreApplication([])
    flags = Flags()
    cleanup()
    proc = subprocess.Popen([sys.executable, "subprogram.py"], stdout=subprocess.PIPE, shell=False)
    thread = SubProgramWatcher(proc, flags, 150)
    thread.finished.connect(app.exit)
    thread.finished.connect(cleanup)
    thread.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

