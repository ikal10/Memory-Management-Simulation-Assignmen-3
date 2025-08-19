#Memory Allocation2 


class SimulationBlock:
    def __init__(self, address, size, is_free=True):
        self.address = address  
        self.size = size       
        self.is_free = is_free 
        self.next = None       
        self.prev = None       

class VintageChunk:
    def __init__(self, total_size):
        
        self.head = SimulationBlock(0, total_size)
    
    def allocate(self, size):
        current = self.head
        while current:
            
            if current.is_free and current.size >= size:
                
                if current.size > size + 16:  # Extra space for new block data
                    new_block = SimulationBlock(current.address + size, current.size - size)
                    new_block.is_free = True
                    new_block.next = current.next
                    new_block.prev = current
                    if current.next:
                        current.next.prev = new_block
                    current.next = new_block
                    current.size = size
                current.is_free = False
                return current.address
            current = current.next
        return None  # No suitable block found
    
    def deallocate(self, address):
        current = self.head
        # Find the block with the given address
        while current and current.address != address:
            current = current.next
        if not current:
            return  # Invalid address
        current.is_free = True
        
        # combine with next block if it's free
        if current.next and current.next.is_free:
            current.size += current.next.size
            current.next = current.next.next
            if current.next:
                current.next.prev = current
        
        # Merge with previous block if it's free
        if current.prev and current.prev.is_free:
            current.prev.size += current.size
            current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
    
    def Show(self):
        
        current = self.head
        while current:
            status = "Free" if current.is_free else "Used"
            print(f"Block at {current.address}: Size = {current.size}, Status = {status}")
            current = current.next


if __name__ == "__main__":
    
    pool = VintageChunk(1000)
    
    # Allocate some memory
    print("Allocating 200 bytes:")
    addr1 = pool.allocate(200)
    print(f"Allocated at address: {addr1}")
    pool.Show()
    
    print("\nAllocating 300 bytes:")
    addr2 = pool.allocate(300)
    print(f"Allocated at address: {addr2}")
    pool.Show()
    
    print("\nDeallocating address 200:")
    pool.deallocate(200)
    pool.Show()