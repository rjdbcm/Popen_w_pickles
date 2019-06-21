from datetime import datetime
import time
from flags import FlagIO


class SubProgram(FlagIO):
    def __init__(self):
        FlagIO.__init__(self, subprogram=True)  # Old-school inheritance
        self.flags = self.read_flags()
        self.flags.started = True
        self.io_flags()
        while self.flags.progress < 1.0 and not self.flags.kill:
            try:
                time.sleep(.5)
            except KeyboardInterrupt:  # Catch a keyboard interrupt and unmount the ramdisk
                self.cleanup_ramdisk()
                raise KeyboardInterrupt
            self.flags.progress += .01
            self.io_flags()
        else:
            self.flags.done = True
            self.io_flags()


if __name__ == "__main__":
    SubProgram()