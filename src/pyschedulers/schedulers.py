from metrics import calculate_turnaround_time, calculate_waiting_time
from base import Process

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

    for i in range(len(processes)):
        current = processes[i]
        previous = processes[i - 1] if i > 0 else None
        
        calculate_waiting_time(current, previous)
        calculate_turnaround_time(current)

    avg_wait = sum(p.waiting_time for p in processes) / len(processes)
    avg_tat = sum(p.turnaround_time for p in processes) / len(processes)

    # Construct Output Dictionary
    output = {
        "individual_results": [
            {
                "pid": p.pid,
                "burst": p.burst_time,
                "wait": p.waiting_time,
                "turnaround": p.turnaround_time
            } for p in processes
        ],
        "averages": {
            "avg_waiting_time": round(avg_wait, 2),
            "avg_turnaround_time": round(avg_tat, 2)
        },
        "total_completion_time": processes[-1].turnaround_time
    }

    return output