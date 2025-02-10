#print("chmod +x vvv\x08\x08s_code.sh\x0d")
with open("out.log", "r") as file:
    out_file = open("out_uft8.log", "w")
    while line := file.readline():
        out_file.write(bytes(line, "unicode-escape").decode("utf-8") + "\n")
        print(bytes(line, "unicode-escape").decode("utf-8"))
