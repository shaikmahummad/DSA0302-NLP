import re

def parse(expression):
    pattern = r'([A-Za-z]+)\(([^()]*)\)'

    match = re.fullmatch(pattern, expression.strip())

    if match:
        predicate = match.group(1)
        arguments = match.group(2).split(',')

        return {
            "Predicate": predicate,
            "Arguments": [arg.strip() for arg in arguments]
        }

    return "Invalid Logical Expression"

expression = input("Enter logical expression: ")

print(parse(expression))