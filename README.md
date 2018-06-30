# Uncertainty calculator
A program to do uncertainty propagation calculations.

## Using the program
Run uncertainty.py and enter a math expression. Inexact values can be written as the value +- the uncertainty. Values without an uncertainty attatched are assumed to be exact. Press enter and the program will calculate the result with the appropriate uncertainty. For example:
```
>>> (10.5 +- 0.2) * (1.24 +- 0.03) + 7.34 +- 0.06
20.36 +- 0.623
```
The output will **not** automatically be rounded to the appropriate number of sig figs.

You can also store intermediate values into variables.
```
>>> a = (10.5 +- 0.2) * (1.24 +- 0.03) + 7.34 +- 0.06
>>> a
20.36 +- 0.623
>>> a / (1.25 +- 0.03)
16.288 +- 0.889312
```

Python keywords and certain reserved names cannot be used as variable names. If typing the name and hitting enter results in something other than `name 'variable' is not defined` then that variable name cannot be used.

Note that variables cannot be used as part of an inexact quantity. For example, this will not work:
```
>>> a = 2
>>> b = a +- 9
```
A `+-` must have numbers on both sides.

## Calculations
Here are how the program calculates uncertainties for each operation. Inexact inputs are denoted by x and y, an exact input is represented by n, and the output is z. A variable preceded by Δ means the uncertainty of that variable.

### Addition and subtraction:

z = x + y or z = x - y

Δz = Δx + Δy

### Multiplication and division:

z = x * y or z = x / y

|Δz / z| = |Δx / x| + |Δy / y|

### Exponentation:

z = x\*\*n

|Δz / z| = |n * Δx / x|

This only works for exact powers. An inexact value used in the exponent will cause an error.

### Other functions:

The function `sqrt` is available, though it is the same as just raising its argument to the power of 0.5.

The basic trigonometric functions sin, cos, and tan are supported and take their input in degrees. Inverse trig functions are also available as asin, acos, and atan and return an angle in degrees. Other functions can also be used by doing
```
>>> (1.04 +- 0.02).func(f)
```
where `f` can be any function that takes one input. The Python `math` library is accessible but must be used in this way.

The uncertainties for these functions are calculated as follows:

z = f(x)

Δz = max( f(x + Δx) - f(x), f(x - Δx) - f(x) )

The new uncertainty is the maximum possible deviation from the calculated value given the uncertainty of the input.
