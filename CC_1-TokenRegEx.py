
import re

N = int(input("Enter no.of Lines:" ))

pattern = r"[A-Za-z]+(?:['-][A-Za-z]+)*"

for _ in range(N):
    line = input("Enter text:")
    tokens = re.findall(pattern, line)

    print(len(tokens), *tokens)
