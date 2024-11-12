
## Nautilus
- open iiasa-performance-engineering/assets


## VSCode 

- open iiasa-performance-engineering
- close all open editors
- close terminal/split

### Outline 

INTRO:
 - Welcome, Introduction
 - High-level Focus
 - Python
 - Perspectives...

-- First perspective:

MECHANICAL ASSEMBLY:
 - A computer is a machine
 - Environment
 - Throttling

We can also be throttled by our

BUSSES:
- A computer is a complicated Bus system
- We need to keep that in mind because busses might be bottlenecks

We can look at the CPU in detail:

CPU:
 - We should already know about the CPU
 - Multicore
 - CPU-Bound

When we finished computing, we can send the results via a:

NETWORK:
 - Our computer as a network node
 - Networks/IO are slow
 - I/O-Bound

But next...

COST AND SCALING:
- Components and Power cost Money
- There a fundamental truths and tradeoffs: RAM vs CPU
- Hence: caching
- Alternate Universe


SOFTWARE:
- Our entire software stack influences our performance
- python is slow, has caveats
- we can measure this: errors as examples
- `time` and unwanted overhead
    - c: linkers etc.
    - python: interpreter startup, import, etc.
    - real, user, sys
    - user: using the CPU
    - need to measure from within the program...

- random noise and `pytest-benchmark`
  - computer occupied
     - cpu scheduling
     - RTOS
     - GC
     - file-systems
     - hard to predtict
  - even with internal measurement: huge outliers

- statistic fix this
- node, jit, warmup

now that we have calibrated our setup and gained perspective, we can go into a more theorethical direction:

COMPLEXITY:
- time and space (only time today)
- matrix multiplication example test output
- explain output
- explain code
- what is "n"?? the size of **one side** of the matrix
- hot areas

- more examples: (SHOW PLOTS AND COMPARE)
   - middle 
   - sum 
   - quick sort
   - it gets tricky:

- average vs worst vs best, dependant on input data
- search
- notation police
- common complexities

- how do we find "hot areas"?

PROFILERS:
 - special programs to measure beyond simple timing
 - types of profilers
 - profiler benchmarks, overhead, 
 - sampling profilers

 - python and `perf`
 - wide ecosystem but didnt work for me

 - `cProfile` is the c version of the std lib profiler
 - `pytest` fixture
 - snakeviz or dot graphs

now that we can take a closer look, some examples:

EXAMPLES:

- numpy vs polar access, snakeviz demo
- measuring the GIL
