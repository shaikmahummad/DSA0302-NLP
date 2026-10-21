
def vowel_groups(word):
    vowels = "aeiou"
    count = 0
    inside = False

    for c in word:
        if c in vowels:
            if not inside:
                count += 1
            inside = True
        else:
            inside = False

    return count


def doublable(word):
    vowels = "aeiou"

    return (
        len(word) >= 3
        and word[-3] not in vowels
        and word[-2] in vowels
        and word[-1] not in vowels
        and word[-1] not in "wxy"
        and vowel_groups(word) == 1
    )


def inflect(stem, feature):
    if feature in ("N+PL", "V+3SG"):
        if stem.endswith(("s", "x", "z", "ch", "sh")):
            return stem + "es"
        elif len(stem) >= 2 and stem[-1] == "o" and stem[-2] not in "aeiou":
            return stem + "es"
        elif stem.endswith("y") and len(stem) >= 2 and stem[-2] not in "aeiou":
            return stem[:-1] + "ies"
        return stem + "s"

    if feature == "V+PROG":
        if len(stem) >= 3 and stem.endswith("e") and stem[-2] not in "aeiou":
            return stem[:-1] + "ing"
        elif doublable(stem):
            return stem + stem[-1] + "ing"
        return stem + "ing"

    suffix = {
        "V+PAST": "ed",
        "ADJ+COMP": "er",
        "ADJ+SUP": "est"
    }

    end = suffix[feature]

    if stem.endswith("e"):
        return stem + end[1:]
    elif stem.endswith("y") and len(stem) >= 2 and stem[-2] not in "aeiou":
        return stem[:-1] + "i" + end
    elif doublable(stem):
        return stem + stem[-1] + end
    return stem + end


L = int(input())
lexicon = {}

for _ in range(L):
    stem, feature, form = input().split()
    lexicon[(stem, feature)] = form

Q = int(input())

for _ in range(Q):
    stem, feature = input().split()
    if (stem, feature) in lexicon:
        print(lexicon[(stem, feature)])
    else:
        print(inflect(stem, feature))
