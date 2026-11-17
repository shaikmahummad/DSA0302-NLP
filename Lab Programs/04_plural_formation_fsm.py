def plural(noun):
    state = 0

    if noun.endswith(('s', 'sh', 'ch', 'x', 'z')):
        state = 1
    elif noun.endswith('y') and len(noun) > 1 and noun[-2] not in 'aeiou':
        state = 2

    if state == 1:
        return noun + "es"
    elif state == 2:
        return noun[:-1] + "ies"
    else:
        return noun + "s"

word = input("Enter a noun: ")
print("Plural:", plural(word))