from io import StringIO
import re


def parse(input):
    result, tmp = [], []
    for line in StringIO(input):
        line = line.strip()
        if not line:
            result.append(tmp)
            tmp = []
        else:
            tmp.extend(line.split(" "))
    if tmp:
        result.append(tmp)
    return result


REQUIRED = {b.split(" ")[0] for b in """byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)""".split("\n")}
# cid (Country ID)


def print_valids(input, func):
    valids = sum((set(i.split(':')[0] for i in j if func(i)).issuperset(REQUIRED)) for j in input)
    print(valids)
    return valids


def f1(input):
    print_valids(input, lambda x: x)


def is_valid2(i):
    key, val = i.split(':')
    if key == 'byr':
        return val.isdigit() and 1920 <= int(val) <= 2002
    elif key == 'iyr':
        return val.isdigit() and 2010 <= int(val) <= 2020
    elif key == 'eyr':
        return val.isdigit() and 2020 <= int(val) <= 2030
    elif key == 'hgt':
        if m := re.fullmatch(r"(\d+)(in|cm)", val):
            h, unit = int(m.group(1)), m.group(2)
            return 150 <= h <= 193 if unit == 'cm' else 59 <= h <= 76
    elif key == 'hcl':
        return bool(re.fullmatch(r'#[0-9a-f]{6}', val))
    elif key == 'ecl':
        return val in ("amb blu brn gry grn hzl oth".split(" "))
    elif key == 'pid':
        return bool(re.fullmatch(r'\d{9}', val))
    return False


def f2(input):
    print_valids(input, is_valid2)


def is_valid2_test(i):
    result = is_valid2(i)
    print(f'{result}  {i}')
    return result


def test():
    input = parse("""\
    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
    
    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946
    
    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
    
    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007""")

    assert print_valids(input, is_valid2_test) == 0

    input = parse("""\
    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f
    
    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
    
    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022
    
    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""")

    assert print_valids(input, is_valid2_test) == 4


def test2():
    assert is_valid2_test("byr:2002")
    assert not is_valid2_test("byr:2003")

    assert is_valid2_test("hgt:60in")
    assert is_valid2_test("hgt:190cm")
    assert not is_valid2_test("hgt:190in")
    assert not is_valid2_test("hgt:190")

    assert is_valid2_test("hcl:#123abc")
    assert not is_valid2_test("hcl:#123abz")
    assert not is_valid2_test("hcl:123abc")

    assert is_valid2_test("ecl:brn")
    assert not is_valid2_test("ecl:wat")

    assert is_valid2_test("pid:000000001")
    assert not is_valid2_test("pid:0123456789")
