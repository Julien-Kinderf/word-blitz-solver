#!/usr/bin/bash
# This scripts takes a number of N arguments
# Each argument corresponds to a node on a Word List grid
# This scripts swipes and links every argument in order to form the word


PATTERN=$@

# This script takes a list of grid nodes as an input
# It just links the dots accordingly

# THE COORDINATES:
YROW[0]=750
YROW[1]=990
YROW[2]=1240
YROW[3]=1480

XCOL[0]=190
XCOL[1]=420 # Nice
XCOL[2]=670
XCOL[3]=900


StartTouch() {
    adb shell sendevent /dev/input/event4 3 57 14
}

# Sending the event to the phone
SendCoordinates () {
    adb shell sendevent /dev/input/event4 3 53 $1
    adb shell sendevent /dev/input/event4 3 54 $2
    adb shell sendevent /dev/input/event4 3 58 57
    adb shell sendevent /dev/input/event4 0 0 0
}

FinishTouch() {
    adb shell sendevent /dev/input/event4 3 57 4294967295
    adb shell sendevent /dev/input/event4 0 0 0
}

# Swiping
StartTouch
for NUM in $PATTERN
do
    COLNUM=$((NUM % 4))
    ROWNUM=$(((NUM - COLNUM) / 4))
    X=${XCOL[$COLNUM]}
    Y=${YROW[$ROWNUM]}
    
    SendCoordinates $X $Y
    
    #echo "node $NUM : row $ROWNUM and col $COLNUM. Coordinates : X=$X - Y=$Y"
done

FinishTouch
