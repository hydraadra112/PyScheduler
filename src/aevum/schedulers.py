from base import Process, ProcessResult, Clock
from utils import is_sorted_by_arrival, sort_processes_by_burst
import heapq

def run_fcfs_simulation(processes: list[Process]) -> dict:
    """
    Executes FCFS scheduling and returns a dictionary of results.

    Args:
        processes(Process): A list of the class Process.

    Returns:
        dict: A dictionary containing the individual results, and its averages.
    """
    if not processes:
        raise ValueError("Process list is empty!")

    # Check if sorted
    if not is_sorted_by_arrival(processes):
        raise ValueError(
            "FCFS requires processes to be sorted by arrival time. "
            "Please use 'aevum.utils.sort_processes_by_arrival()' before passing the list."
        )

    clock = Clock()
    current_job: Process = None
    process_results: list[ProcessResult] = []
    ready_processes: list[ProcessResult] = []
    remaining_time = 0
    start_time = 0

    while processes or ready_processes or current_job:
        # Check if any process arrives at THIS tick
        while processes and processes[0].arrival_time <= clock.time:
            ready_processes.append(processes.pop(0))
        
        # If CPU is idle, pick the shortest job from ready queue
        if not current_job and ready_processes:
            current_job = ready_processes.pop(0) # FCFS, so first process will be executed
            remaining_time = current_job.burst_time
            start_time = clock.time

        # Process 1 unit of work
        if current_job:
            remaining_time -= 1
            
            # Record metrics if finished
            if remaining_time == 0:
                # Use your existing logic for metrics
                comp_t = clock.time + 1
                wait_t = start_time - current_job.arrival_time
                tat_t = comp_t - current_job.arrival_time
                
                process_results.append(ProcessResult(
                    process=current_job,
                    waiting_time=wait_t,
                    turnaround_time=tat_t,
                    completion_time=comp_t
                ))
                current_job = None # CPU becomes idle for the next tick
        clock.tick()


    avg_wait = sum(r.waiting_time for r in process_results) / len(process_results)
    avg_tat = sum(r.turnaround_time for r in process_results) / len(process_results)

    # Construct Output Dictionary
    return {
        "individual_results": [
            {
                "pid": r.process.pid,
                "wait": r.waiting_time,
                "turnaround": r.turnaround_time,
                "completion": r.completion_time
            } for r in process_results
        ],
        "averages": {
            "avg_waiting_time": round(avg_wait, 2),
            "avg_turnaround_time": round(avg_tat, 2)
        }
    }

def run_sjf_simulation(processes: list[Process]) -> dict:
    """
    Executes Shortest Job First (SJF) scheduling and returns a dictionary of results.

    Args:
        processes(Process): A list of the class Process.

    Returns:
        dict: A dictionary containing the individual results, and its averages.
    """
    if not processes:
        raise ValueError("Process list is empty!")

    # Check if sorted
    if not is_sorted_by_arrival(processes):
        raise ValueError(
            "SJF requires processes to be sorted by arrival time. "
            "Please use 'aevum.utils.sort_processes_by_arrival()' before passing the list."
        )
    
    clock = Clock()
    process_results: list[ProcessResult] = []
    ready_processes: list[ProcessResult] = []
    
    current_job: Process = None
    remaining_time = 0
    start_time = 0

    while processes or ready_processes or current_job:
        # Check if any process arrives at THIS tick
        while processes and processes[0].arrival_time <= clock.time:
            ready_processes.append(processes.pop(0))
        
        # If CPU is idle, pick the shortest job from ready queue
        if not current_job and ready_processes:
            current_job = min(ready_processes, key=lambda p: p.burst_time)
            ready_processes.remove(current_job)
            remaining_time = current_job.burst_time
            start_time = clock.time

        # If a job is running, process 1 unit of work
        if current_job:
            remaining_time -= 1

            # Check if the job finished on THIS tick
            if remaining_time == 0:
                completion_time = clock.time + 1
                waiting_time = start_time - current_job.arrival_time
                turnaround_time = completion_time - current_job.arrival_time

                process_results.append(ProcessResult(
                    process=current_job,
                    waiting_time=waiting_time,
                    turnaround_time=turnaround_time,
                    completion_time=completion_time
                ))

                current_job = None

        clock.tick()

    avg_wait = sum(r.waiting_time for r in process_results) / len(process_results)
    avg_tat = sum(r.turnaround_time for r in process_results) / len(process_results)

    return {
        "individual_results": [
            {
                "pid": r.process.pid,
                "wait": r.waiting_time,
                "turnaround": r.turnaround_time,
                "completion": r.completion_time
            } for r in process_results
        ],
        "averages": {
            "avg_waiting_time": round(avg_wait, 2),
            "avg_turnaround_time": round(avg_tat, 2)
        }
    }

def run_stcf_simulation(processes: list[Process]) -> dict:
    """
    Executes STCF scheduling using a priority queue (heapq) for efficiency.

    Args:
        processes(Process): A list of the class Process.

    Returns:
        dict: A dictionary containing the individual results, and its averages.
    """
    if not processes:
        raise ValueError("Process list is empty!")

    if not is_sorted_by_arrival(processes):
        raise ValueError("STCF requires processes to be sorted by arrival time."
        "Please use 'aevum.utils.sort_processes_by_arrival()' before passing the list.")

    clock = Clock()
    process_results: list[ProcessResult] = []
    
    # Priority Queue: (remaining_time, arrival_time, pid, process_object)
    ready_heap = []
    
    # Track remaining times and original bursts (as Process is frozen)
    remaining_times = {p.pid: p.burst_time for p in processes}
    original_bursts = {p.pid: p.burst_time for p in processes}
    
    # Copy of processes to handle arrivals
    ready_processes = list(processes)
    current_job: Process = None

    while ready_processes or ready_heap or current_job:
        
        # Handle Arrivals
        new_arrival_occurred = False
        while ready_processes and ready_processes[0].arrival_time <= clock.time:
            p = ready_processes.pop(0)
            heapq.heappush(ready_heap, (remaining_times[p.pid], p.arrival_time, p.pid, p))
            new_arrival_occurred = True

        # Preemption Check
        # If a new process arrived, we must check if it's shorter than the current one
        if new_arrival_occurred and current_job:
            # Put current job back in heap to let heapq re-evaluate the shortest
            heapq.heappush(ready_heap, (remaining_times[current_job.pid], current_job.arrival_time, current_job.pid, current_job))
            current_job = None

        # Pick Next Job if CPU is idle
        if not current_job and ready_heap:
            # Pop the tuple and extract the Process object (at index 3)
            _, _, _, current_job = heapq.heappop(ready_heap)

        # Execute 1 unit of work
        if current_job:
            remaining_times[current_job.pid] -= 1
            
            # Check if process is finished
            if remaining_times[current_job.pid] == 0:
                completion_time = clock.time + 1
                turnaround_time = completion_time - current_job.arrival_time
                waiting_time = turnaround_time - original_bursts[current_job.pid]

                process_results.append(ProcessResult(
                    process=current_job,
                    waiting_time=waiting_time,
                    turnaround_time=turnaround_time,
                    completion_time=completion_time
                ))
                current_job = None 

        clock.tick()

    # Calculate Averages
    avg_wait = sum(r.waiting_time for r in process_results) / len(process_results)
    avg_tat = sum(r.turnaround_time for r in process_results) / len(process_results)

    return {
        "individual_results": [
            {
                "pid": r.process.pid,
                "wait": r.waiting_time,
                "turnaround": r.turnaround_time,
                "completion": r.completion_time
            } for r in process_results
        ],
        "averages": {
            "avg_waiting_time": round(avg_wait, 2),
            "avg_turnaround_time": round(avg_tat, 2)
        }
    }

def run_rr_simulation(processes: list[Process], time_quantum: int) -> dict:
    """
    Executes Round Robin (RR) scheduling and returns a dictionary of results.

    Args:
        processes(list[Process]): A list of the class Process.
        time_quantum(int): The time slice each process gets before preemption.

    Returns:
        dict: A dictionary containing the individual results and averages.
    """
    if not processes:
        raise ValueError("Process list is empty!")
    
    if time_quantum <= 0:
        raise ValueError("Time quantum must be greater than 0!")

    # Ensure processes are sorted by arrival for the simulation loop
    if not is_sorted_by_arrival(processes):
        raise ValueError(
            "RR requires processes to be sorted by arrival time. "
            "Please use 'aevum.utils.sort_processes_by_arrival()' before passing the list."
        )

    clock = Clock()
    process_results: list[ProcessResult] = []
    ready_processes: list[Process] = []
    incoming_processes = list(processes)
    
    # Track remaining times and original bursts
    remaining_times = {p.pid: p.burst_time for p in incoming_processes}
    original_bursts = {p.pid: p.burst_time for p in incoming_processes}
    
    current_job: Process = None
    quantum_tracker = 0 # Tracks how many ticks the current job has used

    while incoming_processes or ready_processes or current_job:
        
        # New processes go to the TAIL of the ready queue
        while incoming_processes and incoming_processes[0].arrival_time <= clock.time:
            ready_processes.append(incoming_processes.pop(0))
        
        # If CPU is idle, grab from the HEAD of the ready queue
        if not current_job and ready_processes:
            current_job = ready_processes.pop(0)
            quantum_tracker = 0

        # Execute 1 unit of work
        if current_job:
            remaining_times[current_job.pid] -= 1
            quantum_tracker += 1
            
            # Process finishes naturally before quantum expires
            if remaining_times[current_job.pid] == 0:
                completion_time = clock.time + 1
                turnaround_time = completion_time - current_job.arrival_time
                waiting_time = turnaround_time - original_bursts[current_job.pid]

                process_results.append(ProcessResult(
                    process=current_job,
                    waiting_time=waiting_time,
                    turnaround_time=turnaround_time,
                    completion_time=completion_time
                ))
                current_job = None
                quantum_tracker = 0
            
            # Quantum expires, but process still has work to do
            elif quantum_tracker == time_quantum:
                # We must check for new arrivals at THIS exact moment 
                # before putting the preempted process back, so the newcomers 
                # get their fair spot ahead of the preempted one.
                while incoming_processes and incoming_processes[0].arrival_time <= clock.time + 1:
                    ready_processes.append(incoming_processes.pop(0))
                
                ready_processes.append(current_job)
                current_job = None
                quantum_tracker = 0

        clock.tick()

    # Calculate Averages
    avg_wait = sum(r.waiting_time for r in process_results) / len(process_results)
    avg_tat = sum(r.turnaround_time for r in process_results) / len(process_results)

    return {
        "individual_results": [
            {
                "pid": r.process.pid,
                "wait": r.waiting_time,
                "turnaround": r.turnaround_time,
                "completion": r.completion_time
            } for r in process_results
        ],
        "averages": {
            "avg_waiting_time": round(avg_wait, 2),
            "avg_turnaround_time": round(avg_tat, 2)
        }
    }