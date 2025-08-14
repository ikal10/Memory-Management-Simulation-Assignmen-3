memory Allocation Simulator

Overview
This Python script simulates memory allocation and deallocation using different strategies:
- First-fit
- Best-fit
- Worst-fit

Features
- Tracks free memory blocks in a simulated memory space of size 100
- Supports three allocation methods:
  - First-fit: allocates the first suitable block found
  - Best-fit: allocates the smallest suitable block
  - Worst-fit: allocates the largest suitable block
- Automatically merges adjacent free blocks during deallocation
- Provides visualization of current memory state

Usage
1. Run the script: `python memoryalloc.py`
2. The demo sequence will:
   - Show initial memory state
   - Allocate processes A, B, C using first-fit
   - Free process B's memory
   - Allocate process D using first-fit
   - Allocate process E using best-fit
   - Allocate process F using worst-fit

Functions
- `showMemory()`: Displays current free memory blocks
- `allocation(processName, size, method)`: Allocates memory for a process
- `free(processStart, size)`: Releases memory back to the free pool

Example Output
The script will print allocation/deallocation actions and show memory state after each operation.