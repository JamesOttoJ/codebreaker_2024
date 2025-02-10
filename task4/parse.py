#print("chmod +x vvv\x08\x08s_code.sh\x0d")
with open("audit.log", "r") as file:
    out_file = open("out.log", "w")
    while line := file.readline():
        out_file.write(bytes(line, "utf-8").decode("unicode-escape").replace("\x0d", ""))
        print(bytes(line, "utf-8").decode("unicode-escape").replace("\x0d", ""), end="")
