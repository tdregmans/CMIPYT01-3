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
    
    def simpleCalculation(self, calculation):
        regex = re.compile(r"(?P<first>-?[a-zA-Z0-9,.]+)\s*((?P<op>|\+|-|\*|/|%)\s*(?P<second>-?[a-zA-Z0-9.,]+))?")
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
            else:
                print("ERROR!")
                print("Unknown operator: {op}")
                return None
        except: # `op` - or `second` - group is unkown -> This means `first` is a single
            print("ERROR!")
            return float(group.group("first"))
        
    def TrigonometricFunctions(self, calculation):
        regex = re.compile(r".*(?P<op>(sin|sinh|cos|cosh|tan|tanh|log))\s*\(\s*(?P<content>(.*))\s*\).*")
        group = regex.search(calculation)
        if group["op"] == "sin":
            return math.sin(float(self.simpleCalculation(group["content"])))
        elif group["op"] == "sinh":
            return math.sinh(float(self.simpleCalculation(group["content"])))
        elif group["op"] == "cos":
            return math.cos(float(self.simpleCalculation(group["content"])))
        elif group["op"] == "cosh":
            return math.cosh(float(self.simpleCalculation(group["content"])))
        elif group["op"] == "tan":
            return math.tan(float(self.simpleCalculation(group["content"])))
        elif group["op"] == "tanh":
            return math.tanh(float(self.simpleCalculation(group["content"])))
        # Even though 'log' is not a Trigonometric Function, it is a three-letter functions, so in an attempt to create order, I put them together.
        elif group["op"] == "log":
            return math.log10(float(self.simpleCalculation(group["content"])))
        else:
            print("ERROR!")
            return float(group["content"])
        
    
    def recursiveCalculation(self, calculation):
        # remove priority
        regex = re.compile(r"\((?P<first>[\S\s]*)\)\s*((?P<op>|\+|-|\*|/|%)\s*(?P<second>-?[a-zA-Z0-9.,]+)|(?P<op1>|\+|-|\*|/|%)\s*(?P<second1>[\S\s]*))*")
        # regex = re.compile(r"\((?P<first>.*)\)\s*((?P<op>|\+|-|\*|/|%)\s*(?P<second>-?[a-zA-Z0-9.,]+)|(?P<op1>|\+|-|\*|/|%)\s*(?P<second1>.*))*")
        group = regex.findall(calculation) 
        print(group)

        return self.TrigonometricFunctions(calculation)
        # op = group.("op")
        # print(op)

        # regex = re.compile(r"(?P<first>[a-zA-Z0-9,.]+)\s*(?P<op>|\+|-|\*|/|%)\s*(?P<second>[a-zA-Z0-9.,]+)")
        # group = regex.search(calculation)
        # try:
        #     op = group.group("op")
        #     first = float(group.group("first"))
        #     second = float(group.group("second"))
        #     if op == "+":
        #         return first + second
        #     elif op == "-":
        #         return first - second
        #     elif op == "*":
        #         return first * second
        #     elif op == "/":
        #         return first / second
        #     elif op == "%":
        #         return first % second
        # except AttributeError or ValueError: # a group is unknown
        #     print("ERROR!")

    # optional
        # if groups.group("op") == "+":
        #     print(groups.groupdict())
        #     return self.recursiveCalculation(groups.group("single")) + self.recursiveCalculation(groups.group("single"))
        # else:
        #     return int (groups.group("single"))

            # (?P<first>[a-zA-Z0-9]+)\s*(?P<op>(|\+|-|\*|/))\s*(?P<second>[a-zA-Z0-9]+)

            # (?P<single>([a-zA-Z0-9]+))\s*|(?P<first>[a-zA-Z0-9]+)\s*(?P<op>(|\+|-|\*|/))\s*(?P<second>[a-zA-Z0-9]+)

            # \s*(?P<single>[a-zA-Z0-9]+)\s* *(?P<op>[+|-|*|/])*
        
        '''
        needed functions:
            simple calculations:                \((?P<first>.*)\)\s*((?P<op>|\+|-|\*|/|%)\s*(?P<second>-?[a-zA-Z0-9.,]+)|(?P<op1>|\+|-|\*|/|%)\s*(?P<second1>.*))*
                x + y
                x - y
                x * y
                x / y
            other calculations:   Niet getest   \((?P<first>.*)\)\s*((?P<op>|\+|-|\*|/|%|**)\s*(?P<second>-?[a-zA-Z0-9.,]+)|(?P<op1>|\+|-|\*|/|%)\s*(?P<second1>.*))*
                x % y
                x ** y
            arthritmic functions:               .*(?P<op>(sin|cos|tan|log))\s*\(\s*(?P<content>(.*))\s*\).*
                sin x
                cos x
                tan x
                log x
            priority:
                (x + y) * z
                x + (y / z)
            combinations:
                x + (sin y / z)
            sets:
                {x, y, z}
            constants:
                e
                pi
            plots:
                functions
                tables
                traces

            others:
                sum
                product
                ABC-formula
                absolute value
                rounding
                remainder
                max
                min
                factorial
                

        '''


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
            print(self.hist[-1])


# regex:

### (?P<prefix>[\S]*)+sin?\s\((?P<sincontent>[0-9]*)\)(\s(?P<appendix>[\S]*))*