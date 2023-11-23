# AdvancedCalculator
An advanced calculator, powered by Python

**Thijs Dregmans**

Last updated on 2023-11-23

## Course

This Python calculator is made for a bonus course, in the Technische Informatica program.

## Goal

The goal of this calculator is, both to learn more about Object Oriented Programming in Python, and to complete the course.

## Installations

The calculator is written in Python. Python is a interpreter language. This means, you need install Python.
This calculator is specifically designed for and built in 'Python 3.11.1'.

### Libaries

This calculator uses two standard libaries:

- `re` 
- `math`

Both do not require additional installations, besides Python '3.11.1'.

## Architecture

In `main.py`, a `AdvancedCalculator`-object is created. The user input is fed to this object with the `calc()` method.
In the `AdvancedCalculator.calc()` method, the user input is validated and scanned for calculations and/or commands.

This method then calls other methods and carries out the tasks that need to be done.

## User manual

### Commands

The user has several commands, he/she can use:

- `help` provides the user with information about the available commands.
- `quit` stops the calculator.
- `saveAs` saves the previous value to a temporary memory cell. This command takes the name of the variable as argument.
- `mem` print the memory to the user.
- `erase` erases the content of the memory cells.

### Calculations

#### Simple calculations

A calculator is useless, if it cannot perform calculations.
This calculator accepts the most common operators:

- `+` adds two arguments. (infix operator)
- `-` substracts two arguments. (infix operator)
- `*` multiplies two arguments. (infix operator)
- `/` divides two arguments. (infix operator)
- `%` calculates the mode of two arguments. (infix operator)
- `^` powers the first argument by the second. (infix operator)

#### Functions

This version also introduces functions:

- `sin(x)` returns the sinus of `x`. (function)
- `asin(x)` returns the arcsinus of `x`. (function)
- `cos(x)` returns the cosinus of `x`. (function)
- `acos(x)` returns the arccosinus of `x`. (function)
- `tan(x)` returns the tangent of `x`. (function)
- `atan(x)` returns the arctangent of `x`. (function)

- `log(x)` return the 10th log of `x`. (function)

In all these function, `x` can be a integer, float, or a calculation, for example `sin(4 + 4)` is possible, just like `sin(8)`.
