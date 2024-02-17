import os
import sys

from sympy import Idx

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.start_time = -1
        self.repeat_flag_res = 0
        self.repeat_flag_wait = 0
        
    # Update turnaround time of a process
    def update_turnaround_time(self, current_time):
        self.turnaround_time = current_time - self.arrival

    # Update response time of a process
    def update_response_time(self, current_time):
        if self.repeat_flag_res == 1:
            self.response_time = self.response_time 
            # print(self.response_time)
        elif self.repeat_flag_res == 0:
            self.response_time = current_time - self.arrival
            self.repeat_flag_res = 1
    
    
    # Update response time of a process
    def update_wait_time(self, current_time):
        if self.repeat_flag_wait == 1:
            self.wait_time = self.wait_time 
        elif self.repeat_flag_wait == 0:
            self.wait_time = current_time - self.arrival
            self.repeat_flag_wait = 1
        
    
def fifo(processes, run_for, output_file):
    num_processes = len(processes)
    output_file.write(f"{num_processes} processes\n")
    output_file.write("Using First-Come First-Served\n")
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
                output_file.write(f"Time {current_time}: {process.name} arrived\n")

        # If there is a current process and it's finished, print and remove it
        if current_process is not None and current_process.burst == 0:
            current_process.update_turnaround_time(current_time)
            output_file.write(f"Time {current_time}: {current_process.name} finished\n")
            finished_processes.append(current_process)
            remaining_processes.remove(current_process)
            current_process = None

        # Select the next process if none is running
        if current_process is None and eligible_processes:
            next_process = eligible_processes[0]
            current_process = eligible_processes.pop(0)
            current_process.update_response_time(current_time)
            current_process.start_time = current_time
            output_file.write(f"Time {current_time}: {current_process.name} selected (burst: {current_process.burst})\n")

        # Increment wait time for all eligible processes
        for process in eligible_processes:
            if process != current_process:
                process.wait_time += 1

        # If there are no processes, print idle
        if not remaining_processes or current_process is None:
            output_file.write(f"Time {current_time}: Idle\n")

        # Increment current time and decrement burst of current process
        current_time += 1
        if current_process is not None:
            current_process.burst -= 1

    output_file.write("Finished at time " + str(current_time) + "\n\n")
    # Print wait time, turnaround time, and response time for each process
    for process in processes:
        output_file.write(f"{process.name} wait {process.wait_time} turnaround {process.turnaround_time} response {process.response_time}\n")

def sjf(processes, run_for, output_file):
    num_processes = len(processes)
    output_file.write(f"{num_processes} processes\n")
    output_file.write("Using preemptive Shortest Job First\n")

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
                output_file.write(f"Time {current_time}: {process.name} arrived\n")

        # If there is a current process and it's finished, print and remove it
        if current_process is not None and current_process.burst == 0:
            current_process.update_turnaround_time(current_time)
            output_file.write(f"Time {current_time}: {current_process.name} finished\n")
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
            output_file.write(f"Time {current_time}: {current_process.name} selected (burst: {current_process.burst})\n")

        # If there's a process with shorter burst, preempt the current process
        elif current_process is not None and eligible_processes and eligible_processes[0].burst < current_process.burst:
            next_process = eligible_processes[0]
            output_file.write(f"Time {current_time}: {next_process.name} selected (burst: {next_process.burst})\n")
            eligible_processes.append(current_process)
            current_process = eligible_processes.pop(0)
            current_process.wait_time = 0  # Reset wait time when preempted
            

        # Increment wait time for all eligible processes
        for process in eligible_processes:
            if process != current_process:
                process.wait_time += 1

        # If there are no processes, print idle
        if not remaining_processes or current_process is None:
            output_file.write(f"Time {current_time}: Idle\n")

        # Increment current time and decrement burst of current process
        current_time += 1
        if current_process is not None:
            current_process.burst -= 1

    output_file.write("Finished at time " + str(current_time) + "\n\n")
    # Print wait time, turnaround time, and response time for each process
    for process in processes:
        output_file.write(f"{process.name} wait {process.wait_time} turnaround {process.turnaround_time} response {process.response_time}\n")

def rr(processes, run_for, quantum, output_file):
    num_processes = len(processes)
    output_file.write(f"{num_processes} processes\n")
    output_file.write("Using Round-Robin\n")
    output_file.write(f"Quantum {quantum}\n\n")
    
    current_time = 0
    current_quantum = quantum
    
    remaining_processes = processes.copy()
    eligible_processes = []
    finished_processes = []
    current_process = None
    
     # Write values to the file
    output_file.write(f"Run For: {run_for}\n")
    output_file.write(f"Quantum: {quantum}\n")
    
    while current_time < run_for or current_process is not None:
        # Check for newly arrived processes
        for process in remaining_processes:
            if process.arrival == current_time:
                eligible_processes.append(process)
                output_file.write(f"Time {current_time}: {process.name} arrived\n") 
        
        # If there is a current process and it's finished, print and remove it
        if current_process is not None and current_process.burst == 0:
            current_process.update_turnaround_time(current_time)
            output_file.write(f"Time {current_time}: {current_process.name} finished\n")
            finished_processes.append(current_process)
            remaining_processes.remove(current_process)
            current_process = None

        # Select the next process if none is running
        if current_process is None and eligible_processes:
            next_process = eligible_processes[0]
            current_process = eligible_processes.pop(0)
            current_process.start_time = current_time
            current_process.update_response_time(current_time)
            
            output_file.write(f"Time {current_time}: {current_process.name} selected (burst: {current_process.burst})\n")
            current_quantum = quantum
            
        elif current_quantum == 0 and current_process is not None:
            eligible_processes.append(current_process)
            next_process = eligible_processes.pop(0)
            current_process = next_process
           
            current_process.update_response_time(current_time)
            
            output_file.write(f"Time {current_time}: {current_process.name} selected (burst: {current_process.burst})\n")
            #output_file.write("Quantum Hit\n")
            current_quantum = quantum

        # Increment wait time for all eligible processes
        for process in eligible_processes:
            if process != current_process:
                process.wait_time += 1

        # If there are no processes, print idle
        if not remaining_processes or current_process is None:
            output_file.write(f"Time {current_time}: Idle\n")

        # Increment current time and decrement burst of current process
        current_time += 1
        current_quantum -= 1
        if current_process is not None:
            current_process.burst -= 1

    output_file.write("Finished at time " + str(current_time) + "\n\n")
    # Print wait time, turnaround time, and response time for each process
    for process in processes:
        output_file.write(f"{process.name} wait {process.wait_time} turnaround {process.turnaround_time} response {process.response_time}\n")
    return 0


def read_input_file(file_path):
    # Default values
    process_count = 0
    run_for = 0
    algorithm = ""
    quantum = 0  # New variable for RR algorithm
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
                elif tokens[0] == "quantum" and algorithm == "rr":
                    quantum = int(tokens[1])
                    # print(quantum)
                elif tokens[0] == "process":
                    process_name = tokens[2]
                    arrival = int(tokens[4])
                    burst = int(tokens[6])
                    processes.append(Process(process_name, arrival, burst))
                    # print(process_name)
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)  # Exit with error code 1
    
    return  quantum,process_count, run_for, algorithm, processes

def main():
    directory = 'COPClass/InputFiles'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory 'InputFiles' created.")
    
    # Define the file path
    file_path = os.path.join(directory, 'inputFile.in')
    output_file_path = os.path.join(directory, 'inputFile.out')
    
    quantum,process_count, run_for, algorithm, processes = read_input_file(file_path)

    with open(output_file_path, 'w') as output_file:
        if algorithm == "sjf":
            sjf(processes, run_for, output_file)
        elif algorithm == "fcfs":
            fifo(processes, run_for, output_file)
        elif algorithm == "rr":
            rr(processes, run_for, quantum, output_file)
        else:
            print("Unknown algorithm:", algorithm)
    
       
    

if __name__ == "__main__":
    main()
