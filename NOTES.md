# Performance Engineering #1 - The basics

Very basic high-level performance engineering talk.

When we are “Optimizing Performance” what are we optimizing For?

We can set

- Throughput
- Memory Usage
- Concurrency
- Latency
- Persistent Storage
- Predictablity

as targets and optimize toward the others. Very often there are trade-offs we have to consider.
These are real-world coniderations, economical or scientific in nature.
For example: More RAM is often cheaper than a better CPU.

Moreover scaling CPUs is harder than scaling RAM, hence "caching" is very prevalent.
It might become impossible to increase CPU clock speeds so we have to start computing
in parallel - and that might not be possible at all.

## throttling

Semiconductors will increase in conductivity and eventually burn out, the hotter they get.
This means all long-running semi-conducting devices need some sort of negative feedback
with every increase in temperature. Thermal throttling.
Usually this is accomplished via low-level firmware coupled with at least one temperature
sensor within the device assembly. On mobile devices like laptops throttling might
also occur with the decrease of battery voltage and charge.

Consider this plot of a sorting-algorithm benchmark.
![TT](/assets/thermalt.png)

This image is taken from an MIT Courseware Lecture.
https://www.youtube.com/watch?v=LvX3g45ynu8
License: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

## measuring the interpreter/linker/vm-startup etc.

Its tempting to write or compile a program and benchmark it directly from your shell:

```bash
time pytest -k test_python_too_fast -q
```

As you can see from the output of that command: this is not ideal. If you were measuring a simple
C program the measurement would (probably) include the time it takes for the operating system to start the
process and some overhead by the c binary itself like [linking libaries](https://www.lurklurk.org/linkers/linkers.html).
Because we are measuring a python program, this will include all sorts of whacky things we
dont need to worry about.

_Loading and starting the interpreter, loading program files from disk, parsing them, writing byte code to disk for caching ..._

_Note: Switch Python Versions_

```
poetry env use 3.10
poetry install

poetry env use 3.13
poetry install
```

Something very useful howerver, is to see how much time the program has spent in the kernel ("system"). All the time used by sys-calls is listed on its own which might indicate
performance problems connected to writing files, listening on the network and more.

## benchmarks are "too fast"

When measuring performance of a function that is too fast and running it only once, you might end up measuring a siginifcant error introduced by (for example) process scheduling in the operating system. Other overhead like GCs, file-systems, etc. might also play into this. As a rule of thumb: the more high-level your environment the more error will be introduced by these factors.

_This means benchmarking tests are pretty much /always/ slow unless
you are using a [real-time operating system](https://en.wikipedia.org/wiki/Real-time_operating_system).
Real-time scheduling features now exist in the vanilla [Linux](https://www.zdnet.com/article/20-years-later-real-time-linux-makes-it-to-the-kernel-really/)_.

**Back in my day** _(a year ago) we had to install a custom version of the linux kernel
to enjoy real time scheduling features. For example for inter-programm pro audio communication._

```bash
for N in $(seq -s" " 10);
do
   pytest -k test_python_too_fast -q
done
```

Results measured beforehand on python 3.10. These are individual test runs. Most of the pytest output is omitted.

```bash
$ for N in $(seq -s" " 10); do pytest -k test_python_too_fast -q; done

Name (time in us)             Min       Max      Mean  StdDev    Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     202.7160  202.7160  202.7160  0.0000  202.7160  0.0000       0;0        4.9330       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     199.1040  199.1040  199.1040  0.0000  199.1040  0.0000       0;0        5.0225       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     254.6150  254.6150  254.6150  0.0000  254.6150  0.0000       0;0        3.9275       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     246.1540  246.1540  246.1540  0.0000  246.1540  0.0000       0;0        4.0625       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     221.9280  221.9280  221.9280  0.0000  221.9280  0.0000       0;0        4.5060       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     425.5660  425.5660  425.5660  0.0000  425.5660  0.0000       0;0        2.3498       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     212.9930  212.9930  212.9930  0.0000  212.9930  0.0000       0;0        4.6950       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     219.2340  219.2340  219.2340  0.0000  219.2340  0.0000       0;0        4.5613       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     250.9560  250.9560  250.9560  0.0000  250.9560  0.0000       0;0        3.9848       1           1
---------------------------------------------------------------------------------------------------------------------------
test_python_too_fast     216.3560  216.3560  216.3560  0.0000  216.3560  0.0000       0;0        4.6220       1           1
---------------------------------------------------------------------------------------------------------------------------
```

As you can see there are outliers that are close to 100% slower than the average runtime otherwise.
Even worse: if you are not an expert on the scheduling algorithm of your operating system
it is basically impossible to know or measure how big or how frequent the error will be.
To fix this, most benchmarking libraries will automatically run benchmarks multiple times and
present statistics of the result.

```bash
pytest -k test_python_mm
```

## Time Complexity

Consider this benchmark run:

```
-------------------------------------------------------------------------------------- benchmark: 3 tests --------------------------------------------------------------------------------------
Name (time in ms)                 Min                 Max                Mean            StdDev              Median               IQR            Outliers      OPS            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_python_mm[A0-B0-R0]      17.3623 (1.0)       22.4540 (1.0)       17.8058 (1.0)      0.7536 (1.0)       17.5652 (1.0)      0.2995 (1.0)           3;6  56.1614 (1.0)          49           1
test_python_mm[A1-B1-R1]     139.2365 (8.02)     141.8736 (6.32)     140.4964 (7.89)     1.0320 (1.37)     140.3163 (7.99)     1.8739 (6.26)          3;0   7.1176 (0.13)          8           1
test_python_mm[A2-B2-R2]     468.5704 (26.99)    471.1164 (20.98)    470.0863 (26.40)    0.9585 (1.27)     470.3083 (26.78)    1.1472 (3.83)          2;0   2.1273 (0.04)          5           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

These are three tests benchmarking the simple matrix multiplication python function.
The functions only differ in the size of the input matrices. 10x10, 20x20 and 30x30.
Some simple curve fitting reveals that the function has approx.
**O(n^3)** time complexity where **n** is the size of **one side** of the matrix.
This makes perfect sense when we look at the code for the function in question:

```py
def multiply_matrix_python(A: npt.NDArray, B: npt.NDArray):
    a_rows, a_cols = A.shape
    b_rows, b_cols = B.shape

    if a_rows != b_rows or a_cols != b_cols:
        return False
    result = np.zeros((a_rows, b_cols))
    for row in range(a_rows):
        for col in range(b_cols):
            for elt in range(a_rows):
                  result[row, col] = result[row, col] + A[row, elt] * B[elt, col]
    return result
```

As you can see we have three nested loops all iterating over the size of the matrix.
Resulting in size^3 multiplications.

[Mathematicians have written a complicated wikipedia page on the "O(n)" notation](https://en.wikipedia.org/wiki/Big_O_notation), also called "Big O" notation.
Simply put with this notation we can describe a relationship between some characteristics of the input data ("n") and the run time of an algorithm ("O(n)").

Some examples for this relationship:

```py
def get_middle_item(items: list)
    return items[len(items) // 2]
```

has **O(1)** time-complexity, at least as long as `len(items)` has **O(1)** tc.
There is full list of the time-complexities of python functions in the python wiki:

https://wiki.python.org/moin/TimeComplexity

```py
def sum_items(items: list[int])
    sum_ = 0
    for item in items:
        sum_ += item
    return sum_
```

has **O(n)** time-complexity.

```py
def partition(items: list[int], low: int, high: int):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1

def quick_sort(
    items: list[int], 
    low: int | None = None, 
    high: int | None = None
):
    if low is None and high is None
        low = 0
        high = len(items)
    if low < high:
        pi = partition(array, low, high)
        quick_sort(array, low, pi - 1)
        quick_sort(array, pi + 1, high)
```

[Quick sort](https://en.wikipedia.org/wiki/Quicksort) has **O(n * log(n))** time-complexity.


![Big O Cheat Sheet](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Comparison_computational_complexity.svg/1280px-Comparison_computational_complexity.svg.png)
