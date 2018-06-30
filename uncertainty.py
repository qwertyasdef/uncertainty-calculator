import math
import re
from measurement import Measurement


def sqrt(a):
    return a ** 0.5


def sin(a):
    f = lambda x: math.sin(math.radians(x))
    try:
        return a.func(f)
    except:
        return f(a)


def cos(a):
    f = lambda x: math.cos(math.radians(x))
    try:
        return a.func(f)
    except:
        return f(a)


def tan(a):
    f = lambda x: math.tan(math.radians(x))
    try:
        return a.func(f)
    except:
        return f(a)


def asin(a):
    f = lambda x: math.degrees(math.asin(x))
    try:
        return a.func(f)
    except:
        return f(a)


def acos(a):
    f = lambda x: math.degrees(math.acos(x))
    try:
        return a.func(f)
    except:
        return f(a)


def atan(a):
    f = lambda x: math.degrees(math.atan(x))
    try:
        return a.func(f)
    except:
        return f(a)


if __name__ == "__main__":
    default = {
        "Measurement": Measurement,
        "sqrt": sqrt,
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "asin": asin,
        "acos": acos,
        "atan": atan,
        "__builtins__": {},
    }
    namespace = default.copy()
    while True:
        namespace.update(default)
        expr = input(">>> ")
        split = re.split(r"(\d+\.?\d* *\+- *\d+\.?\d*)", expr)
        for i, s in enumerate(split):
            if "+-" in s:
                v, u = re.split(r" *\+- *", s)
                split[i] = "Measurement(" + v + ", " + u + ")"
        joined = "".join(split)
        try:
            print(eval(joined, namespace))
        except SyntaxError:
            try:
                exec(joined, namespace)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
