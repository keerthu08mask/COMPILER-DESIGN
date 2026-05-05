from collections import defaultdict


# -------------------------
# Read Grammar from File
# -------------------------
def read_grammar(filename):
    grammar = defaultdict(list)

    with open(filename, "r") as file:
        for line in file:
            if "->" not in line:
                continue
            left, right = line.split("->")
            left = left.strip()
            productions = [p.strip().split() for p in right.split("|")]
            grammar[left].extend(productions)

    return grammar


# -------------------------
# Compute FIRST Sets (Iterative)
# -------------------------
def compute_first(grammar):
    first = defaultdict(set)

    # Add terminals to their own FIRST set
    for nt in grammar:
        for production in grammar[nt]:
            for symbol in production:
                if symbol not in grammar:   # Terminal
                    first[symbol].add(symbol)

    changed = True

    while changed:
        changed = False

        for nt in grammar:
            for production in grammar[nt]:

                for symbol in production:
                    before = len(first[nt])

                    # Add FIRST(symbol) except epsilon
                    first[nt].update(first[symbol] - {"#"})

                    # If epsilon not in FIRST(symbol), stop
                    if "#" not in first[symbol]:
                        break
                else:
                    # If all symbols contain epsilon
                    first[nt].add("#")

                if before != len(first[nt]):
                    changed = True

    return first


# -------------------------
# Compute FOLLOW Sets (Iterative)
# -------------------------
def compute_follow(grammar, first):
    follow = defaultdict(set)

    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add("$")

    changed = True

    while changed:
        changed = False

        for nt in grammar:
            for production in grammar[nt]:
                for i in range(len(production)):

                    symbol = production[i]

                    if symbol in grammar:  # Non-terminal

                        before = len(follow[symbol])

                        # Case 1: Not last symbol
                        if i + 1 < len(production):
                            next_symbol = production[i + 1]

                            # Add FIRST(next) except epsilon
                            follow[symbol].update(first[next_symbol] - {"#"})

                            # If epsilon in FIRST(next), add FOLLOW(nt)
                            if "#" in first[next_symbol]:
                                follow[symbol].update(follow[nt])

                        else:
                            # Case 2: Last symbol
                            follow[symbol].update(follow[nt])

                        if before != len(follow[symbol]):
                            changed = True

    return follow


# -------------------------
# Main Execution
# -------------------------
if __name__ == "__main__":

    grammar = read_grammar("grammar_input.txt")

    first = compute_first(grammar)
    follow = compute_follow(grammar, first)

    print("\nFIRST Sets:\n")
    for nt in grammar:
        print(f"{nt} : {first[nt]}")

    print("\nFOLLOW Sets:\n")
    for nt in grammar:
        print(f"{nt} : {follow[nt]}")