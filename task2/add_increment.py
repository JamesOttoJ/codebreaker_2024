#!/usr/bin/python3

files = ["logseq14870984571-i","logseq188149928221-i","logseq275591500024897-i","logseq2811679046771-i","logseq284582537021286-i","logseq31049129429664-i","logseq3221662148509-i","logseq32882693717455-i","logseq33022166721967-i","logseq359152092707-i","logseq40582166913031-i","logseq5763223028829-i","logseq69301907728591-i","logseq9224279729674-i","logseq173613109912986-i","logseq223322278614086-i","logseq7781332013904-i","logseq164091379732168-i","logseq19893200728065-i","logseq359152092707-i"]

for i in range(len(files)):
    for j in range(len(files)):
        print("cat /home/jamesj/Documents/codebreaker_2024/task2/snapshots/" + files[j] + " | sudo zfs recv -F testpool/testdisk")
