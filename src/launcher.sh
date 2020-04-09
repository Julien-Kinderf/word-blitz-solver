#!/usr/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# First get the screen from the phone to /img/temp.png:
adb shell screencap /storage/self/primary/scripts/word-blitz/temp.png
adb pull /storage/self/primary/scripts/word-blitz/temp.png $DIR/../img/tmp/temp.png
echo "Screenshot successfully taken"

# Then just start the python script :
python3 $DIR/solver.py $DIR/../img/tmp/temp.png


# mv $DIR/../img/tmp/temp.png $DIR/../img/toidentify/temp.png