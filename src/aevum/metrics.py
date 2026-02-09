from base import Process
from numbers import Number

def calculate_waiting_time(arrival_time: int, prev_completion_time: int) -> Number:
    """ Calculate waiting time of a process 
    
    Args:
        arrival_time(int): The arrival time of the process to be passed
        prev_completion_time(int): The completion time of the previous process 
    
    Returns:
        Number
    """
    wait_time = prev_completion_time - arrival_time
    return max(0, wait_time)

def calculate_turnaround_time(burst_time: int, waiting_time: int) -> Number:
    """ Calculate the turnaround time of a process
    
    Args:
        burst_time(int): The burst time of the process to be passed down
        waiting_time(int): The waiting time of the process to be passed down 
    
    Returns:
        Number
    """
    return burst_time + waiting_time