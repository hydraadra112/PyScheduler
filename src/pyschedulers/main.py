from base import Process
from schedulers import run_fcfs_simulation

def main():
    processes = [Process(1, 10), Process(2, 5), Process(3, 8)]
    results = run_fcfs_simulation(processes)
    print(f"Average Wait: {results['averages']['avg_waiting_time']}")

if __name__ == "__main__":
    main()