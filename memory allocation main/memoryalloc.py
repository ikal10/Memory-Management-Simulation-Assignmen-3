memorySize = 8000    #starting memory size in Megabytes (8gb)
freeBlocks = [(0, memorySize)]  # 0 represents the start address
allocatedBlocks = {} # keeping track of all allocated processes

#dynamic memory thresholds default values
bestFitThreshold = 15.0
worstFitThreshold = 40.0

def calculateFragmentation():
    if not freeBlocks:
        return 0
    TotalFreeMemory = sum(size for start, size in freeBlocks)
    if TotalFreeMemory == 0:
        return 0
    LargestFreeBlock = max(size for start, size in freeBlocks)
    fragmentation = 1 - (LargestFreeBlock / TotalFreeMemory)
    return fragmentation

#function to dynamically adjust threshold based on memory allocations
def Adjustment():
    global bestFitThreshold
    global worstFitThreshold
    fragmentation = calculateFragmentation()
    memoryUsage = sum(size for start, size in allocatedBlocks.values()) / memorySize
    numFreeBlocks = len(freeBlocks)

    #high fragmentation > 0.6 in favor of best fit
    if fragmentation > 0.6:
        bestFitThreshold = min(25.0, bestFitThreshold + 2)
        worstFitThreshold = max(35.0, worstFitThreshold - 1)
        reason = "high fragmentation detected"
    elif fragmentation < 0.2 and memoryUsage > 0.7:
        bestFitThreshold = max(8.0, bestFitThreshold - 1)
        worstFitThreshold = min(50.0, worstFitThreshold + 2)
        reason = "low fragmentation with high utilization"
    elif numFreeBlocks > 5:
        bestFitThreshold = min(20.0, bestFitThreshold + 2)
        reason = "many small free blocks detected"
    elif memoryUsage < 0.3:
        bestFitThreshold = 15.0  # Reset to default
        worstFitThreshold = 40.0  # Reset to default
        reason = "low memory utilization - using balanced approach"
    else:
        reason = "stable conditions"
        return

    # Ensure bestFitThreshold < worstFitThreshold
    if bestFitThreshold >= worstFitThreshold:
        worstFitThreshold = bestFitThreshold + 5
    print(f"dynamic adjustment: best-fit: {bestFitThreshold:.2f} | worst-fit: {worstFitThreshold:.2f} | reason: {reason}")
    print(f"Fragmentation: {fragmentation:.2f}, Utilization: {memoryUsage:.2f}, Free blocks: {numFreeBlocks}")

#memory allocation
def allocation(processName, size): #default allocation will be first fit
    global freeBlocks, allocatedBlocks, memorySize, bestFitThreshold, worstFitThreshold  #making these variables global to use in each code scope/block
    # Automatically adjust thresholds before each allocation
    Adjustment()
    chosen_index = None

    methods = [(i, start, block_size) for i, (start, block_size) in enumerate(freeBlocks) if block_size >= size ]
    if not methods:
        print(f"Memory error, no block is big enough for {processName} ({size}MB)")
        return
    #automatic selection based on dynamic threshold
    #small use best fit
    if size < memorySize * (bestFitThreshold / 100):    #converting percentage to decimal, eg 15 to 0.15MBs
        best_i, best_start, best_size = min(methods, key=lambda x: x[2])    #smallest block
        chosen_index = best_i
        method = "best-fit"
    #large process use worst fit
    elif size > memorySize * (worstFitThreshold / 100):
        worst_i, worst_start, worst_size = max(methods, key=lambda x: x[2]) #largest block
        chosen_index = worst_i
        method = "worst-fit"
    else:
        #for medium size process in between worst fit and best fit use first fit
        chosen_index = methods[0][0]
        method = "first-fit"

    #log where putting the process
    start, block_size = freeBlocks[chosen_index]
    print(f"Allocation: {processName} -> Start Address: {start}, Size: {size}MB, Allocation Method used: {method}")
    allocatedBlocks[processName] = (start, size)
    #if whole block is what we need exactly we need we remove it, if its big we cut the allocated part and shrink the hole
    if block_size == size:
        freeBlocks.pop(chosen_index)
    else:
        freeBlocks[chosen_index] = (start + size, block_size - size)
#releasing memory
def free(processName):
    global freeBlocks, allocatedBlocks
    if processName not in allocatedBlocks:
        print(f"Error: could not locate {processName}, ensure correct spelling and try again")
        return

    start, size = allocatedBlocks.pop(processName)
    print(f"deallocating: {processName}, Size: {size}MB")
    freeBlocks.append((start, size))
    freeBlocks.sort()
    merge_blocks() #merge functions will merge all the free memory holes

#coalescing
def merge_blocks():
    global freeBlocks
    merged = []
    for blocks in freeBlocks:
        if merged and merged[-1][0] + merged[-1][1] == blocks[0]:
            merged[-1] = (merged[-1][0], merged[-1][1] + blocks[1])
        else:
            merged.append(blocks)
    freeBlocks = merged

#function show memory
def showMemory():
    totalFree = sum(size for start, size in freeBlocks)
    totalAllocated = sum(size for start, size in allocatedBlocks.values())
    print(f"Free blocks: {freeBlocks}")
    print(f"allocated: {allocatedBlocks}")
    print(f"Memory usage: {totalAllocated:.2f}MB allocated ({totalAllocated/memorySize*100:.1f}%), "
    f"{totalFree:.2f}MB free ({totalFree/memorySize*100:.1f}%)")

while True:
    print("----MEMORY SIMULATION----")
    print(" select an option ")
    print("1. memory allocation")
    print("2. memory deallocation")
    print("3. show available memory")
    print("0. exit program")
    userInput = int(input("-> "))
    if userInput == 1:
        processName = input("enter process name: ")
        processSize = float(input("enter process size in megabytes (MB): "))
        showMemory()
        allocation(processName, processSize)
        showMemory()
    elif userInput == 2:
        processName = input("enter process name to deallocate memory: ")
        showMemory()
        free(processName)
        showMemory()
    elif userInput == 3:
        print("current memory state:")
        showMemory()
    elif userInput == 0:
        print("----->exiting program....")
        break

