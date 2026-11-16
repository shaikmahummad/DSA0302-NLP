import re

tests = [
    ("cat", r"cat?"),          # ? : zero or one occurrence
    ("ca", r"cat+"),         # + : one or more occurrences
    ("cat", r"[abc]+"),        # [] : character set
    ("xyz", r"[^abc]+"),       # [^] : not a, b, or c
    ("cat", r"c.t"),           # . : any single character
    ("hello", r"^hello$"),     # ^ and $ : beginning and end
    ("hello world", r"^hello"),# ^ : beginning
    ("hello world", r"hello$") # $ : end
]

for string, pattern in tests:
    if re.search(pattern, string):
        print(f"Pattern {pattern:12} String '{string:12}' -> YES")
    else:
        print(f"Pattern {pattern:12} String '{string:12}' -> NO")