#!/usr/bin/env python3
import re

FILENAME = "attack-surface-tech.adoc"

# if a line contains :: create a new dict entry and use the text before :: as dict key
# read lines after that line until an empty line and
# add them to the dict value which is a list of strings

glossary = {}
current_term = ""

with open(FILENAME) as f:
    for line in f:
        m = re.match(r"(.*)::", line)
        if m:
            current_term = m.group(1)
            glossary[current_term] = []  # start new term
        elif current_term != "":
            if not re.match(r"^\s*$", line):  # non-empty -> add to the term
                glossary[current_term].append(line.strip())
            else:
                current_term = ""

for k in sorted(glossary.keys()):
    print(f"{k}::")
    for l in glossary[k]:
        print(l)
    print("")
