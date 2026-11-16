
def is_consonant(word, i):
    c = word[i]

    if c in "aeiou":
        return False

    if c == "y":
        if i == 0:
            return True
        return not is_consonant(word, i - 1)

    return True


def measure(word):
    m = 0
    previous_vowel = False

    for i in range(len(word)):
        vowel = not is_consonant(word, i)

        if previous_vowel and not vowel:
            m += 1

        previous_vowel = vowel

    return m


def has_vowel(word):
    for i in range(len(word)):
        if not is_consonant(word, i):
            return True
    return False


def double_consonant(word):
    return (
        len(word) >= 2
        and word[-1] == word[-2]
        and is_consonant(word, len(word) - 1)
    )


def cvc(word):
    if len(word) < 3:
        return False

    n = len(word)

    return (
        is_consonant(word, n - 3)
        and not is_consonant(word, n - 2)
        and is_consonant(word, n - 1)
        and word[-1] not in "wxy"
    )


def porter_step1(word):
    # Step 1a
    if word.endswith("sses"):
        word = word[:-2]
    elif word.endswith("ies"):
        word = word[:-2]
    elif word.endswith("ss"):
        pass
    elif word.endswith("s"):
        word = word[:-1]

    # Step 1b
    if word.endswith("eed"):
        stem = word[:-3]
        if measure(stem) > 0:
            word = stem + "ee"

    elif word.endswith("ed") and has_vowel(word[:-2]):
        word = word[:-2]
        word = cleanup(word)

    elif word.endswith("ing") and has_vowel(word[:-3]):
        word = word[:-3]
        word = cleanup(word)

    # Step 1c
    if word.endswith("y") and has_vowel(word[:-1]):
        word = word[:-1] + "i"

    return word


def cleanup(word):
    if word.endswith(("at", "bl", "iz")):
        return word + "e"

    if double_consonant(word) and word[-1] not in "lsz":
        return word[:-1]

    if measure(word) == 1 and cvc(word):
        return word + "e"

    return word


Q = int(input())

for _ in range(Q):
    word = input().strip()
    print(porter_step1(word))
