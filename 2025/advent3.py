
def f1(input):
    result = []
    for line in input:
        mx = 0
        mx_digit = 0
        for digit in line:
            digit = int(digit)
            if mx_digit + digit > mx:
                mx = mx_digit + digit
            if digit * 10 > mx_digit:
                mx_digit = digit * 10
        result.append(mx)

    return sum(result)

def f2(input):
    result = []
    for line in input:
        mx = 13 * [0]
        # mx[i] is het hoogste getal dat je met i digits kunt maken
        for digit in line:
            digit = int(digit)
            for i in range(12, 0, -1):
                can_make = mx[i-1] * 10 + digit
                if can_make > mx[i]:
                    mx[i] = can_make
        result.append(mx[12])

    return sum(result)
