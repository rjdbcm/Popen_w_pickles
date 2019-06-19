from datetime import datetime
import pickle
import sys
import time
import os


class FlagIO(object):
    def __init__(self):
        self.READ_MSG = "[{}] {} Flags Read: {}"
        flagfile = ".flags.pkl"
        if sys.platform == "darwin":
            ramdisk = "/Volumes/RAMDisk"
            os.system(". mac_shm_setup.sh; RAMDisk_mount")
            time.sleep(.5)  # Give the OS time to finish
        else:
            ramdisk = "/dev/shm"
        self.flagpath = os.path.join(ramdisk, flagfile)

    def send_flags(self):
        print("[{}] {} Flags Send: {}".format(datetime.now(), type(self).__name__, self.flags))
        with open(r"{}".format(self.flagpath), "wb") as outfile:
            pickle.dump(self.flags, outfile)

    def read_flags(self):
        with open(r"{}".format(self.flagpath), "rb") as inpfile:
            try:
                flags = pickle.load(inpfile)
            except EOFError:
                print("[{}] Program Flags Busy: Reusing old".format(datetime.now()))
                flags = self.flags
            self.flags = flags
            return self.flags

    def cleanup_ramdisk(self):
        if sys.platform == "darwin":
            os.system(". mac_shm_setup.sh; RAMDisk_unmount")
        else:
            pass