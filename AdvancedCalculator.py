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
        regex = re.compile(r"(?P<first>-?[a-zA-Z0-9,.]+)\s*((?P<op>|\+|-|\*|/|%|\^)\s*(?P<second>-?[a-zA-Z0-9.,]+))?")
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
            elif op == "^":
                return first ** second
        except: # `op` - or `second` - group is unkown -> This means `first` is a single
            return group.group("first")
        
    def TrigonometricFunctions(self, calculation):
        regex = re.compile(r".*(?P<op>(sin|asin|cos|acos|tan|atan|log))\s*\(\s*(?P<content>(.*))\s*\).*")
        group = regex.search(calculation)
        try:
            if group["op"] == "sin":
                return math.sin(float(self.simpleCalculation(group["content"])))
            elif group["op"] == "asin":
                return math.sinh(float(self.simpleCalculation(group["content"])))
            elif group["op"] == "cos":
                return math.cos(float(self.simpleCalculation(group["content"])))
            elif group["op"] == "acos":
                return math.cosh(float(self.simpleCalculation(group["content"])))
            elif group["op"] == "tan":
                return math.tan(float(self.simpleCalculation(group["content"])))
            elif group["op"] == "atan":
                return math.tanh(float(self.simpleCalculation(group["content"])))
            # Even though 'log' is not a Trigonometric Function, it is a three-letter functions, so in an attempt to create order, I put them together.
            elif group["op"] == "log":
                return math.log10(float(self.simpleCalculation(group["content"])))
            else:
                print("ERROR!")
                return float(group["content"])
        except:
            return float(self.simpleCalculation(calculation))
    
    def recursiveCalculation(self, calculation):
        # At this point, recursion is not implemented completely, so calling TrigonometricFunctions is neccessary at this point
        return self.TrigonometricFunctions(calculation)

    def saveVar(self, calculation):
        varName = calculation[(len("saveAs ")):]
        self.mem[varName] = self.hist[len(self.hist)-1]

    def calc(self, calculation):
        if calculation == "help":
            print("All commands")
            print("  - `help`")
            print("  - `quit`")
            print("  - `saveAs [var]`; where `var` is the variable name")
            print("  - `mem`")
            print("  - `erase`")
        elif calculation.startswith("saveAs "):
            self.saveVar(calculation)
        elif calculation == "erase":
            self.mem.clear()
            self.hist.clear()
        elif calculation == "mem":
            print("All items in memory:")
            for key, value in self.mem.items():
                print(f"  {key} = {value}")
        else:
            self.hist.append(self.recursiveCalculation(calculation))
            print(self.hist[-1])