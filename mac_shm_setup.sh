#! /bin/sh
NAME="RAMDisk"

function RAMDisk_mount() {
    DISKNO="$(hdiutil attach -nomount -mountpoint /dev/shm ram://$((2 * 1024 * 4)))"
    echo ${DISKNO}
    diskutil eraseVolume HFS+ $NAME ${DISKNO}
}

function RAMDisk_unmount() {
    hdiutil unmount /Volumes/$NAME
}