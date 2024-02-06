class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

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
            selected_process.response_time = current_time

        # Print information
        if current_time == selected_process.arrival:
            print(f'Time  {current_time:3d} : {selected_process.name} arrived')
        print(f'Time  {current_time:3d} : {selected_process.name} selected (burst {selected_process.burst})')

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

        # Calculate wait time and turnaround time
        selected_process.wait_time = current_time - selected_process.arrival - selected_process.turnaround_time
        selected_process.turnaround_time = current_time - selected_process.arrival

        # Move finished process to the finished list
        finished_processes.append(selected_process)
        remaining_processes.remove(selected_process)

        # Print finished message
        print(f'Time  {current_time:3d} : {selected_process.name} finished')

    print(f'Finished at time  {current_time:3d}')
    print('\nProcess metrics:')
    for p in processes:
        print(f'{p.name} wait {p.wait_time:3d} turnaround {p.turnaround_time:3d} response {p.response_time:3d}')

# Define processes
processes = [
    Process(name='A', arrival=0, burst=5),
    Process(name='B', arrival=1, burst=4),
    Process(name='C', arrival=4, burst=2)
]
# Define run time
run_for = 20

# Run SJF algorithm
shortest_job_first(processes, run_for)
