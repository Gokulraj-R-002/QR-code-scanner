#!/bin/sh

# run the python script serialtotxt.py and wait for it to end
# then run the python script decode.py and wait for it to end

rm -rf data.txt

echo "Reading from serial port and writing the data in the file \"data.txt\"."
python serialtotxt.py

if [ -f data.txt ]; then
    echo "Successfully written the data in the file \"data.txt\"."
else
    echo "Failed to write the data in the file \"data.txt\"."
    exit
fi

echo "Decoding the data."

python decode.py
