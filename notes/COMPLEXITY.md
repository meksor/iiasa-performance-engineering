# Complexity

Consider this benchmark run:

| Name                     | Min                   | Max                   | Mean                  | StdDev                | Median                | IQR                  | Outliers | OPS                | Rounds | Iterations |
|--------------------------|-----------------------|-----------------------|-----------------------|-----------------------|-----------------------|----------------------|----------|--------------------|--------|------------|
| test_python_mm[A0-B0-R0] | 17.3623 (1.0)         | 22.4540 (1.0)         | 17.8058 (1.0)         | 0.7536 (1.0)          | 17.5652 (1.0)         | 0.2995 (1.0)         | 3;6      | 56.1614 (1.0)      | 49     | 1          |
| test_python_mm[A1-B1-R1] | 139.2365 (8.02)       | 141.8736 (6.32)       | 140.4964 (7.89)       | 1.0320 (1.37)         | 140.3163 (7.99)       | 1.8739 (6.26)        | 3;0      | 7.1176 (0.13)      | 8      | 1          |
| test_python_mm[A2-B2-R2] | 468.5704 (26.99)      | 471.1164 (20.98)      | 470.0863 (26.40)      | 0.9585 (1.27)         | 470.3083 (26.78)      | 1.1472 (3.83)        | 2;0      | 2.1273 (0.04)      | 5      | 1          |


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

As you can see we have three nested loops all iterating over the size of the matrix. Resulting in size^3 multiplications.

[Mathematicians have written a complicated wikipedia page on the "O(n)" notation](https://en.wikipedia.org/wiki/Big_O_notation), also called "Big O" notation. Simply put with this notation we can describe a relationship between some characteristics of the input data ("n") and the run time of an algorithm ("O(n)").

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
    pivot = items[high]
    i = low - 1
    for j in range(low, high):
        if items[j] <= pivot:
            i = i + 1
            (items[i], items[j]) = (items[j], items[i])
    (items[i + 1], items[high]) = (items[high], items[i + 1])
    return i + 1

def quick_sort(
    items: list[int], 
    low: int | None = None, 
    high: int | None = None
):
    if low is None or high is None:
        low = 0
        high = len(items)
    
    if low < high:
        pi = partition(items, low, high)
        quick_sort(items, low, pi - 1)
        quick_sort(items, pi + 1, high)

```

[Quick sort](https://en.wikipedia.org/wiki/Quicksort) has **O(n * log(n))** time-complexity.

And so on...
Here is a plot of theses functions from wikipedia:

![Big O Cheat Sheet](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Comparison_computational_complexity.svg/1280px-Comparison_computational_complexity.svg.png)

**Keep in mind that we are not plotting actual "run time" here, just the scaling relationship between run time and 
the input of an algorithm. **

```bash
pytest -k test_tc_get_middle_item -q
pytest -k test_tc_sum_items -q
pytest -k test_tc_sum_builtin -q
pytest -k test_tc_quick_sort -q
pytest -k test_tc_sorted_builtin -q
```

### Benchmark: Get Middle Item

One very fast run before changing power settings:

| Name (time in ns)                             | Min              | Max               | Mean             | StdDev            | Median           | IQR              | Outliers      | OPS (Mops/s)      | Rounds  | Iterations |
|------------------------------------------------|------------------|-------------------|------------------|-------------------|------------------|------------------|---------------|------------------|---------|------------|
| test_tc_get_middle_item[list_1]              | 479.5500 (1.0)   | 5,699.6000 (1.0)  | 575.5937 (1.02)  | 189.6684 (1.25)   | 535.0500 (1.0)    | 30.2500 (1.14)   | 3454;7627    | 1.7373 (0.98)    | 79834   | 20         |
| test_tc_get_middle_item[list_2]              | 494.0500 (1.03)  | 29,525.1500 (5.18)| 564.5243 (1.0)   | 151.2244 (1.0)    | 551.6500 (1.03)   | 26.5999 (1.0)    | 755;5086     | 1.7714 (1.0)     | 72675   | 20         |
| test_tc_get_middle_item[list_4]              | 542.9999 (1.13)  | 14,298.2501 (2.51)| 660.0780 (1.17)  | 152.5636 (1.01)   | 643.0000 (1.20)   | 52.7500 (1.98)   | 3026;7618    | 1.5150 (0.86)    | 174703  | 4          |
| test_tc_get_middle_item[list_3]              | 672.9997 (1.40)  | 24,546.0005 (4.31)| 884.9792 (1.57)  | 206.6707 (1.37)   | 861.0004 (1.61)   | 95.9999 (3.61)   | 4150;6056    | 1.1300 (0.64)    | 179986  | 1          |
| test_tc_get_middle_item[list_0]              | 733.0000 (1.53)  | 26,902.9997 (4.72)| 940.2008 (1.67)  | 250.1688 (1.65)   | 917.9994 (1.72)   | 103.0003 (3.87)  | 2025;3633    | 1.0636 (0.60)    | 130141  | 1          |

A slower run:

| Name (time in us)                      | Min                | Max                | Mean              | StdDev            | Median            | IQR              | Outliers      | OPS (Kops/s)      | Rounds | Iterations |
|-----------------------------------------|--------------------|--------------------|-------------------|-------------------|-------------------|------------------|---------------|-------------------|--------|------------|
| test_tc_get_middle_item[list_0]       | 3.9610 (1.0)       | 73.6270 (3.25)     | 5.0214 (1.02)     | 1.1179 (1.39)     | 4.7900 (1.0)      | 0.5120 (1.05)    | 1766;2168     | 199.1484 (0.99)    | 37566  | 1          |
| test_tc_get_middle_item[list_1]       | 3.9980 (1.01)      | 22.6830 (1.0)      | 4.9471 (1.0)      | 0.8035 (1.0)      | 4.8050 (1.00)     | 0.5000 (1.02)    | 1928;1530     | 202.1378 (1.0)     | 41807  | 1          |
| test_tc_get_middle_item[list_3]       | 4.0090 (1.01)      | 52.0210 (2.29)     | 5.0287 (1.02)     | 0.8792 (1.09)     | 4.8810 (1.02)     | 0.4890 (1.0)     | 2322;2359     | 198.8580 (0.98)    | 60599  | 1          |
| test_tc_get_middle_item[list_4]       | 4.0500 (1.02)      | 76.8430 (3.39)     | 5.0294 (1.02)     | 0.8701 (1.08)     | 4.8950 (1.02)     | 0.5060 (1.03)    | 1552;1408     | 198.8305 (0.98)    | 40331  | 1          |
| test_tc_get_middle_item[list_2]       | 4.0840 (1.03)      | 245.6380 (10.83)   | 5.0224 (1.02)     | 1.7122 (2.13)     | 4.8780 (1.02)     | 0.4990 (1.02)    | 970;2025      | 199.1060 (0.99)    | 58590  | 1          |

As you can see the time complexity here is for all purposes almost "random", the array with the medium amount of items took the longest.

### Benchmark: Sum Items

| Name (time in us)                      | Min                | Max                | Mean              | StdDev            | Median            | IQR              | Outliers      | OPS (Kops/s)      | Rounds | Iterations |
|-----------------------------------------|--------------------|--------------------|-------------------|-------------------|-------------------|------------------|---------------|-------------------|--------|------------|
| test_tc_sum_items[list_0]              | 12.5580 (1.0)      | 83.4370 (1.0)      | 13.8530 (1.0)     | 1.5569 (1.0)      | 13.5530 (1.0)     | 0.5530 (1.0)     | 984;1357      | 72.1863 (1.0)      | 27882  | 1          |
| test_tc_sum_items[list_1]              | 21.8150 (1.74)     | 132.1810 (1.58)    | 23.9522 (1.73)    | 3.3440 (2.15)     | 23.0980 (1.70)    | 0.6990 (1.26)    | 1762;2297     | 41.7498 (0.58)     | 24385  | 1          |
| test_tc_sum_items[list_2]              | 32.2970 (2.57)     | 117.3100 (1.41)    | 34.6872 (2.50)    | 2.3011 (1.48)     | 34.2115 (2.52)    | 1.0000 (1.81)    | 1202;1377     | 28.8291 (0.40)     | 20478  | 1          |
| test_tc_sum_items[list_3]              | 41.2980 (3.29)     | 90.6320 (1.09)     | 43.9271 (3.17)    | 2.1079 (1.35)     | 43.5070 (3.21)    | 1.0588 (1.91)    | 1205;1215     | 22.7650 (0.32)     | 17399  | 1          |
| test_tc_sum_items[list_4]              | 51.9250 (4.13)     | 218.6510 (2.62)    | 55.6067 (4.01)    | 3.0981 (1.99)     | 54.8520 (4.05)    | 1.4960 (2.71)    | 1443;1743     | 17.9835 (0.25)     | 13698  | 1          |

### Benchmark: Sum Built-in

| Name (time in us)                      | Min                | Max                | Mean              | StdDev            | Median            | IQR              | Outliers      | OPS (Kops/s)      | Rounds | Iterations |
|-----------------------------------------|--------------------|--------------------|-------------------|-------------------|-------------------|------------------|---------------|-------------------|--------|------------|
| test_tc_sum_builtin[list_0]           | 6.3100 (1.0)       | 77.3920 (2.60)     | 7.1979 (1.0)      | 1.0391 (1.09)     | 7.0640 (1.0)      | 0.4040 (1.0)     | 721;1329      | 138.9291 (1.0)     | 36645  | 1          |
| test_tc_sum_builtin[list_1]           | 9.3730 (1.49)      | 29.7970 (1.0)      | 10.2694 (1.43)    | 0.9497 (1.0)      | 10.1005 (1.43)    | 0.4090 (1.01)    | 1174;1801     | 97.3764 (0.70)     | 42014  | 1          |
| test_tc_sum_builtin[list_2]           | 12.5390 (1.99)     | 132.1630 (4.44)    | 13.8500 (1.92)    | 2.5469 (2.68)     | 13.2650 (1.88)    | 0.4660 (1.15)    | 2292;2738     | 72.2021 (0.52)     | 33871  | 1          |
| test_tc_sum_builtin[list_3]           | 15.5000 (2.46)     | 176.5840 (5.93)    | 16.9216 (2.35)    | 2.5767 (2.71)     | 16.2895 (2.31)    | 0.4580 (1.13)    | 2012;2411     | 59.0959 (0.43)     | 31004  | 1          |
| test_tc_sum_builtin[list_4]           | 18.9810 (3.01)     | 63.3300 (2.13)     | 20.0413 (2.78)    | 1.5652 (1.65)     | 19.7300 (2.79)    | 0.4320 (1.07)    | 967;1365      | 49.8970 (0.36)     | 25614  | 1          |

### Benchmark: Quick Sort
| Name (time in us)            | Min                  | Max                  | Mean                 | StdDev               | Median               | IQR                  | Outliers | OPS                 | Rounds | Iterations |
|-------------------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------|---------------------|--------|------------|
| test_tc_quick_sort[list_0]   | 295.3170 (1.0)       | 1,938.7670 (1.0)     | 382.7862 (1.0)       | 107.0890 (1.0)       | 361.8710 (1.0)       | 58.7960 (1.0)        | 459;523  | 2,612.4245 (1.0)    | 8074   | 1          |
| test_tc_quick_sort[list_1]   | 1,042.7370 (3.53)    | 2,510.2660 (1.29)    | 1,199.9708 (3.13)    | 124.8894 (1.17)      | 1,176.2730 (3.25)    | 113.0315 (1.92)      | 749;212  | 833.3536 (0.32)     | 4309   | 1          |
| test_tc_quick_sort[list_2]   | 2,234.1080 (7.57)    | 4,889.0630 (2.52)    | 2,958.9261 (7.73)    | 467.9265 (4.37)      | 2,812.8030 (7.77)    | 663.8130 (11.29)     | 876;33   | 337.9604 (0.13)     | 2985   | 1          |
| test_tc_quick_sort[list_3]   | 4,048.5360 (13.71)   | 7,575.4120 (3.91)    | 4,699.1379 (12.28)   | 561.8317 (5.25)      | 4,551.1670 (12.58)   | 525.5520 (8.94)      | 270;115  | 212.8050 (0.08)     | 1567   | 1          |
| test_tc_quick_sort[list_4]   | 6,337.3070 (21.46)   | 13,530.6310 (6.98)   | 7,355.6791 (19.22)   | 740.7349 (6.92)      | 7,156.1620 (19.78)   | 915.2985 (15.57)     | 376;38   | 135.9494 (0.05)     | 1567   | 1          |
| test_tc_quick_sort[list_5]   | 9,240.8080 (31.29)   | 20,046.6190 (10.34)  | 10,134.6027 (26.48)  | 872.1170 (8.14)      | 9,948.3160 (27.49)   | 595.2665 (10.12)     | 92;72    | 98.6719 (0.04)      | 1232   | 1          |
| test_tc_quick_sort[list_6]   | 12,654.9330 (42.85)  | 42,256.0170 (21.80)  | 14,088.4343 (36.80)  | 1,387.4693 (12.96)   | 13,725.5100 (37.93)  | 1,260.4588 (21.44)   | 136;40   | 70.9802 (0.03)      | 1127   | 1          |
| test_tc_quick_sort[list_7]   | 16,562.6100 (56.08)  | 27,196.4470 (14.03)  | 18,770.9217 (49.04)  | 1,878.9609 (17.55)   | 18,054.2710 (49.89)  | 1,888.4582 (32.12)   | 155;69   | 53.2739 (0.02)      | 897    | 1          |
| test_tc_quick_sort[list_8]   | 21,226.9460 (71.88)  | 63,980.7050 (33.00)  | 24,828.3112 (64.86)  | 3,738.5746 (34.91)   | 23,313.5325 (64.42)  | 3,892.3925 (66.20)   | 106;26   | 40.2766 (0.02)      | 724    | 1          |

Number 9 failed "maximum rc. depth exceeded"

### Benchmark: Sorted Built-in
| Name                          | Min (us)    | Max (us)    | Mean (us)   | StdDev (us) | Median (us) | IQR (us) | Outliers  | OPS (Kops/s) | Rounds | Iterations |
|-------------------------------|-------------|-------------|-------------|-------------|-------------|----------|-----------|--------------|--------|------------|
| test_tc_sorted_builtin[list_0]| 10.2330 (1.0)| 86.8940 (1.0)| 11.8841 (1.0)| 3.0807 (1.0)| 11.0150 (1.0)| 0.5150   | 1696;1864 | 84.1459 (1.0)| 17660  | 1          |
| test_tc_sorted_builtin[list_1]| 20.1870 (1.97)| 132.5540 (1.53)| 21.9665 (1.85)| 4.0732 (1.32)| 21.0850 (1.91)| 0.5200   | 769;923   | 45.5239 (0.54)| 12340  | 1          |
| test_tc_sorted_builtin[list_2]| 31.4440 (3.07)| 139.8390 (1.61)| 34.8777 (2.93)| 7.6319 (2.48)| 32.6560 (2.96)| 0.7000   | 703;961   | 28.6716 (0.34)| 8723   | 1          |
| test_tc_sorted_builtin[list_3]| 41.8330 (4.09)| 131.5750 (1.51)| 45.1700 (3.80)| 6.8370 (2.22)| 43.4330 (3.94)| 0.7760   | 425;563   | 22.1386 (0.26)| 6184   | 1          |
| test_tc_sorted_builtin[list_4]| 53.5660 (5.23)| 156.0000 (1.80)| 57.5184 (4.84)| 7.6318 (2.48)| 55.3860 (5.03)| 1.2970   | 269;614   | 17.3858 (0.21)| 3962   | 1          |

