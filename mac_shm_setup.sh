#! /bin/sh

NAME="RAMDisk"

function RAMDisk_mount() {
    diskutil quiet eraseVolume HFS+ $NAME `hdiutil attach -nomount ram://$((2048 * 2))`
}

function RAMDisk_unmount() {
    CURDISK="$(diskutil info RAMDisk | grep -o '/dev/disk[1-99]')"
    hdiutil detach -quiet $CURDISK
}
if [[ "$1" = "mount" ]]; then
    RAMDisk_mount
fi

if [[ "$1" = "unmount" ]]; then
    RAMDisk_unmount
fi