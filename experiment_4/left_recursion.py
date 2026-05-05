def remove_left_recursion(grammar):
    new_grammar = {}

    for non_terminal in grammar:
        productions = grammar[non_terminal]
        alpha = []
        beta = []

        for prod in productions:
            if prod.startswith(non_terminal):
                alpha.append(prod[len(non_terminal):].strip())
            else:
                beta.append(prod.strip())

        if alpha:
            new_nt = non_terminal + "'"
            new_grammar[non_terminal] = [b + " " + new_nt for b in beta]
            new_grammar[new_nt] = [a + " " + new_nt for a in alpha]
            new_grammar[new_nt].append("#")
        else:
            new_grammar[non_terminal] = productions

    return new_grammar


def read_grammar(filename):
    grammar = {}
    with open(filename, "r") as file:
        for line in file:
            left, right = line.split("->")
            left = left.strip()
            productions = [p.strip() for p in right.split("|")]
            grammar[left] = productions
    return grammar


if __name__ == "__main__":
    grammar = read_grammar("grammar_input.txt")
    new_grammar = remove_left_recursion(grammar)

    print("Grammar after removing Left Recursion:\n")
    for nt in new_grammar:
        print(f"{nt} -> {' | '.join(new_grammar[nt])}")