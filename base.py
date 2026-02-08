class Process():
    def __init__(self, pid: int, burst_time: int):
        if not isinstance(pid, int) or not isinstance(burst_time, int):
            raise TypeError("PID and Burst Time must be integers.")
        if burst_time < 0:
            raise ValueError("Burst time cannot be negative.")
            
        self.pid = pid
        self.burst_time = burst_time
        self.waiting_time = None
        self.turnaround_time = None