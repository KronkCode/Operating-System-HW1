import os
import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # Initialize to -1, will be updated when process starts
        self.start_time = -1  # Initialize to -1, will be updated when process starts


    def update_response_time(self, current_time):
        if self.response_time == -1:
            self.response_time = current_time - self.arrival

    def update_turnaround_time(self, current_time):
        self.turnaround_time = current_time - self.arrival
  
  
def first_in_first_out(processes, run_for):
    num_processes = len(processes)
    print(f" {num_processes} processes")
    print("Using First-Come First-Served")

    current_time = 0

    remaining_processes = processes.copy()
    eligible_processes = []
    finished_processes = []
    current_process = None

    while current_time < run_for or current_process is not None:
        # Check for newly arrived processes
        for process in remaining_processes:
            if process.arrival == current_time:
                eligible_processes.append(process)
                print(f"Time {current_time}: {process.name} arrived")

        # If there is a current process and it's finished, print and remove it
        if current_process is not None and current_process.burst == 0:
            current_process.update_turnaround_time(current_time)
            print(f"Time {current_time}: {current_process.name} finished")
            finished_processes.append(current_process)
            remaining_processes.remove(current_process)
            current_process = None

        # Select the next process if none is running
        if current_process is None and eligible_processes:
            next_process = eligible_processes[0]
            current_process = eligible_processes.pop(0)
            current_process.update_response_time(current_time)
            current_process.start_time = current_time
            print(f"Time {current_time}: {current_process.name} selected (burst: {current_process.burst})")

        # If there are no processes, print idle
        if not remaining_processes or current_process is None:
            print(f"Time {current_time}: Idle")

        # Increment current time and decrement burst of current process
        current_time += 1
        if current_process is not None:
            current_process.burst -= 1

    print("Finished at time", current_time)
    print("")
    # Print wait time, turnaround time, and response time for each process
    for process in processes:
        wait_time = process.start_time - process.arrival if process.start_time != -1 else 2
        print(f"{process.name} wait {wait_time} turnaround {process.turnaround_time} response {process.response_time}")



# Define the Shortest Job First (SJF) scheduling function
def shortest_job_first(processes, run_for):
    num_processes = len(processes)
    print(f"{num_processes} processes")
    print("Using preemptive Shortest Job First")

    current_time = 0

    remaining_processes = processes.copy()
    eligible_processes = []
    finished_processes = []
    current_process = None

    while current_time < run_for or current_process is not None:
        # Check for newly arrived processes
        for process in remaining_processes:
            if process.arrival == current_time:
                eligible_processes.append(process)
                print(f"Time {current_time}: {process.name} arrived")

        # If there is a current process and it's finished, print and remove it
        if current_process is not None and current_process.burst == 0:
            current_process.update_turnaround_time(current_time)
            print(f"Time {current_time}: {current_process.name} finished")
            finished_processes.append(current_process)
            remaining_processes.remove(current_process)
            current_process = None

        # Sort eligible processes by burst time
        eligible_processes.sort(key=lambda x: x.burst)

        # Select the next process if none is running
        if current_process is None and eligible_processes:
            next_process = eligible_processes[0]
            current_process = eligible_processes.pop(0)
            current_process.update_response_time(current_time)
            current_process.start_time = current_time
            print(f"Time {current_time}: {current_process.name} selected (burst: {current_process.burst})")

        # If there's a process with shorter burst, preempt the current process
        elif current_process is not None and eligible_processes and eligible_processes[0].burst < current_process.burst:
            next_process = eligible_processes[0]
            print(f"Time {current_time}: {next_process.name} selected (burst: {next_process.burst})")
            eligible_processes.append(current_process)
            current_process = eligible_processes.pop(0)
            current_process.wait_time = 0  # Reset wait time when preempted

        # Increment wait time for all eligible processes
        for process in eligible_processes:
            if process != current_process:
                process.wait_time += 1

        # If there are no processes, print idle
        if not remaining_processes or current_process is None:
            print(f"Time {current_time}: Idle")

        # Increment current time and decrement burst of current process
        current_time += 1
        if current_process is not None:
            current_process.burst -= 1

    print("Finished at time", current_time)
    print("")
    # Print wait time, turnaround time, and response time for each process
    for process in processes:
        print(f"{process.name} wait {process.wait_time} turnaround {process.turnaround_time} response {process.response_time}")

#Done Erik Dokken
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

#Done Erik Dokken
def print_input(process_count, run_for, algorithm, processes):
    print("Process count:", process_count)
    print("Run for:", run_for)
    print("Algorithm:", algorithm)
    
    print("Processes:")
    for process in processes:
        print(f"Process name: {process.name}, Arrival: {process.arrival}, Burst: {process.burst}")
   

def main():
    # Define the directory path
    directory = 'COPClass/InputFiles'
   
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory 'InputFiles' created.")

    # Define the file path
    file_path = os.path.join(directory, 'c5-fcfs.in')
    
    # Read the input file
    process_count, run_for, algorithm, processes = read_input_file(file_path)



    if algorithm == "sjf":
        shortest_job_first(processes, run_for)
    elif algorithm == "fcfs":
        first_in_first_out(processes, run_for)
    else:
        print(f"Error: Algorithm {algorithm} not supported.")
    

if __name__ == "__main__":
    main()