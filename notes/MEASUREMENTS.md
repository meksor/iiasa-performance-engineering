# Taking Measurements

As with any other measurement, we have to keep a few basic things mind to ensure we can trust our results. We have to create a "sterile" environment for ourselves as best we can.

In a best case scenario we would be using a remote server in a datacenter somewhere.

## Throttling

Semiconductors will increase in conductivity and eventually burn out the hotter they get. This means all long-running semi-conducting devices need some sort of negative feedback with every increase in temperature. Thermal throttling.

Usually this is accomplished via low-level firmware coupled with at least one temperature sensor within the device assembly. On mobile devices like laptops throttling might also occur with the decrease of battery voltage and charge.

Consider this plot of a sorting-algorithm benchmark.

![TT](/assets/thermalt.png)

This image is taken from an MIT Courseware Lecture.
https://www.youtube.com/watch?v=LvX3g45ynu8
License: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

High-level system settings like the power profile will also impact your benchmarking results:

![TT](/assets/power_profiles.png)

## Measuring the Interpreter/Linker/JIT etc.

Its tempting to write or compile a program and benchmark it directly from your shell:

```bash
time pytest -k test_python_too_fast -q
```

As you can see from the output of that command: this is not ideal. 
If you were measuring a simple C program the measurement would (probably) include the time it takes for the operating system to start the process and some overhead by the c binary itself like [linking libaries](https://www.lurklurk.org/linkers/linkers.html).
Because we are measuring a python program, this will include all sorts of whacky things we dont need to worry about.

_Loading and starting the interpreter, loading program files from disk, parsing them, writing byte code to disk for caching ..._

_Note: Switch Python Versions_

```bash
poetry env use 3.10
poetry install

poetry env use 3.13
poetry install
```

Something very useful howerver, is to see how much time the program has spent in the kernel ("system"). All the time used by sys-calls is listed on its own which might indicate performance problems connected to writing files, listening on the network and more.

## Measuring Hard-To-Predict Noise

When measuring performance of a function that is too fast and running it only once, you might end up measuring a siginifcant error introduced by (for example) process scheduling in the operating system. Other overhead like GCs, file-systems, etc. might also play into this. As a rule of thumb: the more high-level your environment the more error will be introduced by these factors.

_This means benchmarking tests are pretty much /always/ slow unless you are using a [real-time operating system](https://en.wikipedia.org/wiki/Real-time_operating_system).
Real-time scheduling features now exist in the vanilla [Linux](https://www.zdnet.com/article/20-years-later-real-time-linux-makes-it-to-the-kernel-really/)_.

**Back in my day** _(a year ago) we had to install a custom version of the linux kernel to enjoy real time scheduling features. For example for inter-programm pro audio communication._

```bash
for N in $(seq -s" " 10);
do
   pytest -k test_python_too_fast -q
done
```

Results measured beforehand on python 3.10. These are individual test runs. 


| Name  (time in us)       | Min       | Max       | Mean      | StdDev | Median    | IQR    | Outliers | OPS (Kops/s) | Rounds | Iterations |
|--------------------------|-----------|-----------|-----------|--------|-----------|--------|----------|---------------|--------|------------|
| test_python_too_fast     | 202.7160  | 202.7160  | 202.7160  | 0.0000 | 202.7160  | 0.0000 | 0;0      | 4.9330        | 1      | 1          |
| test_python_too_fast     | 199.1040  | 199.1040  | 199.1040  | 0.0000 | 199.1040  | 0.0000 | 0;0      | 5.0225        | 1      | 1          |
| test_python_too_fast     | 254.6150  | 254.6150  | 254.6150  | 0.0000 | 254.6150  | 0.0000 | 0;0      | 3.9275        | 1      | 1          |
| test_python_too_fast     | 246.1540  | 246.1540  | 246.1540  | 0.0000 | 246.1540  | 0.0000 | 0;0      | 4.0625        | 1      | 1          |
| test_python_too_fast     | 221.9280  | 221.9280  | 221.9280  | 0.0000 | 221.9280  | 0.0000 | 0;0      | 4.5060        | 1      | 1          |
| test_python_too_fast     | 425.5660  | 425.5660  | 425.5660  | 0.0000 | 425.5660  | 0.0000 | 0;0      | 2.3498        | 1      | 1          |
| test_python_too_fast     | 212.9930  | 212.9930  | 212.9930  | 0.0000 | 212.9930  | 0.0000 | 0;0      | 4.6950        | 1      | 1          |
| test_python_too_fast     | 219.2340  | 219.2340  | 219.2340  | 0.0000 | 219.2340  | 0.0000 | 0;0      | 4.5613        | 1      | 1          |
| test_python_too_fast     | 250.9560  | 250.9560  | 250.9560  | 0.0000 | 250.9560  | 0.0000 | 0;0      | 3.9848        | 1      | 1          |
| test_python_too_fast     | 216.3560  | 216.3560  | 216.3560  | 0.0000 | 216.3560  | 0.0000 | 0;0      | 4.6220        | 1      | 1          |


As you can see there are outliers that are close to 100% slower than the average runtime otherwise.
Even worse: if you are not an expert on the scheduling algorithm of your operating system it is basically impossible to know or measure how big or how frequent the error will be.
To fix this, most benchmarking libraries will automatically run benchmarks multiple times and present statistics of the result.

```bash
pytest -k test_python_mm
```

## Summary

Limit throttling behaviour:

- Set your laptop's power profile and plug it in
- Use a desktop PC
- Use a server in a datacenter

Consider ambient factors like room temperature, air conditioning and so on.

Make sure your CPU is as idle as possible: close programs, log out other users, disable ssh server (actually dont do that if you are on a remote machine :D), etc...

Run benchmarks multiple times and do statistics. Use a benchmarking framework/write your own. Consider your programming language.

Now that we have an enviroment for testing set up, we can start thinking about "Datastructures and Algorithms" and their [COMPLEXITY](COMPLEXITY.md).
