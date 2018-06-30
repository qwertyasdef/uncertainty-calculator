import math


class Measurement:

    def __init__(self, value, uncertainty):
        self.value = value
        self.uncertainty = abs(uncertainty)

    def __neg__(self):
        return Measurement(-self.value, self.uncertainty)

    def __add__(self, other):
        other = toMeasurement(other)
        return Measurement(
            self.value + other.value,
            self.uncertainty + other.uncertainty
        )

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        other = toMeasurement(other)
        return Measurement(
            self.value * other.value,
            (abs(self.uncertainty / self.value) + abs(other.uncertainty / other.value)) * self.value * other.value
        )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        other = toMeasurement(other)
        return Measurement(
            self.value / other.value,
            (abs(self.uncertainty / self.value) + abs(other.uncertainty / other.value)) * self.value / other.value
        )

    def __rtruediv__(self, other):
        return Measurement(1, 0) / (self / other)

    def __pow__(self, other):
        return Measurement(
            self.value ** other,
            self.uncertainty / self.value * other * self.value ** other
        )

    def __str__(self):
        return str(self.value) + " +- " + str(self.uncertainty)

    def __repr__(self):
        return self.__str__()


def toMeasurement(a):
    return Measurement(getattr(a, "value", a), getattr(a, "uncertainty", 0))


def func(f, m):
    return Measurement(
        f(m.value),
        max(
            abs(f(m.value + m.uncertainty) - f(m.value)),
            abs(f(m.value - m.uncertainty) - f(m.value)),
        )
    )


def trig(f, a):
    g = lambda x: f(math.radians(x))
    try:
        return func(g, a)
    except:
        return g(a)


def invTrig(f, a):
    g = lambda x: math.degrees(f(x))
    try:
        return func(g, a)
    except:
        return g(a)


if __name__ == "__main__":
    import re
    default = {
        "Measurement": Measurement,
        "sqrt": lambda x: x**0.5,
        "sin": lambda x: trig(math.sin, x),
        "cos": lambda x: trig(math.cos, x),
        "tan": lambda x: trig(math.tan, x),
        "asin": lambda x: invTrig(math.asin, x),
        "acos": lambda x: invTrig(math.acos, x),
        "atan": lambda x: invTrig(math.atan, x),
        "func": func,
        "math": math,
        "__builtins__": {},
    }
    namespace = default.copy()
    namespace["ans"] = None
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
            namespace["ans"] = eval(joined, namespace)
            print(namespace["ans"])
        except:
            namespace["ans"] = None
            try:
                exec(joined, namespace)
            except Exception as e:
                print(e)
