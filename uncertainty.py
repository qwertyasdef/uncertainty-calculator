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


# Convert numbers to numbers with uncertainties
def toMeasurement(a):
    return Measurement(getattr(a, "value", a), getattr(a, "uncertainty", 0))


# Apply an arbitrary function
def func(f, m):
    return Measurement(
        f(m.value),
        max(
            abs(f(m.value + m.uncertainty) - f(m.value)),
            abs(f(m.value - m.uncertainty) - f(m.value)),
        )
    )


# Trig functions in degrees
def trig(f, a):
    g = lambda x: f(math.radians(x))
    try:
        return func(g, a)
    except:
        return g(a)


# Inverse trig functions return degrees
def invTrig(f, a):
    g = lambda x: math.degrees(f(x))
    try:
        return func(g, a)
    except:
        return g(a)


if __name__ == "__main__":
    import re
    # Functions that shouldn't be overwritten
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
    # Namespace for eval and exec
    namespace = default.copy()
    # namespace["ans"] should always contain the result of the previous expression
    namespace["ans"] = None
    while True:
        # Replace functions that may have been overwritten
        namespace.update(default)
        # Get user input
        expr = input(">>> ")
        # Replace a +- b with Measurement(a, b)
        expr = re.sub(
            r"(\d+\.?\d*([Ee]-?\d+)?) *\+- *(\d+\.?\d*([Ee]-?\d+)?)",
            r"Measurement(\1, \3)",
            expr
        )
        # Evaluate the expression
        try:
            # Calculate the result, stor it in ans, and display it
            namespace["ans"] = eval(expr, namespace)
            print(namespace["ans"])
        except:
            # The expression was not an expression
            namespace["ans"] = None
            try:
                # Maybe it was a variable assignment
                exec(expr, namespace)
            except Exception as e:
                # Not valid, show error
                print(e)
