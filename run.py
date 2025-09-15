#!/usr/bin/env python3
"""
@author: Marek Putala

"""

# libraries

from src.main_module import main as main_run
import argparse
import sys
import re
import unittest

# function for parsing command-line arguments

def arg_parser():
    parser = argparse.ArgumentParser(
        description="A simple script for extracting data from webs"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        dest="test",
        help="Run unit tests instead of main program",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        type=str,
        help="Path to file containing URLs (otherwise URLs are read from stdin)",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        help="Path to output file (otherwise results are printed to stdout)",
    )
    return parser.parse_args()


# function for extracting input string from a file or stdin

def get_input(input_file):
    if input_file is None:
        data = sys.stdin.read()
    else:
        # try to open a file and read its contents

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    # remove all whitespace and store all words in an array

    words = re.split(r"\s+", data.strip())
    return words


# function to write processed data to a file or stdout based on arguments

def set_output(output_file, output):
    s_output = ""
    # process all collected data into a structured string

    for o in output:
        s_output = s_output + o[0] + ": "
        if len(o[1]) == 0:
            continue
        for url in o[1]:
            s_output = s_output + url + ", "
        s_output = s_output[:-2] + "\n"
    # write data to a file if a filename is specified, otherwise print to stdout

    if output_file is None:
        print(s_output)
    else:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(s_output)
        except Exception as e:
            print(f"An error occurred: {e}")


# main function for controlling the program

def main():
    # part for parsing input arguments

    args = arg_parser()
    run_tests = args.test
    input_file = args.input
    output_file = args.output
    # if the --test argument is not provided, run the main module with real data and URLs

    if not run_tests:
        urls = get_input(input_file)
        output = main_run(urls)
        set_output(output_file, output)
    # if the --test argument is provided, run unit tests using mocks and fake data

    else:
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir="tests", pattern="test_*.py")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        if result.wasSuccessful():
            print("All tests passed!")
        else:
            print("Some tests failed.")


if __name__ == "__main__":
    main()
