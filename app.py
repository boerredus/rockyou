import argparse
import itertools
import os
import sys
import re

import utils

def parse_args():
    abspath = os.path.abspath(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(
        description='Combination-based password generator')
    parser.add_argument('-p', '--path', type=str, default=abspath,
                        help=f'Path to store password file on (without filename). Defaults to {abspath}')
    parser.add_argument('-f', '--file', type=str, default='rockyou.txt', help='File name with extension. Defaults to rockyou.txt')
    parser.add_argument('-l', '---disable-lowercase', action='store_true',
                        help='If given, will not include lowercase letters on (default) character set')
    parser.add_argument('-U', '---disable-uppercase', action='store_true',
                        help='If given, will not include uppercase letters on (default) character set')
    parser.add_argument('-n', '---disable-numbers', action='store_true',
                        help='If given, will not include numbers on (default) character set')
    parser.add_argument('-c', '---disable-special-chars', action='store_true',
                        help='If given, will not include special characters on (default) character set')
    parser.add_argument('-d', '---disable-chars', type=list, default=False,
                        help='Disable a certain set of characters from the default character set')
    parser.add_argument('-C', '--character-set', type=list, default=['*', '.', '?', '@', '#', '$', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                                                                     'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], help="Character set to be used. Defaults to *.?@#$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    parser.add_argument('-m', '---minimum-length', type=int, default=4,
                        help='Minimum length of passwords (including the given number). Defaults to 4')
    parser.add_argument('-M', '---maximum-length', type=int, default=16,
                        help='Maximum length of passwords (including the given number). Defaults to 16')
    parser.add_argument('-s', '--separator', type=str, default=',',
                        help=r'Separator of combinations. Use "\n" to use a linebreak as a separator. Defaults to a comma')
    parser.add_argument('---estimate-size', action='store_true',
                        help='Will print the esitmated end-file size and exit')
    parser.add_argument('---estimate-time', action='store_true',
                        help='Will print the estimated time it would take to generate the end-file and exit')
    parser.add_argument('---estimate-ammount', action='store_true',
                        help='Will print the ammount of different combination to be generated and exit')
    parser.add_argument('-e', '--estimate', action='store_true',
                        help='Alias to ---estimate-size ---estimate-time ---estimate-ammount')

    args = parser.parse_args()
    if args.disable_lowercase:
        args.character_set = list(filter(
            lambda c: not re.search(r'[a-z]', c), args.character_set))

    if args.disable_uppercase:
        args.character_set = list(filter(
            lambda c: not re.search(r'[A-Z]', c), args.character_set))

    if args.disable_numbers:
        args.character_set = list(filter(
            lambda c: not re.search(r'[0-9]', c), args.character_set))

    if args.disable_special_chars:
        args.character_set = list(filter(
            lambda c: not c in ['*', '.', '?', '@', '#', '$'], args.character_set))

    if args.disable_chars:
        args.character_set = list(filter(
            lambda c: not c in args.disable_chars, args.character_set))

    return args


def main() -> int:
    args = parse_args()
    args.path = args.path[0:-1] if args.path[-1] == '/' else args.path
    args.separator = '\n' if args.separator == r'\n' else args.separator
    estimator = utils.Estimator(args)

    if args.estimate:
        return print(estimator.estimate()) or 0
    elif args.estimate_size or args.estimate_time or args.estimate_ammount:
        if args.estimate_size:
            return print(estimator.estimate_size()) or 0
        elif args.estimate_time:
            return print(estimator.estimate_time()) or 0
        elif args.estimate_ammount:
            return print(estimator.estimate_ammount()) or 0

    with open(f'{args.path}/{args.file}', 'w') as f:
        for i in range(args.minimum_length, args.maximum_length + 1):
            for c in itertools.product(args.character_set, repeat=i):
                f.write(utils.join(c, args.separator))

    with open(f'{args.path}/{args.file}', 'rb+') as f:
        f.seek(-1, os.SEEK_END)
        f.truncate()

    return 0


if __name__ == '__main__':
    sys.exit(main())
