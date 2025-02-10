import http.client
import json
import ssl
import re
import urllib.parse
import requests
import warnings
import html
import ansi_parser

warnings.filterwarnings('ignore')

host = '34.195.208.56'
#print("chmod +x vvv\x08\x08s_code.sh\x0d")
with open("audit.log", "r") as file:
    i = -1
    command_history = []
    out_file = open("responses.json", "w")
    out_file.write("[")
    response_file = open("responses.md", "w")
    error_file = open("error_responses.out", "w")
    commands_file = open("commands.txt", "w")
    while line := file.readline():
        i += 1
        match = re.search("d=.*u=", line)
        if (match is None):
            #match = re.search("(d=)?.*u=", line)
            print("Not found: " + line)
            continue
        #print("Start and end: " + str(match.span()))
        #print("First and last char: " + line[match.start()] + " | " + line[match.end()])
        #if (line[match.start()] == 'd'):
        #    start = match.start() + 2
        #else:
        #    start = match.start()
        start = match.start() + 2
        end = match.end() - 3
        command = line[start:end]
        #print("Raw: " + command)
        command = ansi_parser.parse(command)
        if command == "":
            i -= 1
            continue
        j = 0
        for c in command:
            if c == '\x1a':
                j += 1
        if j != 0:
            command = command_history[i - j] + command[j:]
        commands_file.write(command + "\n")
        if command in command_history:
            command_history.append(command)
            continue
        command_history.append(command)
        #print("Parsed: " + command)
        if (command[:5] == "gagpt"):
            command = command[10:-1] # remove "gagpt -m"
            #print("Command: " + command)
        elif (command[:6] == " gagpt"):
            command = command [11:-1]
        else: continue
        #print()
        response = requests.get(
            "https://" + host + "/?q=" + urllib.parse.quote_plus(command),
            verify=False,
            cert=("client.crt", "client.key")
        )
        #print(str(response.status_code) + " | " + response.text)
        if (response.status_code > 399):
            error_file.write(command + "\n")
            error_file.write(str(response.status_code) + " | " + response.text + "\n\n")
        else:
            out_file.write(response.text + ",")
            response_file.write("# Command\n")
            response_file.write(command + "\n")
            response_file.write("# Response\n")
            response_file.write(response.json()["fulfillment"][0]["text"].replace('<', r'\<').replace('>', r'\>')+ "\n")
        print(command)
    out_file.write(']')
