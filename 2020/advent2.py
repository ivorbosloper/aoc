import re

regex = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def parse_line(line):
    return regex.search(line).groups()


def f1(input):
    return sum(int(min_chars) <= string.count(char) <= int(max_chars) for min_chars, max_chars, char, string in input)


def f2(input):  # 815 is too high
    return sum((string[int(min_chars)-1] == char) ^ (string[int(max_chars)-1] == char)
               for min_chars, max_chars, char, string in input)
