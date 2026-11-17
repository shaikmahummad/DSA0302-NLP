import re

text = "Python is easy. Python is powerful. I love programming."

pattern = r"Python"

print(re.match(pattern, text))
print(re.search(pattern, text))
print(re.findall(pattern, text))
print(re.sub(pattern, "Java", text))