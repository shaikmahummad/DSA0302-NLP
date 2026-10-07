def finite_automaton(string):
    state = "q0"
    path = [state]

    for symbol in string:
        if symbol not in "ab":
            return False, path, "Invalid symbol"

        if state == "q0":
            if symbol == "a":
                state = "q1"
            else:
                state = "q0"

        elif state == "q1":
            if symbol == "a":
                state = "q1"
            else:
                state = "q0"

        path.append(state)

    accepted = (state == "q1")
    return accepted, path, state


strings = ["a", "b", "aba", "abb", "baa", "bab", "aa"]

for string in strings:
    accepted, path, final_state = finite_automaton(string)

    print("\nInput:", string)
    print("Path:", " -> ".join(path))
    print("Final state:", final_state)

    if accepted:
        print("Result: ACCEPTED")
    else:
        print("Result: REJECTED")