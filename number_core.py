#!/bin/bash/python
"""
- Steps to find a numeric core -

- Take any number with four or more digits. Without changing the sequence, split
    that number into four smaller numbers. (ex. 86455 becomes 8 6 45 5)
- Next, assign each a different color, resulting in a valid mathematical
    equation that produces the smallest whole number possible. The first number
    should always be assigned teal to begin with a positive number.
    (ex. + 8 - 6 x 45 / 5)
- If the result is a number with more than three digits, repeat the above
    process. The final number you obtain that is less than four digits is
    considered the "numeric core" of the larger number. (ex. 18)
"""

# built-in imports
from itertools import combinations, permutations
import logging
from logging.config import dictConfig
import os
import sys

# pip installed imports
import yaml  # type: ignore

# custom imports

# Start logging
current_dir = os.path.dirname(__file__)
with open(os.path.join(current_dir, "config/logging_config.yaml"), "rt") as f:
    try:
        config = yaml.safe_load(f.read())
        dictConfig(config)
    except Exception as e:
        print(e)
        print("Error in Logging Configuration.")
        sys.exit()
logger = logging.getLogger(__name__)

# Establish global variables


def execute():
    valid = False
    inputs = []
    smallest_num = -1
    operation = []
    smallest = False

    while not valid:
        inputs = num_inputs()
        valid = validate(inputs)

    while not smallest:
        smallest_num, operation = calc_number_core(inputs)

        if smallest_num == -1:
            logger.info("Could not find a number core.")
            break
        elif 0 < smallest_num < 1000:
            smallest = True
        else:
            logger.info(f"Current Smallest number: {smallest_num}")
            inputs = [int(i) for i in str(smallest_num)]
            valid = validate(inputs)
            if not valid:
                logger.info("How did this happen?")
                sys.exit()

    logger.info(f"Result: {smallest_num}")
    logger.info(f"Correct operations: {operation}")


def num_perms(num):
    numbers = list(str(num))
    num_combs = []
    final = []
    for i, j in combinations(range(len(numbers) + 1), 2):
        num_combs.append(numbers[i:j])

    print(final)


def validate(inputs):
    logger.info(f"You entered: {inputs[0]}, {inputs[1]}, {inputs[2]}, {inputs[3]}")

    correct = input("Is this correct? (y/n): ")

    if correct.lower() == "n":
        valid = False
    elif correct.lower() == "y":
        valid = True
    else:
        logger.info(f"Please enter an appropriate option (y/n).")
        valid = False

    return valid


def calc_number_core(inputs):
    ops = []
    operation = []
    smallest_num = -1

    [ops.append(item) for item in list(permutations(["-", "*", "\\"]))]

    for item in ops:
        total = inputs[0]

        if ops.index(item) == 0:
            operation = item

        logger.debug(f"Current ops: {item}")
        logger.debug(f"Current total: {total}")

        for num, op in zip(inputs[1:], item):
            logger.debug(f"Num: {num}, Op: {op}")

            if op == "-":
                logger.debug("Performing subtraction.")
                total = sub_nums(total, num)
                logger.debug(f"Current total: {total}")
            elif op == "*":
                logger.debug("Performing multiplication.")
                total = mult_nums(total, num)
                logger.debug(f"Current total: {total}")
            elif op == "\\":
                logger.debug("Performing division.")

                if num == 0:
                    logger.debug("Cannot divide by 0.")
                    break
                else:
                    total = div_nums(total, num)

                logger.debug(f"Current total: {total}")

        logger.debug(f"Final total: {total}")

        if smallest_num == -1 or total < smallest_num:
            if total > 0 and total % 1 == 0:
                logger.debug("The number fits the criteria.")
                smallest_num = int(total)
                operation = item

        logger.debug(f"Current smallest num: {smallest_num}")
        logger.debug(f"Current correct operations: {operation}")

    return (smallest_num, operation)


def num_inputs():
    num1 = input("Enter the first number: ")
    num2 = input("Enter the second number: ")
    num3 = input("Enter the third number: ")
    num4 = input("Enter the fourth number: ")

    return [int(num1), int(num2), int(num3), int(num4)]


def add_nums(x, y):
    return x + y


def sub_nums(x, y):
    return x - y


def mult_nums(x, y):
    return x * y


def div_nums(x, y):
    return x / y


if __name__ == "__main__":
    logger.info("Starting the numeric core caluclator.")

    run = True

    while run:
        ans = input("Do you want to check for a number core? (y/n): ")

        if ans.lower() == "y":
            execute()
        elif ans.lower() == "n":
            run = False
        else:
            logger.info("Please enter a correct value. ('y' or 'n')")

    logger.info("Thank you for using the numeric core calculator.")
