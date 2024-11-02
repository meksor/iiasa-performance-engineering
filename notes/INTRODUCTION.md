> SLIDE 1

# Performance Engineering 

_**For the scenario services team at IIASA/ECE.**_

Since we are mostly working in scripting languages this workshop is going to focus on high-level performance engineering only. This means I will not be talking in detail about things like: the CPU cache, branching/unconditional code, low level datastuctures like linked lists vs vectors vs buffers etc, context switches/forced pipeline flushing or any other extremely finicky technique.

I will be using python as a test subject. Python can be considered "the slowest language" although things have gotten a lot better recently. 
It also has many pitfalls, allocates a lot of memory in advance and has a robust and predictable but slow memory management technique. This technique and its implementation ("reference counting") also thus far prevented python from having "true concurrency". [Basically any operating-system process by python can only execute one python byte-code instruction at a time](https://wiki.python.org/moin/GlobalInterpreterLock).

I could go into detail in another installation of this format.
Before python 3.13 there was many attempts to get rid of the GIL
For now: 

> SLIDE 2

## What are we (even) optimi(z/s)ing (toward[s]) !?

... well first of all we can optimize presentations, like code, for readability and maintainability.
This isnt necessarily what I want to go in to here, but keep in mind:
Maintainability might become a salient weight on your journey to an optimized code base. 

Anyway since we are "performance engineering" lets start by asking: 

> SLIDE 3

## What are we optimzing?

When we are "optimizing performance" we can set some targets and keep other things in mind.

_Collect things to optimize toward from audience._

- Run Time
- Throughput and Concurrency (.. One-Shot vs Service)
- Memory Usage
- Latency
- Persistent Storage ? 
- ... Predictablity

> SLIDE 4

Very often there are trade-offs we have to consider. These are real-world considerations, economical or scientific in nature. For example: *In some way* More RAM is cheaper than a better CPU.

> SLIDE 5

... and  scaling CPUs is harder than scaling RAM, hence "caching" is very prevalent. It might become impossible to increase CPU clock speeds so we have to start computing in parallel - and that might not be possible at all.

... On the other hand: you probably dont want to cache gigabytes of completely random noise ... 

// Strange example with an alternate universe where 1000 people have to say a special incantation for one hour for each bit in each RAM stick. (in this universe we are better off computing the result again than storing it in memory)

Now that we got that out of the way, lets continue by taking [MEASUREMENTS](MEASUREMENTS.md).

> SLIDE 6
