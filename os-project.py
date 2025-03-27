def fifo_page_replacement(pages, frame_size):
    memory = []
    page_faults = 0

    for page in pages:
        if page not in memory:
            if len(memory) < frame_size:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1

    return page_faults

pages = [1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 3, 4, 5]
frame_size = 3
print(f"Total Page Faults: {fifo_page_replacement(pages, frame_size)}")