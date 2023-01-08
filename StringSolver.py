import math

numbers = "1234567890"
chars = "+-/*^"
accept_chars = "SQRTINCPOEA|LGsqrtincepoalg()xX1234567890-+*/^."
letters = "SQRTINCOA|LGsqrtincoalg"
forbidden_chars = "ABCDEFHIJKMNPQRSTUVWXYZbdefhjkmuvwxyz%$#@!><,?='~`'\"_}{][\\"
func = ["sqrt", "sin", "cos", "tan", "||", "log"]

def check_chars(s):
    for i in range(len(s)):
        if s[i] not in accept_chars:
            return False
    return True

def derivativeString(s : str):
    derivative = [""]
    if s[0] == "-":
        derivative[-1] += s[0]
        s = s[1:]
    while s != "":
        if s[0] in chars.replace("^",""):
            derivative.append(s[0])
            derivative.append("")
            s = s[1:]
        else:
            derivative[-1] += s[0]
            s = s[1:]
    return derivative

def unKnowFunc(s : str, isx : bool = False):
    if isx:
        s = s.replace("x", "")
    s = s.replace("pi","").replace("e","")
    for f in range(len(func)):
        s = s.replace(func[f], "")
    for l in range(len(letters)):
        if letters[l] in s:
            return True
    return False

def recognize(s: str):
    for f in range(len(func)):
        if s.find(func[f]) == 0:
            if s.find(func[f] + "(") != 0:
                raise SyntaxError("you cant use " + func[f] + " like that")
            return [True, f]
        #else:
        #    print(s)
        #    raise SyntaxError("you dont use that right")
    return [False]

def recognizeInList(exe: list):
    for e in range(len(exe)):
        for f in range(len(func)):
            if exe[e].find(func[f]+"(") == 0:
                return [True,e, func[f]]
    return [False]

def isNone(exe):
    for i in range(len(exe)):
        if exe[i] == "None":
            return True
    return False

def DivideByZero(b):
    if b == 0:
        return True
    return False

def findBarckets(exe : list):
    for i in range(len(exe)):
        if exe[i][0] == "(":
            return i
    return None

def calculator(exe: list):
    if len(exe) == 1 and findBarckets(exe) is None and not recognizeInList(exe)[0]:
        if exe[0] == "None":
            return None
        elif float(exe[0]) % 1 == 0:
            return int(float(exe[0]))
        else:
            return float(exe[0])
    elif type(findBarckets(exe)) is int:
        exe[findBarckets(exe)] = str(calculator(ExerciseStringSolver(exe[findBarckets(exe)][1:][:-1])))
    elif recognizeInList(exe)[0]:
        try:
            if recognizeInList(exe)[2] == "sqrt":
                if StringCalculator(exe[recognizeInList(exe)[1]].removeprefix("sqrt")[1:][:-1]) < 0:
                    return None
                exe[recognizeInList(exe)[1]] = str(math.sqrt(StringCalculator(exe[recognizeInList(exe)[1]].removeprefix("sqrt")[1:][:-1])))
            elif recognizeInList(exe)[2] == "sin":
                exe[recognizeInList(exe)[1]] = str(math.sin(StringCalculator(exe[recognizeInList(exe)[1]].removeprefix("sin")[1:][:-1])))
            elif recognizeInList(exe)[2] == "cos":
                exe[recognizeInList(exe)[1]] = str(math.cos(StringCalculator(exe[recognizeInList(exe)[1]].removeprefix("cos")[1:][:-1])))
            elif recognizeInList(exe)[2] == "tan":
                try:
                    exe[recognizeInList(exe)[1]] = str(math.tan(StringCalculator(exe[recognizeInList(exe)[1]].removeprefix("tan")[1:][:-1])))
                except Exception:
                    return None
            elif recognizeInList(exe)[2] == "||":
                try:
                    exe[recognizeInList(exe)[1]] = str(math.fabs(StringCalculator(exe[recognizeInList(exe)[1]].removeprefix("||")[1:][:-1])))
                except Exception:
                    return None
            elif recognizeInList(exe)[2] == "log":
                try:
                    exe[recognizeInList(exe)[1]] = str(math.log(StringCalculator(exe[recognizeInList(exe)[1]].removeprefix("log")[1:][:-1])))
                except Exception:
                    return None
        except Exception:
            return None
    else:
        if not isNone(exe):
            oper = None
            if "^" in exe:
                try:
                    oper = exe.index("^")
                    if float(exe[oper - 1]) == 0 and float(exe[oper + 1]) < 0:
                        return None
                    else:
                        exe[oper - 1] = str(math.pow(float(exe[oper - 1]), float(exe[oper + 1])))
                except Exception:
                    print(f"{float(exe[oper - 1])} ^ {float(exe[oper + 1])}")
                    return None
            elif "*" in exe and "/" in exe:
                if exe.index("*") < exe.index("/"):
                    oper = exe.index("*")
                    exe[oper - 1] = str(float(exe[oper - 1]) * float(exe[oper + 1]))
                elif exe.index("*") > exe.index("/"):
                    oper = exe.index("/")
                    if not DivideByZero(float(exe[oper + 1])):
                        exe[oper - 1] = str(float(exe[oper - 1]) / float(exe[oper + 1]))
                    else:
                        return None
            elif "*" in exe:
                oper = exe.index("*")
                exe[oper - 1] = str(float(exe[oper - 1]) * float(exe[oper + 1]))
            elif "/" in exe:
                oper = exe.index("/")
                if not DivideByZero(float(exe[oper + 1])):
                    exe[oper - 1] = str(float(exe[oper - 1]) / float(exe[oper + 1]))
                else:
                    return None
            elif "+" in exe and "-" in exe:
                if exe.index("+") < exe.index("-"):
                    oper = exe.index("+")
                    exe[oper - 1] = str(float(exe[oper - 1]) + float(exe[oper + 1]))
                elif exe.index("+") > exe.index("-"):
                    oper = exe.index("-")
                    exe[oper - 1] = str(float(exe[oper - 1]) - float(exe[oper + 1]))
            elif "+" in exe:
                oper = exe.index("+")
                exe[oper - 1] = str(float(exe[oper - 1]) + float(exe[oper + 1]))
            elif "-" in exe:
                oper = exe.index("-")
                exe[oper - 1] = str(float(exe[oper - 1]) - float(exe[oper + 1]))
            if oper is not None:
                del exe[oper]
                del exe[oper]
        else:
            return None
    #print(exe)
    return calculator(exe)

def brackets(exe, s, isx = False):
    run = True
    while run:
        if s == "":
            run = False
            if exe[-1] != ")":
                raise SyntaxError("you forgot to end the brackets")
        elif s[0] == ")":
            exe[-1] += s[0]
            s = s[1:]
            run = False
        elif s[0] == "(":
            exe[-1] += s[0]
            s = s[1:]
            exe, s = brackets(exe, s, isx)
        elif recognize(s)[0]:
            exe[-1] += func[recognize(s)[1]]
            s = s.removeprefix(func[recognize(s)[1]])
            exe[-1] += s[0]
            s = s[1:]
            exe, s = brackets(exe, s, isx)
        elif s[0] in numbers or s[0] in chars or s[0] == ".":
            exe[-1] += s[0]
            s = s[1:]
        elif isx and (s[0] == "x" or s[0] == "X"):
            exe[-1] += s[0]
            s = s[1:]
    return [exe, s]

def ExerciseStringSolver(s="0", isx = False):
    s = s.lower()
    s = s.replace("j", "")
    s = s.replace("e", "")
    s = s.replace(" ", "")
    for i in range(len(forbidden_chars)):
        if isx and (forbidden_chars[i] == "x" or forbidden_chars[i] == "X"):
            continue
        if forbidden_chars[i] in s:
            raise ValueError("you cant use these chars in this function")

    if unKnowFunc(s, isx):
        raise SyntaxError("func not found")

    exercise = [""]
    if s[0] == "*"  or s[0] == "/":
        raise ValueError("you cant put + * or / in the start")
    elif s[0] == "-" or s[0] == "+":
        exercise[-1] += s[0] + "1"
        exercise.append("*")
        exercise.append("")
        s = s[1:]
    while s != "":
        if len(exercise[-1]) > 0 and s[0] in numbers and exercise[-1][-1] == ")":
            exercise.append("*")
            exercise.append(s[0])
            s = s[1:]
        elif s[0] in numbers or s[0] == ".":
            exercise[-1] += s[0]
            s = s[1:]
        elif isx and (s[0] == "x" or s[0] == "X"):
            exercise[-1] += s[0]
            s = s[1:]
        elif recognize(s)[0]:
            exercise[-1] += func[recognize(s)[1]]
            s = s.removeprefix(func[recognize(s)[1]])
            exercise[-1] += s[0]
            s = s[1:]
            exercise, s = brackets(exercise, s, isx)
        elif len(exercise[-1]) > 0 and s[0] == "(" and exercise[-1][-1] in numbers:
            exercise.append("*")
            exercise.append("")
            exercise[-1] += s[0]
            s = s[1:]
            exercise, s = brackets(exercise, s, isx)
        elif len(exercise[-1]) > 0 and s[0] == "(" and exercise[-1][-1] ==")":
            exercise.append("*")
            exercise.append("")
            exercise[-1] += s[0]
            s = s[1:]
            exercise, s = brackets(exercise, s, isx)
        elif len(exercise) > 0 and s[0] == "(" and exercise[-1] == "-":
            exercise[-1] += "1"
            exercise.append("*")
            exercise.append("")
            exercise[-1] += s[0]
            s = s[1:]
            exercise, s = brackets(exercise, s, isx)
        elif (s[0] == "+" or s[0] == "-") and exercise[-1] == "":
            exercise[-1] += s[0]
            s = s[1:]
        elif s[0] in chars:
            exercise.append(s[0])
            s = s[1:]
            exercise.append("")
        elif s[0] == "(":
            exercise[-1] += s[0]
            s = s[1:]
            exercise, s = brackets(exercise, s, isx)
        else:
            raise ValueError("forbbiden char")
    return exercise

def StringCalculator(s : str):
    s = s.replace("pi", str(math.pi))
    s = s.replace("e", str(math.e))
    return calculator(ExerciseStringSolver(s))

def main():
    print(StringCalculator("sin(0)"))

if __name__ == "__main__":
    main()