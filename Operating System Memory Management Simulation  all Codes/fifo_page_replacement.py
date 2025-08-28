import Page_Replacement_String_Generator as ref_st
from collections import deque  # For FIFO queue

def fifo_page_replacement(reference_string, num_frames):
    """
    Simulates FIFO page replacement.
    - reference_string: List of page accesses.
    - num_frames: Number of memory frames.
    Returns: faults, hit ratio, frame history.
    """
    frames = deque(maxlen=num_frames)  # Tracks pages in FIFO order
    page_faults = 0  # Counts faults
    hits = 0  # Counts hits
    frame_history = []  # Records frame states
    
    for page in reference_string:
        if page in frames:
            # Hit: No change to frames
            hits += 1
        else:
            # Fault: Add page, evict oldest if full
            frames.append(page)  # deque handles eviction if full
            page_faults += 1
        
        frame_history.append(list(frames))  # Snapshot frames
    
    total_accesses = len(reference_string)
    hit_ratio = hits / total_accesses if total_accesses > 0 else 0
    
    return page_faults, hit_ratio, frame_history

# Example simulation
'''for i in range(1, 6, 1):  # i will be 1, 2, 3, 4, 5
    ref_string = getattr(RF, f"REF_STR_{i}")  # Dynamically access REF_STR_i
    print(f"Ref Str {i}: ", ref_string)
    num_frames = 4
    
    faults, hit_ratio, history = fifo_page_replacement(ref_string, num_frames)
    print(f"Page Faults: {faults}")
    print(f"Hit Ratio: {hit_ratio:.2f}")
    print("Frame History:", history)
    print()  # Blank line for readability'''
    
for i in range(1, 6, 1):  # i will be 1, 2, 3, 4, 5
    print("Frame Size",i)

    ref_string= ref_st.generate_referance_string (
            length = i,
            number_of_pages = i,
            page_local = 0.45,                  
            page_jump = 0.20,                    
            locality_window = 6,                   
            phase_size = 200,                      
            phase_overlap = 0.3,                 
            stride = None,               
            stride_burst_every = 300,              
            stride_burst_length = 30,                 
            hot_pages = None,  
            page_favour = 0.0,                   
            seed  = None)
    
    #ref_string = getattr(RF, f"REF_STR_{i}")  # Dynamically access REF_STR_i
    #print(f"Ref Str {i}: ", ref_string)
    num_frames = i
    faults, hit_ratio, history = fifo_page_replacement(ref_string, num_frames)
    print(f"Page Faults: {faults}")
    print(f"Hit Ratio: {hit_ratio:.2f}")
    print("Frame History:", history)
    print()  # Blank line for readability