Dynamic Memory Allocator Documentation

Overview
This is a Python-based memory allocation simulator that implements a dynamic, self-adapting memory management system. The simulator uses three allocation algorithms (Best-Fit, First-Fit, and Worst-Fit) and automatically adjusts which algorithm to use based on real-time memory conditions.

System Specifications
- Total Memory Size: 8GB (8000 MB)
- Memory Units: Megabytes (MB)
- Allocation Methods: Best-Fit, First-Fit, Worst-Fit
- Dynamic Threshold Adjustment: Automatic based on fragmentation and utilization

Core Features

1. Memory Allocation Algorithms
-  Best-Fit  : Allocates processes to the smallest suitable free block to minimize wasted space
-  First-Fit  : Allocates processes to the first suitable free block found
-  Worst-Fit  : Allocates processes to the largest suitable free block to prevent fragmentation of smaller blocks
2. Dynamic Threshold System
   The system automatically adjusts allocation method thresholds based on:
-  Memory Fragmentation Level  : How scattered free memory blocks are
-  Memory Utilization  : Percentage of total memory currently in use
-  Number of Free Blocks  : Count of separate free memory chunks

   Default Thresholds:
-  Best-Fit  : Processes < 15% of total memory (< 1200 MB)
-  First-Fit  : Processes 15% - 40% of total memory (1200 MB - 3200 MB)
-  Worst-Fit  : Processes > 40% of total memory (> 3200 MB)

3. Automatic Threshold Adjustments

   High Fragmentation (> 60%)
-  Action  : Increases Best-Fit threshold (+2%), decreases Worst-Fit threshold (-1%)
-  Goal  : More processes use Best-Fit to fill small gaps and reduce fragmentation
-  Threshold Limits  : Best-Fit max 25%, Worst-Fit min 35%

   Low Fragmentation + High Utilization (< 20% fragmentation, > 70% utilization)
-  Action  : Decreases Best-Fit threshold (-1%), increases Worst-Fit threshold (+2%)
-  Goal  : Preserve large blocks for future big processes
-  Threshold Limits  : Best-Fit min 8%, Worst-Fit max 50%

   Many Small Free Blocks (> 5 blocks)
-  Action  : Increases Best-Fit threshold (+2%)
-  Goal  : Consolidate small fragments using Best-Fit allocation
-  Threshold Limits  : Best-Fit max 20%

   Low Memory Utilization (< 30%)
-  Action  : Resets thresholds to default values (15%, 40%)
-  Goal  : Use balanced approach when memory isn't under stress

   4. Memory Management Features
-  Process Allocation  : Assigns memory blocks to named processes
-  Memory Deallocation  : Releases memory and returns it to free block pool
-  Block Coalescing  : Automatically merges adjacent free blocks to prevent fragmentation
-  Real-time Monitoring  : Displays memory usage, fragmentation levels, and current thresholds

   User Interface
   Interactive command-line menu with options:
1. Memory Allocation  : Allocate memory to a new process
2. Memory Deallocation  : Release memory from an existing process
3. Show Available Memory  : Display current memory state and statistics
0. Exit Program  : Terminate the simulator

   Technical Implementation

   Key Functions:
-  calculateFragmentation()  : Computes fragmentation ratio (1 - largest_block/total_free)
-  Adjustment()  : Automatically adjusts thresholds based on memory conditions
-  allocation()  : Allocates memory using dynamic threshold-based method selection
-  free()  : Deallocates memory and triggers block coalescing
-  merge_blocks()  : Combines adjacent free blocks to reduce fragmentation
-  showMemory()  : Displays comprehensive memory statistics

    Data Structures:
-   freeBlocks  : List of tuples (start_address, size) representing available memory
-   allocatedBlocks  : Dictionary {process_name: (start_address, size)} tracking allocated memory
-   Dynamic thresholds  : Global variables that adjust automatically

   System Benefits
1.  Adaptive Performance  : Automatically optimizes allocation strategy based on current conditions
2.  Fragmentation Management  : Actively works to reduce memory fragmentation
3.  Efficient Resource Utilization  : Balances between minimizing waste and preventing fragmentation
4.  Real-time Feedback  : Provides detailed information about allocation decisions and system state
5.  Self-Optimizing  : No manual tuning required - system learns and adapts

   Limitations and Considerations

1. Simulation Limitations
-   Not Real Memory Management  : This is a simulator, not actual OS-level memory management
-   Simplified Model  : Real memory systems have additional complexities (virtual memory, paging, etc.)
-   No Multi-threading  : Single-threaded simulation without concurrent access considerations
-   Fixed Memory Size  : Total memory size is fixed at initialization (8GB)
2. Edge Cases
- Memory Exhaustion: May not handle near-full memory conditions optimally
- Rapid Threshold Changes: Frequent adjustments might cause instability
- Single Large Process: May not handle processes larger than 50% of memory efficiently
- Empty Memory: Adjustment logic may not be optimal when memory usage is very low

3. Scalability Issues
- Fixed Thresholds: Adjustment ranges are hardcoded and may not suit all scenarios
- Limited Adaptation Range: Thresholds have fixed minimum and maximum bounds
- No Configuration: No runtime configuration options for adjustment parameters
- Memory Size Dependency: Threshold logic tied to specific memory size assumptions

Use Cases
- Educational Tool: Learning memory management concepts and algorithms
- Algorithm Comparison: Studying effectiveness of different allocation strategies
- System Design: Prototyping memory management approaches
- Performance Analysis: Understanding fragmentation and utilization trade-offs

Conclusion
This dynamic memory allocator provides a somewhat sophisticated simulation of adaptive memory management. While it has limitations as a simplified model, it effectively demonstrates how real time system conditions can be used to optimize allocation strategies automatically. The system successfully balances the competing goals of minimizing fragmentation and maximizing memory utilization through intelligent threshold adjustment.