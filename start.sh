#!/bin/bash


# check if there are existing processes
if pgrep -f "./ngrok http 3000" &> /dev/null
then
    printf "Ngrok is already running, exiting."
    exit
else
    printf "Tunneling port 3000 via ngrok in the background.\n"
    nohup ngrok http 3000 > /dev/null 2>&1 &
fi

# check if there are existing processes
if pgrep -f "python app.py" &> /dev/null
then
    printf "Python process is already running, exiting."
    exit
else
    printf "Running PDT ProgressBot in the background."
    nohup python app.py > /dev/null 2>&1 &
fi

printf "Done."
