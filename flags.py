from datetime import datetime
import pickle
import sys
import time
import os

class FlagIO(object):
    def __init__(self, subprogram=False, delay=0.2):
        self.READ_MSG = "[{}] {} Flags Read: {}"
        self.subprogram = subprogram
        self.delay = delay
        self.flagpath = self.init_ramdisk()
        if subprogram:
            try:
                f = open(self.flagpath)
                f.close()
            except FileNotFoundError:
                time.sleep(5)

    def send_flags(self):
        print("[{}] {} Flags Send: {}".format(datetime.now(), type(self).__name__, self.flags))
        with open(r"{}".format(self.flagpath), "wb") as outfile:
            pickle.dump(self.flags, outfile)

    def read_flags(self):
        with open(r"{}".format(self.flagpath), "rb") as inpfile:
            try:
                flags = pickle.load(inpfile)
            except EOFError:
                print("[{}] {} Flags Busy: Reusing old".format(datetime.now(), type(self).__name__))
                flags = self.flags
            self.flags = flags
            return self.flags

    def init_ramdisk(self):
        flagfile = ".flags.pkl"
        if sys.platform == "darwin":
            ramdisk = "/Volumes/RAMDisk"
            if not self.subprogram:
                os.system("./mac_shm_setup.sh mount")
                time.sleep(self.delay)  # Give the OS time to finish
        else:
            ramdisk = "/dev/shm"
        flagpath = os.path.join(ramdisk, flagfile)
        return flagpath

    def cleanup_ramdisk(self):
        if sys.platform == "darwin":
            os.system("./mac_shm_setup.sh unmount")
        else:
            pass