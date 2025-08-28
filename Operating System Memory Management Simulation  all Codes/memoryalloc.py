memorySize = 8000    #starting memory size in Megabytes (8gb)
freeBlocks = [(0, memorySize)]  # 0 represents the start address
allocatedBlocks = {} # keeping track of all allocated processes

#memory allocation
def allocation(processName, size): #default allocation will be first fit
    global freeBlocks, allocatedBlocks, memorySize  #making free blocks, memorySize and allocatedBlocks global to use in each code scope/block
    chosen_index = None

    methods = [(i, start, block_size) for i, (start, block_size) in enumerate(freeBlocks) if block_size >= size ]
    if not methods:
        print(f"Memory error, no block is big enough for {processName} ({size}KB)")
        return
    #automatic selection
    #small process <= 1200mbs = best fit
    if size < memorySize * 0.15:
        best_i, best_start, best_size = min(methods, key=lambda x: x[2])    #smallest block
        chosen_index = best_i
        method = "best-fit"
    #large process >= 3200mbs = worst fit
    elif size > memorySize * 0.4:
        worst_i, worst_start, worst_size = max(methods, key=lambda x: x[2]) #largest block
        chosen_index = worst_i
        method = "worst-fit"
    else:
        #medium size process 1200mbs to 3200mbs = first fit
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



