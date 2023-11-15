import math

class AdvancedCalculator:
    name = "MyAdvancedPythonCalculator"
    mem = {}

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def recursiveCalculation(self, calculation):
        if calculation.startswith("sin"):
            start = calculation.find("(")
            end = calculation.find(")")
            if start != -1 and end != -1:
                return math.sin(self.recursiveCalculation(calculation[start+1:end]))
            else:
                print(f"ERROR! {self.name} didn't understand `{calculation}`. You need to provide brackets.")
                return 0
        elif calculation.startswith("cos"):
            start = calculation.find("(")
            end = calculation.find(")")
            if start != -1 and end != -1:
                return math.cos(self.recursiveCalculation(calculation[start+1:end]))
            else:
                print(f"ERROR! {self.name} didn't understand `{calculation}`. You need to provide brackets.")
                return 0
        elif calculation.startswith("tan"):
            start = calculation.find("(")
            end = calculation.find(")")
            if start != -1 and end != -1:
                return math.tan(self.recursiveCalculation(calculation[start+1:end]))
            else:
                print(f"ERROR! {self.name} didn't understand `{calculation}`. You need to provide brackets.")
                return 0
        else:
            try:
                return float (calculation)
            except ValueError:
                print(f"ERROR! {self.name} didn't understand `{calculation}`.")
                return 0 

    def calc(self, calculation):
        if calculation == "help":
            print("All possibilities")
        else:
            print(self.recursiveCalculation(calculation))