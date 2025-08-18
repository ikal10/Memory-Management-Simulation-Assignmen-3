# A page replacement string can have any number of numbers, 
# depending on the specific problem or scenario being analyzed.
# It represents the sequence of memory pages requested by a process during execution.

import random
from typing import Optional, List, Iterable

#random - generates random numbers (needed for random page requests).
# typing - notify the reader the type of data we are using.


# function to generate the referance string.
def generate_referance_string ( length: int,                                # how many page refernces to make.
                                number_of_pages: int,                       # how mang different pages exist.
                                page_sequence: float = 0.35,                # how likey to move to the next page in order.
                                page_local: float = 0.45,                   # how liky to mve to a page near the current page.
                                page_jump: float = 0.20,                    # change of jumping randomly to a new page.
                                locality_window: int = 6,                   # how far nearby pages are.
                                phase_size: int = 200,                      # after how many requests the working set changes.
                                phase_overlap: float = 0.3,                 # how many of the old working set is kept when changing.
                                stride: Optional[int] = None,               # jumping with a fixed size.
                                stride_burst_every: int = 300,              # pages that get accessed more often than others.
                                stride_burst_length: int = 30,              # how much we favour those hot pages.
                                hot_pages: Optional[Iterable[int]] = None,  # pages that are used frequenty.
                                page_favour: float = 0.0,                   # how much we favour hot pages.
                                seed: Optional[int] = None                  # allows us to generate the same results
                              ) -> List[int]:
    
    # If we have a seed, use it so the random numbers are the same every run.  
    assert abs ((page_sequence + page_local + page_jump) - 1.0) < 1e-9, "Probabilities must sum to 1"
    if seed is not None:
        random.seed(seed)
    
    # This makes sure hot pages are valid page numbers.
    # if the list empty, we turn off the hot page feature
    if hot_pages is not None:
        hot_pages = [page for page in set(hot_pages) if 0 <= page < number_of_pages]
        if not hot_pages:
            hot_pages = None
            page_favour = 0.0

    # stores the reference string 
    reference_string = []

    working_set = random.sample(range(number_of_pages), k=min(number_of_pages, max(10, number_of_pages // 3)))  # pages currently in use
    current = random.choice(working_set)                                                                        # the first page

    # Variables for controlling stride jumps (optional mode).
    in_stride_burst = False
    stride_left = 0
    next_burst_at = stride_burst_every if stride is not None else None

    # This function pics a hot page depending on favour page
    def pick_hot():
        if hot_pages and random.random() < page_favour:
            return random.choice(hot_pages)
        return None
    
    # This changes the working set but keeps some old pages
    def swap_working_page(ws):
        keep = int(len(ws) * phase_overlap)
        kept = random.sample(ws, k=keep) if keep > 0 else []
        need = len(ws) - keep
        pool = [p for p in range(number_of_pages) if p not in kept]
        add = random.sample(pool, k=min(need, len(pool)))
        return kept + add
    
    # Main loop
    # loop through every page request we need to generate. 

    #Inside the loop

    for i in range(length):
        if phase_size > 0 and i > 0 and (i % phase_size == 0):      # change the working set if phase_size has passed.
            working_set = swap_working_page(working_set)
            
        #Handle stride bursts if and only if stride is active.
        #Maybe pick a hot page.
        #Otherwise, decide if,
        #Go to next page (page_sequential).
        #Go to a nearby page (page_local).
        #Jump randomly in the working set (page_jump).

        if stride is not None:
            if not in_stride_burst and next_burst_at is not None and i == next_burst_at:
                in_stride_burst = True
                stride_left = stride_burst_length
                next_burst_at += stride_burst_every
            if in_stride_burst and stride_left <= 0:
                in_stride_burst = False

        hot_pick = pick_hot()
        if hot_pick is not None:
            current = hot_pick
            reference_string.append(current)
            continue

        if in_stride_burst:
            candidate = (current + stride) % number_of_pages

            if candidate not in working_set:
                candidate = random.choice(working_set)
            current = candidate
            stride_left -= 1
            reference_string.append(current)
            continue

        random_unmber = random.random()
        if random_unmber < page_sequence:
            candidate = (current + 1) % number_of_pages

            if candidate not in working_set:
                candidate = random.choice(working_set)
            current = candidate

        elif random_unmber < page_sequence + page_local:
            low = max(0, current - locality_window)
            high = min(number_of_pages - 1, current + locality_window)
            candidate = random.randint(low, high)

            if candidate not in working_set:
                candidate = random.choice(working_set)
            current = candidate

        else:
            current = random.choice(working_set)

        #add page to reference string.
        reference_string.append(current)

    return reference_string


# main entry point of the program 
for i in range(10, 100, 10):
    if __name__ == "__main__":
        reference_string = generate_referance_string ( 
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
            seed  = 45
            )
        
        print("Generated Reference String:")

        print(" ".join(map(str, [reference_string])))