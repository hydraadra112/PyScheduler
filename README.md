# **PyScheduler**

A unified Python module of CPU schedulers for educators and students, and for educational and simulation purposes.

---

## How to use?

Here's an example implementation of FCFS scheduling:

```python
# Using the built-in scheduler
from pyscheduler import Process, run_fcfs_simulation

processes = [
    Process(1, 10),
    Process(2, 5),
    Process(3, 8)
    ]

results = run_fcfs_simulation(processes)
print(results)

# Or if you wish to experiment, you can reimplement the FCFS like this:

from pyscheduler import calculate_turnaround_time, calculate_waiting_time

for i in range(len(processes)):
    current = processes[i]
    previous = processes[i - 1] if i > 0 else None

    calculate_waiting_time(current, previous)
    calculate_turnaround_time(current)

avg_wait = sum(p.waiting_time for p in processes) / len(processes)
avg_tat = sum(p.turnaround_time for p in processes) / len(processes)
```

---

## **Initial TODO lists**

Supported:

- [x] First Count First Serve (FCFS)

Planned:

- [ ] Shortest Job First (SJF)
- [ ] Shortest Time to Completion (STCF)
- [ ] Round Robin (RR)

I will add more algorithms in the future, but I aim to finish the todo lists above before I publish it officially as a Python package.

---

## Why do this?

During my OS class, we are tasked to perform simulations of CPU scheduling algorithms in Python, and since there are no Python modules (as far as I know) for schedulers, I had to scour through the internet to look for sample implementation, and somehow refactor every algorithm that I need to fit my use case.

Because of this, it took me a few hours to perform the simulation. It could've been far more faster if there was a module, and our teacher could've provide a demo as well.

So I took the initiative in starting this project, and thought of it as my first ever open source project to give back to the community.

This project will also be a platform for me (I hope it does for you too), to practice my coding skills and strengthen our OS scheduling knowledge.
