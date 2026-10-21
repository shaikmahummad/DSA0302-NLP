
n, k = map(int, input().split())
alphabet = input().split()
start = int(input())

data = list(map(int, input().split()))
accepting = set(data[1:])

t = int(input())
transitions = {}

for _ in range(t):
    p, c, r = input().split()
    p, r = int(p), int(r)

    if (p, c) not in transitions:
        transitions[(p, c)] = set()

    transitions[(p, c)].add(r)

Q = int(input())

for _ in range(Q):
    s = input()
    if s == "#":
        s = ""

    current = {start}

    for c in s:
        next_states = set()

        for state in current:
            next_states.update(transitions.get((state, c), set()))

        current = next_states

    if current & accepting:
        print("ACCEPT")
    else:
        print("REJECT")

