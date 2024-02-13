import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_time = burst
        self.start_time = None
        self.end_time = None
        self.response_time = None
        self.wait_time = None

def round_robin(processes, quantum):
    time = 0
    queue = []
    current_process = None
    finished_processes = []
    
    print(f"  {len(processes)} processes")
    print("Using Round-Robin")
    print(f"Quantum   {quantum}\n")

    while True:
        for process in processes:
            if process.arrival == time:
                queue.append(process)
                print(f"Time {time:3} : {process.name} arrived")
        
        if current_process is None and queue:
            current_process = queue.pop(0)
            current_process.start_time = time
            current_process.response_time = time - current_process.arrival
            print(f"Time {time:3} : {current_process.name} selected (burst {current_process.burst:4})")
        
        if current_process:
            current_process.remaining_time -= 1
            if current_process.remaining_time == 0:
                current_process.end_time = time + 1
                finished_processes.append(current_process)
                print(f"Time {time+1:3} : {current_process.name} finished")
                current_process = None
            elif (time - current_process.start_time) % quantum == 0:
                queue.append(current_process)
                print(f"Time {time+1:3} : {current_process.name} selected (burst {current_process.remaining_time:4})")
                current_process = None
        
        if not queue and not current_process:
            print(f"Time {time+1:3} : Idle")
        
        time += 1
        if len(finished_processes) == len(processes):
            break
    
    print(f"\nFinished at time {time}\n")
    
    for process in finished_processes:
        process.turnaround_time = process.end_time - process.arrival
        process.wait_time = process.turnaround_time - process.burst
        print(f"{process.name} wait {process.wait_time:3} turnaround {process.turnaround_time:3} response {process.response_time:3}")

def parse_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    process_count = int(lines[0].split()[1])
    run_for = int(lines[1].split()[1])
    scheduling_algorithm = lines[2].split()[1]
    quantum = int(lines[3].split()[1])
    processes = []

    for line in lines[4:]:
        if line.strip() == "end":
            break
        tokens = line.split()
        name = tokens[2]
        arrival = int(tokens[4])
        burst = int(tokens[6])
        processes.append(Process(name, arrival, burst))
    
    return run_for, quantum, processes

def main():
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py inputFile.in")
        return

    input_file = sys.argv[1]
    run_for, quantum, processes = parse_input(input_file)
    round_robin(processes, quantum)

if __name__ == "__main__":
    main()
