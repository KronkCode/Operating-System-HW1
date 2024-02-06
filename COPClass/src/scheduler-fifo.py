import sys
import re

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.in'):
        print("Usage: python scheduler-gpt.py inputFile.in")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = input_filename.replace('.in', '.out')

    processes = []
    time_ticks = 0
    current_process = None
    remaining_burst_time = 0
    idle = False

    with open(input_filename, 'r') as input_file:
        lines = [line.strip() for line in input_file.readlines() if not line.startswith('#')]

        process_count = int(re.search(r'\d+', lines[0].split("#")[0]).group())
        runtime_value = int(lines[1].split("#")[0].split()[1])

        for line in lines[2:]:
            if line.startswith("process name"):
                parts = line.split()
                name = parts[3]
                arrival_match = re.search(r'\d+', line)
                burst_match = re.search(r'\d+', line)

                if arrival_match and burst_match:
                    arrival_time = int(arrival_match.group())
                    burst_time = int(burst_match.group())
                    processes.append(Process(name, arrival_time, burst_time))
                else:
                    print("Error: Unable to extract arrival or burst time from the input line.")
                    sys.exit(1)

        with open(output_filename, 'w') as output_file:
            output_file.write(f"{process_count} processes\nUsing FCFS\n")

            while time_ticks <= runtime_value or current_process or processes:
                if current_process is None and processes:
                    current_process = processes.pop(0)
                    current_process.response_time = time_ticks

                if current_process:
                    remaining_burst_time -= 1
                    output_file.write(f"Time {time_ticks} : {current_process.name} selected (burst {current_process.burst_time})\n")
                    current_process.burst_time -= 1

                    if current_process.burst_time == 0:
                        current_process.turnaround_time = time_ticks - current_process.arrival_time
                        current_process.wait_time = current_process.turnaround_time - current_process.response_time
                        output_file.write(f"Time {time_ticks} : {current_process.name} finished\n")
                        current_process = None
                        remaining_burst_time = 0
                else:
                    output_file.write(f"Time {time_ticks} : Idle\n")
                    idle = True

                if not idle:
                    time_ticks += 1
                else:
                    idle = False

    print(f"Output written to {output_filename}")

if __name__ == "__main__":
    main()