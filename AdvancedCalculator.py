import math
import re

class AdvancedCalculator:
    name = "MyAdvancedPythonCalculator"
    mem = {}
    hist = [0]

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def recursiveCalculation(self, calculation):
        # regex = re.compile(r"\b(?P<single>[a-zA-Z0-9]+)\b")

        regex = re.compile(r"(?P<first>[a-zA-Z0-9,.]+)\s*(?P<op>|\+|-|\*|/|%)\s*(?P<second>[a-zA-Z0-9.,]+)")
        group = regex.search(calculation)
        try:
            op = group.group("op")
            first = float(group.group("first"))
            second = float(group.group("second"))
            if op == "+":
                return first + second
            elif op == "-":
                return first - second
            elif op == "*":
                return first * second
            elif op == "/":
                return first / second
            elif op == "%":
                return first % second
        except AttributeError or ValueError: # a group is unknown
            print("ERROR!")

        # if groups.group("op") == "+":
        #     print(groups.groupdict())
        #     return self.recursiveCalculation(groups.group("single")) + self.recursiveCalculation(groups.group("single"))
        # else:
        #     return int (groups.group("single"))

            # (?P<first>[a-zA-Z0-9]+)\s*(?P<op>(|\+|-|\*|/))\s*(?P<second>[a-zA-Z0-9]+)

            # (?P<single>([a-zA-Z0-9]+))\s*|(?P<first>[a-zA-Z0-9]+)\s*(?P<op>(|\+|-|\*|/))\s*(?P<second>[a-zA-Z0-9]+)

            # \s*(?P<single>[a-zA-Z0-9]+)\s* *(?P<op>[+|-|*|/])*


    def saveVar(self, calculation):
        varName = calculation[(len("saveAs ")):]
        self.mem[varName] = self.hist[len(self.hist)-1]

    def calc(self, calculation):
        if calculation == "help":
            print("All commands")
            print("  - `help`")
            print("  - `quit`")
            print("  - `saveAs [var]`; where `var` is the variable name")
            print("  - `erase`")
        elif calculation.startswith("saveAs "):
            self.saveVar(calculation)
        elif calculation == "erase":
            self.mem.clear()
            self.hist.clear()
        else:
            self.hist.append(self.recursiveCalculation(calculation))
            print(self.hist)


# regex:

### (?P<prefix>[\S]*)+sin?\s\((?P<sincontent>[0-9]*)\)(\s(?P<appendix>[\S]*))*