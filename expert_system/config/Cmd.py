import argparse
import sys


class Cmd:
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", choices=['shell', 'interactive', 'interface'], default='mode_shell', help="Interface mode")
    parser.add_argument("-r", "--rules", action='store_true', help="Displays the rules")
    parser.add_argument("-v", "--verbose", action='store_true', help="Displays the steps of the resolution")
    parser.add_argument("input", nargs='?', help="The file containing rules, facts and queries")

    args = parser.parse_args()
