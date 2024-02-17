import sys
from collections import deque
# FCFS Scheduling Algorithm

# Read input from the user
input_filename = sys.argv[1]

# Read input from the file
with open(input_filename, "r") as file:
    lines = file.readlines()

# Parse input
process_count = int(lines[0].split()[1])
run_for = int(lines[1].split()[1])
algorithm = lines[2].split()[1]

processes = {}
for line in lines[3:-1]:
    tokens = line.split()
    process_name = tokens[2]
    arrival_time = int(tokens[4])
    burst_time = int(tokens[6])
    processes[process_name] = (arrival_time, burst_time)

# Sort processes based on arrival time
sorted_processes = sorted(processes.items(), key=lambda item: item[1][0])

# Initialize variables
current_time = 0
output_lines = []
waiting_times = []
turnaround_times = []
queue = deque()
all_processes = sorted_processes.copy()  # Keep a copy of all processes

# Simulate scheduling
while current_time < run_for:
    # Add arrived processes to the queue
    while sorted_processes and sorted_processes[0][1][0] <= current_time:
        queue.append(sorted_processes.pop(0))
    
    # If no process is running and the queue is empty, advance time
    if not queue:
        output_lines.append(f"Time {current_time} : Idle")
        current_time += 1
        continue

    # Get the next process from the queue
    process_name, (arrival_time, burst_time) = queue.popleft()
    
    output_lines.append(f"Time {current_time} : {process_name} arrived")
    output_lines.append(f"Time {current_time} : {process_name} selected (burst {burst_time})")
    
    # Calculate waiting time and turnaround time
    waiting_time = max(0, current_time - arrival_time)
    waiting_times.append(waiting_time)
    current_time += burst_time
    turnaround_times.append(current_time - arrival_time)
    
    output_lines.append(f"Time {current_time} : {process_name} finished")

# Handle remaining idle time
while current_time < run_for:
    output_lines.append(f"Time {current_time} : Idle")
    current_time += 1

# Print the output
output_lines.insert(0, f"{process_count} processes")
output_lines.insert(1, f"Using First-Come First-Served")
output_lines.append(f"Finished at time {current_time}\n")
for i, (process_name, _) in enumerate(all_processes):  # Use all_processes here
    output_lines.append(f"{process_name} wait {waiting_times[i]} turnaround {turnaround_times[i]} response 0")

# Write output to a file
output_filename = input_filename.replace(".in", ".out")
with open(output_filename, "w") as output_file:
    output_file.write("\n".join(output_lines))

print(f"Output written to {output_filename}")