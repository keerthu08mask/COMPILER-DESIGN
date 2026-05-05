from collections import defaultdict
from grammar import grammar, start_symbol, EPSILON

ENDMARKER = '$'


class LL1Parser:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.non_terminals = list(grammar.keys())
        self.terminals = self.get_terminals()
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.parsing_table = defaultdict(dict)
        self.is_ll1 = True

    # ---------------- TERMINALS ----------------
    def get_terminals(self):
        terminals = set()
        for productions in self.grammar.values():
            for production in productions:
                for symbol in production:
                    if symbol not in self.grammar and symbol != EPSILON:
                        terminals.add(symbol)
        return terminals

    # ---------------- FIRST ----------------
    def compute_first(self):
        for terminal in self.terminals:
            self.first[terminal] = {terminal}

        for non_terminal in self.non_terminals:
            self.first[non_terminal] = set()

        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    before = len(self.first[nt])

                    if production == [EPSILON]:
                        self.first[nt].add(EPSILON)
                    else:
                        for symbol in production:
                            self.first[nt] |= (self.first[symbol] - {EPSILON})
                            if EPSILON not in self.first[symbol]:
                                break
                        else:
                            self.first[nt].add(EPSILON)

                    if len(self.first[nt]) > before:
                        changed = True

    # ---------------- FOLLOW ----------------
    def compute_follow(self):
        self.follow[self.start_symbol].add(ENDMARKER)

        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    for i in range(len(production)):
                        symbol = production[i]

                        if symbol in self.non_terminals:
                            before = len(self.follow[symbol])

                            if i + 1 < len(production):
                                next_symbol = production[i + 1]
                                self.follow[symbol] |= (self.first[next_symbol] - {EPSILON})

                                if EPSILON in self.first[next_symbol]:
                                    self.follow[symbol] |= self.follow[nt]
                            else:
                                self.follow[symbol] |= self.follow[nt]

                            if len(self.follow[symbol]) > before:
                                changed = True

    # ---------------- FIRST OF STRING ----------------
    def first_of_string(self, symbols):
        result = set()

        if symbols == [EPSILON]:
            return {EPSILON}

        for symbol in symbols:
            result |= (self.first[symbol] - {EPSILON})
            if EPSILON not in self.first[symbol]:
                return result

        result.add(EPSILON)
        return result

    # ---------------- PARSING TABLE ----------------
    def build_parsing_table(self):
        for nt in self.non_terminals:
            for production in self.grammar[nt]:
                first_set = self.first_of_string(production)

                for terminal in first_set - {EPSILON}:
                    if terminal in self.parsing_table[nt]:
                        self.is_ll1 = False
                    self.parsing_table[nt][terminal] = production

                if EPSILON in first_set:
                    for terminal in self.follow[nt]:
                        if terminal in self.parsing_table[nt]:
                            self.is_ll1 = False
                        self.parsing_table[nt][terminal] = production

    # ---------------- PRINT TABLE ----------------
    def print_table(self):
        terminals = sorted(list(self.terminals)) + [ENDMARKER]
        col_width = 18

        def print_line():
            print("+" + "+".join(["-" * col_width] * (len(terminals) + 1)) + "+")

        print("\nPredictive Parsing Table\n")

        print_line()

        # Header
        print("|" + "NT/T".center(col_width) + "|", end="")
        for t in terminals:
            print(t.center(col_width) + "|", end="")
        print()

        print_line()

        # Rows
        for nt in self.non_terminals:
            print("|" + nt.center(col_width) + "|", end="")
            for t in terminals:
                prod = self.parsing_table[nt].get(t, "")
                if prod:
                    prod_str = nt + " → " + " ".join(prod)
                    print(prod_str.center(col_width) + "|", end="")
                else:
                    print("".center(col_width) + "|", end="")
            print()
            print_line()

        # Final result
        if self.is_ll1:
            print("\nThe grammar IS LL(1)\n")
        else:
            print("\nThe grammar is NOT LL(1) (conflict detected)\n")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    parser = LL1Parser(grammar, start_symbol)
    parser.compute_first()
    parser.compute_follow()
    parser.build_parsing_table()
    parser.print_table()