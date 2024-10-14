# Performance Engineering 

_**For the scenario services team at IIASA/ECE.**_

Since we are mostly working in scripting languages this workshop is going to focus on high-level performance engineering only. This means I will not be talking in detail about things like: the CPU cache, branching/unconditional code, low level datastuctures like linked lists vs vectors vs buffers etc, context switches/forced pipeline flushing or any other extremely finicky technique.

I will be using python as a test subject. Python can be considered "the slowest language" although things have gotten a lot better recently. 
It also has many pitfalls, allocates a lot of memory in advance and has a robust and predictable but slow memory management technique. This technique and its implementation ("reference counting") also thus far prevented python from having "true concurrency". [Basically any operating-system process by python can only execute one python byte-code instruction at a time](https://wiki.python.org/moin/GlobalInterpreterLock).

More on all that at a later time...
For now: 

## What are we optimizing?

When we are "optimizing performance" we can set some targets and keep other things in mind.

_Collect things to optimize toward from audience._

- Run Time
- Throughput
- Memory Usage
- Latency
- Persistent Storage ? 
- ... Predictablity

Very often there are trade-offs we have to consider. These are real-world coniderations, economical or scientific in nature. For example: More RAM is often cheaper than a better CPU.

Moreover scaling CPUs is harder than scaling RAM, hence "caching" is very prevalent. It might become impossible to increase CPU clock speeds so we have to start computing in parallel - and that might not be possible at all.

Now that we got that out of the way, lets continue by taking[MEASUREMENTS](MEASUREMENTS.md).
