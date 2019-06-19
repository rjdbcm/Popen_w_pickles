#! /bin/sh
$NAME="RAMDisk"

function mount() {
    hdiutil attach -nomount -mountpoint /dev/shm ram://$((2 * 1024 * 4)) > $DISKNO
    diskutil eraseVolume HFS+ $NAME $DISKNO
}

function unmount() {
    hdiutil unmount /Volumes/$NAME
}