import numpy as np
from itertools import permutations
import string

c1_xor_c2 = b'\x7d\x10\x48\x3b\x27\x53\x6f\x1d\x52\x72\x3d\x51\x3d\x20\x14\x42'#\x6b\x83'
characters = string.ascii_letters + string.digits + string.punctuation
print("Characters: " + characters)
available_characters = []
for i in range(len(c1_xor_c2)):
    available_characters.append([])
    for char in characters:
        #print((int.from_bytes(char.encode()) ^ c1_xor_c2[i]).to_bytes(1).decode('utf-8'))
        #found_char = characters.find(str((int.from_bytes(char.encode()) ^ c1_xor_c2[i]).to_bytes(1)))
        #print(str(c1_xor_c2[i]) + " ^ " + char + " = " + str(found_char))
        try:
            if characters.find((int.from_bytes(char.encode()) ^ c1_xor_c2[i]).to_bytes(1).decode('utf-8')) > -1:
                available_characters[i].append(char)
        except:
            continue
    #print(str(i) + " | " + str(available_characters[i]))
with open("wordlist.txt", "w") as worlist_file:
    for a in available_characters[0]:
        for b in available_characters[1]:
            for c in available_characters[2]:
                for d in available_characters[3]:
                    for e in available_characters[4]:
                        for f in available_characters[5]:
                            for g in available_characters[6]:
                                for h in available_characters[7]:
                                    for i in available_characters[8]:
                                        for j in available_characters[9]:
                                            for k in available_characters[10]:
                                                for l in available_characters[11]:
                                                    for m in available_characters[12]:
                                                        print("inc m")
                                                        for n in available_characters[13]:
                                                            for o in available_characters[14]:
                                                                for p in available_characters[15]:
                                                                    for q in characters:
                                                                        for r in characters:
                                                                            worlist_file.write(str(a) + str(b) + str(c) + str(d) + str(e) + str(f) + str(g) + str(h) + str(i) + str(j) + str(k) + str(l) + str(m) + str(n) + str(o) + str(p) + str(q) + str(r) + "\n")
