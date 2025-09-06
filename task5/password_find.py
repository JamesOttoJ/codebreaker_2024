import string
import subprocess

characters = string.ascii_letters + string.digits + string.punctuation
password_base = ";:qXBeX?oM~/CU{g"

for char1 in characters:
    for char2 in characters:
        password = password_base + char1 + char2
        print("password: " + password)
        out = subprocess.run(["/mnt/USB-128/unlock"], input=password.encode(), capture_output=True)
        #print(out.stderr)
        if "Password incorrect." not in str(out.stderr):
            exit()
        print()
