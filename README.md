# Preemptive Shortest Job First (SJF) Scheduling Algorithm

This repository contains Python code implementing a preemptive Shortest Job First (SJF) scheduling algorithm. SJF is a scheduling policy that selects the waiting process with the smallest execution time to execute next.

## Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [SJF Algorithm Steps](#sjf-algorithm-steps)
- [License](#license)

## Introduction

The code simulates the execution of processes in a preemptive SJF scheduling environment. It reads process information from an input file, runs the SJF algorithm on the processes, and prints out the scheduling details such as wait time, turnaround time, and response time for each process.

## Features

- Implements preemptive Shortest Job First (SJF) scheduling algorithm.
- Reads input process information from a text file.
- Calculates and prints wait time, turnaround time, and response time for each process.
- Handles invalid input and file errors gracefully.

## Requirements

- Python 3.x (I used Ubuntu)

## SJF Algorithm Steps
  - Initialization: Initialize current time and other variables.
  - Process Arrival: Check for newly arrived processes.
  - Process Completion: If there is a current process and it's finished, mark it as completed.
  - Select Next Process: Select the next process if none is running.
  - Idle Check: If there are no processes or the CPU is idle, print "Idle".
  - Preemption: If there's a process with a shorter burst, preempt the current process.
  - Execution: Increment current time and decrement burst of the current process.
  - Completion: Repeat steps 2-7 until all processes are completed.

## SJF_Function.py Check
  - c2-sjf.in WORKS
  - Webcourses example WORKS
  - c10-sjf.in WORKS
  - c5-sjf.in WORKS

  For some reason there is a promblme only when its a process that need to be replaced before finishing since there is a shorter process that arrived
