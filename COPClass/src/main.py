import os
import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst

class SJFResult:
    def __init__(self, wait, turnaround, response):
        self.wait = wait
        self.turnaround = turnaround
        self.response = response

def read_input_file(file_path):
    # Default values
    process_count = 0
    run_for = 0
    algorithm = ""
    processes = []

    # Try to open the file for reading
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                tokens = line.split()
                if tokens[0] == "processcount":
                    process_count = int(tokens[1])
                elif tokens[0] == "runfor":
                    run_for = int(tokens[1])
                elif tokens[0] == "use":
                    if tokens[1] not in ["sjf", "fcfs", "rr"]:
                        print("Error: Invalid use statement.")
                        sys.exit(1)  # Exit with error code 1
                    else:
                        algorithm = tokens[1]
                elif tokens[0] == "process":
                    process_name = tokens[2]
                    arrival = int(tokens[4])
                    burst = int(tokens[6])
                    processes.append(Process(process_name, arrival, burst))
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)  # Exit with error code 1
    
    return process_count, run_for, algorithm, processes

def print_input(process_count, run_for, algorithm, processes):
    print("Process count:", process_count)
    print("Run for:", run_for)
    print("Algorithm:", algorithm)
    
    print("Processes:")
    for process in processes:
        print(f"Process name: {process.name}, Arrival: {process.arrival}, Burst: {process.burst}")

def sjf(processes):
    result = []

    processes.sort(key=lambda x: x.arrival)

    current_time = 0
    remaining_processes = processes.copy()

    print(f"{len(processes)} processes")
    print("Using preemptive Shortest Job First")

    while remaining_processes:
        ready_processes = [p for p in remaining_processes if p.arrival <= current_time]
        if not ready_processes:
            print(f"Time {current_time:3d} : Idle")
            current_time += 1
            continue

        shortest_job = min(ready_processes, key=lambda x: x.burst)
        remaining_processes.remove(shortest_job)

        print(f"Time {current_time:3d} : {shortest_job.name} arrived")
        print(f"Time {current_time:3d} : {shortest_job.name} selected (burst {shortest_job.burst})")
        current_time += shortest_job.burst

        wait_time = current_time - shortest_job.arrival - shortest_job.burst
        turnaround_time = current_time - shortest_job.arrival
        response_time = wait_time if wait_time >= 0 else 0

        result.append(SJFResult(wait_time, turnaround_time, response_time))

        print(f"Time {current_time:3d} : {shortest_job.name} finished")

    print(f"Finished at time {sum(result.turnaround for result in result)}")
    print("Results:")
    for i, res in enumerate(result, 1):
        print(f"{processes[i - 1].name} wait {res.wait:3d} turnaround {res.turnaround:3d} response {res.response:3d}")

    return result


def main():
    # Define the directory path
    directory = 'COPClass/InputFiles'
    
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory 'InputFiles' created.")
    
    # Define the file path
    file_path = os.path.join(directory, 'input.txt')
    
    # Read the input file
    process_count, run_for, algorithm, processes = read_input_file(file_path)

    #print_input(process_count, run_for, algorithm, processes)

    if algorithm == "sjf":
        sjf_results = sjf(processes)
        print(f"Finished at time {sum(result.turnaround for result in sjf_results)}")
        print("Results:")
        for i, result in enumerate(sjf_results, 1):
            print(f"{processes[i - 1].name} wait {result.wait} turnaround {result.turnaround} response {result.response}")

if __name__ == "__main__":
    main()
