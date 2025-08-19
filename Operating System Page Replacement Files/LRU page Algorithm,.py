from collections import OrderedDict  # For ordered tracking of page recency
import Reference_strings as RF # To import Genrated reference strings to inssure unifyed information.



def lru(reference_string, num_frames):#Function to simulate Least Recently Used page replacement algorithm
    """

    - reference_string: List of page accesses.
    - num_frames: Number of memory frames.
    Returns: faults, hit ratio, frame history.
    """
    frames = OrderedDict()  # Tracks pages with most recent at end
    page_faults = 0  # Counts faults
    hits = 0  # Counts hits
    frame_history = []  # Records frame states
    
    for page in reference_string:
        if page in frames:
            # Hit: Update recency by moving to end
            frames.move_to_end(page)
            hits += 1
        else:
            # Fault: Evict LRU if full
            if len(frames) >= num_frames:
                frames.popitem(last=False)  # Remove least recent
            frames[page] = None  # Add new page
            page_faults += 1
        
        frame_history.append(list(frames.keys()))  # Snapshot frames
    
    total_accesses = len(reference_string)
    hit_ratio = hits / total_accesses if total_accesses > 0 else 0
    
    return page_faults, hit_ratio, frame_history

# Example simulation
#For loop to simulate LRU page relpacement for increasing pages.
for i in range(1, 6, 1):  # i will be 1, 2, 3, 4, 5
    ref_string = getattr(RF, f"REF_STR_{i}")  # Dynamically access REF_STR_i
    print(f"Ref Str {i}: ", ref_string)
    num_frames = 3
    faults, hit_ratio, history = lru(ref_string, num_frames)
    print(f"Page Faults: {faults}")
    print(f"Hit Ratio: {hit_ratio:.2f}")
    print("Frame History:", history)
    print()  # Blank line for readability


