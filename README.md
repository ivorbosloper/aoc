# AOC
My Advent of Code solutions, see https://adventofcode.com/

## Usage

```
./run.py <year> <day>
./run.py 2022 6
```

## Structure

It's a minimal framework targeted at solving AoC problems.

- Input data (test data, prod-data) is a tuple in file `<year>/data.py` , in variable `a<day>` (e.g. `a6`). 
- The solutions are in file `<year>/advent<day>.py` (e.g. 2022/advent6.py) 

The run-script imports the input-data and calls function `f1(input)` and `f2(input)` in the solution file. f1 and f2 indicate the first half and second half of the problem. The return value of `f1` and `f2` is printed, but you're free to print your own stuff.

Add a function `def parse(input)` in the solution file to override input parsing, or add a `parse_line(line)` to parse lines.

## Example

Year 2000 day 1; The input consists of an integer per line, you should add all numbers. Second half of the problem is; you should add all squared input values.

In file `2000/data.py`:

```
a1 = ["""\
1
2
3""", """\
4
5
6"""]
```

In file `2000/advent1.py`:

```
parse_line = int

def f1(input):
  return sum(input)

def f2(input):
  return sum(i*i for i in input)
```
