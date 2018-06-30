class Measurement:

    def __init__(self, value, uncertainty):
        self.value = value
        self.uncertainty = abs(uncertainty)

    def __neg__(self):
        return Measurement(-self.value, self.uncertainty)

    def __add__(self, other):
        other = toM(other)
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
        other = toM(other)
        return Measurement(
            self.value * other.value,
            (self.uncertainty / self.value + other.uncertainty / other.value) * self.value * other.value
        )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        other = toM(other)
        return Measurement(
            self.value / other.value,
            (self.uncertainty / self.value + other.uncertainty / other.value) * self.value / other.value
        )

    def __rtruediv__(self, other):
        return Measurement(1, 0) / (self / other)

    def __pow__(self, other):
        return Measurement(
            self.value ** other,
            self.uncertainty / self.value * other * self.value ** other
        )

    def func(self, func):
        return Measurement(
            func(self.value),
            max(
                abs(func(self.value + self.uncertainty) - func(self.value)),
                abs(func(self.value - self.uncertainty) - func(self.value)),
            )
        )

    def __str__(self):
        return str(self.value) + " +- " + str(self.uncertainty)

    def __repr__(self):
        return self.__str__()


def toM(a):
    return Measurement(getattr(a, "value", a), getattr(a, "uncertainty", 0))
