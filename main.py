### main.py ###

### Author: Thijs Dregmans 
### Last edited on: 2023-11-17
### Version: 1.1

### Goal: to learn more about OOP Python 
### and to complete the introduction course.

import math
import AdvancedCalculator as AC

def main():
    # Create a calcuator
    calculator = AC.AdvancedCalculator("Thijs' Calculator")

    print("####################################################")
    print("############### The AdvancedCalcuator ##############")
    print("####################################################")
    print("# Use this calculator to solve your math problems. #")
    print("# Try `help` to learn more                         #")
    print("# Try `quit` to stop using the calcuator           #")
    print("####################################################")


    text = input(">  ")
    while text != "quit":
        calculator.calc(text)
        text = input(">  ")

if __name__ == "__main__":
    main()