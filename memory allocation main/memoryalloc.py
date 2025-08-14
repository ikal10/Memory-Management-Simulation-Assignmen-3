memorySize = 100
freeBlocks = [(0, memorySize)]

#just show memory first
def showMemory():
    print(f"Free blocks: {freeBlocks}")

#memory allocation
def allocation(processName, size, method="first"): #default alloction will be first fit
    global freeBlocks #ensuring global is global in each code block
    chosen_index = None

    #first fit
    if method == "first":
        for i, (start, block_size) in enumerate(freeBlocks):
            if block_size >= size:
                chosen_index = i
                break
    #best fit
    elif method == "best":
        best_size = float("inf")
        for i, (start, block_size) in enumerate(freeBlocks):
            if block_size >= size and block_size < best_size:
                best_size = block_size
                chosen_index = i
    #worst fit
    elif method == "worst":
        worstSize = -1
        for i, (start, block_size) in enumerate(freeBlocks):
            if block_size >= size and block_size > worstSize:
                worstSize = block_size
                chosen_index = i
    #if no blocks chosen is big enough
    if chosen_index is None:
        print(f"Memory error, no block is big enough for {processName} ({size})")
        return
    #log where putting the process
    start, block_size = freeBlocks[chosen_index]
    print(f"Allocation: {processName} -> Start {start}, Size{size}")
    #if whole is what we need exaclty we need we remove it, if its big we cut the allocated part and shrink the hole
    if block_size == size:
        freeBlocks.pop(chosen_index)
    else:
        freeBlocks[chosen_index] = (start + size, block_size - size)
#releasing memory
def free(processStart, size):
    global freeBlocks
    print(f"release: start {processStart}, Size {size}")
    freeBlocks.append((processStart, size))
    freeBlocks.sort()
    merge_blocks() ##merge functions will merge all the free holes

def merge_blocks():
    global freeBlocks
    merged = []
    for blocks in freeBlocks:
        if merged and merged[-1][0] + merged[-1][1] == blocks[0]:
            merged[-1] = (merged[-1][0], merged[-1][1] + blocks[1])
        else:
            merged.append(blocks)
            freeBlocks = merged

showMemory()
allocation("A", 10, method="first")
allocation("B", 20, method="first")
allocation("C", 5, method="first")
showMemory()

free(10, 20)
showMemory()

allocation("D", 18, method="first")
showMemory()

allocation("E", 3, method="best")
showMemory()

allocation("F", 15, method="worst")
showMemory()
