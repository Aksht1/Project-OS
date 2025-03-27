import random
import time

MEMORY_SIZE = 50
TIME_STEPS = 15  # Number of time steps for simulation

# Class to represent a memory block
class MemoryBlock:
    def __init__(self, start, size, process_id, allocated_time):
        self.start = start  # Starting address
        self.size = size    # Size of the block
        self.process_id = process_id  # ID of the process using this block
        self.allocated_time = allocated_time  # Time when block was allocated
        self.freed_time = None  # Time when block was freed (None if still allocated)

# Class to manage memory and visualize allocation
class MemoryManager:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.memory_blocks = []  # List of allocated memory blocks
        self.time = 0  # Current time step

    def allocate(self, size, process_id):
        # Find a free space using First-Fit algorithm
        if size > self.memory_size:
            print(f"Process {process_id}: Requested size {size} is too large for memory!")
            return False

        # Sort blocks by start address to find gaps
        self.memory_blocks.sort(key=lambda x: x.start)
        current_pos = 0

        # Look for a free space
        for block in self.memory_blocks:
            if block.freed_time is not None:  # Skip freed blocks
                continue
            if current_pos + size <= block.start:  # Found a gap
                new_block = MemoryBlock(current_pos, size, process_id, self.time)
                self.memory_blocks.append(new_block)
                print(f"Process {process_id}: Allocated {size} units at address {current_pos}")
                return True
            current_pos = block.start + block.size

        # Check if there's space at the end of memory
        if current_pos + size <= self.memory_size:
            new_block = MemoryBlock(current_pos, size, process_id, self.time)
            self.memory_blocks.append(new_block)
            print(f"Process {process_id}: Allocated {size} units at address {current_pos}")
            return True

        print(f"Process {process_id}: No free space for {size} units!")
        return False

    def deallocate(self, process_id):
        # Deallocate memory for a given process
        for block in self.memory_blocks:
            if block.process_id == process_id and block.freed_time is None:
                block.freed_time = self.time
                print(f"Process {process_id}: Deallocated {block.size} units at address {block.start}")
                return True
        print(f"Process {process_id}: No allocated memory found to deallocate!")
        return False

    def visualize(self):
        # Create a text-based visualization of the memory state
        memory_display = ['-'] * self.memory_size  # Initialize memory with free slots ('-')

        # Fill in allocated blocks
        for block in self.memory_blocks:
            if block.freed_time is None or block.freed_time > self.time:  # Block is still allocated
                for i in range(block.start, block.start + block.size):
                    memory_display[i] = f"P{block.process_id}"

        # Print the memory state
        print(f"\nTime Step {self.time}:")
        print("Memory State: [", end="")
        for i in range(self.memory_size):
            print(memory_display[i], end="")
            if (i + 1) % 10 == 0:  # Add spacing for readability
                print(" ", end="")
        print("]")
        print(f"Legend: '-' = Free, P<Number> = Process ID")

        self.time += 1

# Simulate memory management
def simulate_memory_management():
    manager = MemoryManager(MEMORY_SIZE)

    # Simulate allocation and deallocation over time
    for t in range(TIME_STEPS):
        print(f"\n=== Time Step {t} ===")
        # Randomly decide to allocate or deallocate
        action = random.choice(["allocate", "deallocate", "none"])

        if action == "allocate":
            process_id = random.randint(0, 4)  # Random process ID (0 to 4)
            size = random.randint(5, 10)  # Random size between 5 and 10
            manager.allocate(size, process_id)
        elif action == "deallocate":
            process_id = random.randint(0, 4)  # Random process ID
            manager.deallocate(process_id)

        # Visualize the memory state
        manager.visualize()
        time.sleep(1)  # Add a delay to make the simulation easier to follow

# Run the simulation
if __name__ == "__main__":
    simulate_memory_management()