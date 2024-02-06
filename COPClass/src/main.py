import os
import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

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
   
#Done Erik Dokken
def shortest_job_first(processes, run_for):
    current_time = 0
    finished_processes = []
    remaining_processes = processes.copy()

    print(f'{len(processes)} processes')
    print('Using preemptive Shortest Job First')

    while current_time < run_for or remaining_processes:
        # Find processes that have arrived by the current time
        eligible_processes = [p for p in remaining_processes if p.arrival <= current_time]

        if not eligible_processes:  # If no process arrived yet, increment time
            print(f'Time  {current_time:3d} : Idle')
            current_time += 1
            continue

        # Sort eligible processes by burst time
        eligible_processes.sort(key=lambda x: x.burst)

        # Select the shortest job
        selected_process = eligible_processes[0]

        # Calculate response time if it's the first time executing the process
        if selected_process.response_time == -1:
            selected_process.response_time = current_time - selected_process.arrival

        # Calculate wait time
        wait_time = current_time - selected_process.arrival
        selected_process.wait_time = wait_time

        # Print information
        if current_time == selected_process.arrival:
            print(f'Time  {current_time:3d} : {selected_process.name} arrived')
        print(f'Time  {current_time:3d} : {selected_process.name} selected (burst {selected_process.burst}, wait {selected_process.wait_time})')

        # Execute the process one unit at a time
        for _ in range(selected_process.burst):
            current_time += 1
            selected_process.burst -= 1

            # Check if a new process has arrived
            for p in remaining_processes:
                if p.arrival == current_time:
                    print(f'Time  {current_time:3d} : {p.name} arrived')
                    eligible_processes.append(p)

            # Sort eligible processes by burst time
            eligible_processes.sort(key=lambda x: x.burst)

            # Check if the selected process has finished
            if selected_process.burst == 0:
                break

        # Calculate turnaround time
        selected_process.turnaround_time = current_time - selected_process.arrival

        # Move finished process to the finished list
        finished_processes.append(selected_process)
        remaining_processes.remove(selected_process)

        # Print finished message
        print(f'Time  {current_time:3d} : {selected_process.name} finished')

    print(f'Finished at time  {current_time:3d}')
    print('\nProcess metrics:')
    for p in processes:
        print(f'{p.name} wait {p.wait_time:3d} turnaround {p.turnaround_time:3d} response {p.response_time:3d} ')
        
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
       shortest_job_first(processes, run_for)
    

if __name__ == "__main__":
    main()
