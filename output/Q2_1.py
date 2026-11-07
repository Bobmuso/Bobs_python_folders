class SafeRoutePriorityQueue:
    def __init__(self):
        self.heap = []
        self._sequence_counter = 0  

    def log_incident(self, priority, description):
        """
        Logs an incident into the priority queue.
        1 = Critical, 3 = Routine
        """
        self._sequence_counter += 1
        # Tuple structure: priority, counter, description
        item = (priority, self._sequence_counter, description)
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def dispatch_next(self):
        """Removes and returns the highest-priority incident."""
        if not self.heap:
            return None
        
        # Swap the minimum element with the last element
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        min_item = self.heap.pop()  # Remove the minimum item from the end
        
        if self.heap:
            self._sift_down(0)
            
        priority, _, description = min_item
        return priority, description

    def _sift_up(self, index):
        """Restores heap property by moving an element up."""
        while index > 0:
            parent = (index - 1) // 2
            # Comparison 
            if self.heap[index] < self.heap[parent]:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break

    def _sift_down(self, index):
        """Restores heap property by sinking an element down."""
        length = len(self.heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < length and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < length and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break


# ==============
# Demonstration 
# ==============
if __name__ == "__main__":
    system = SafeRoutePriorityQueue()

    print("--- Logging Incoming Incidents ---")
    
    # 1. Routine call arriving first
    system.log_incident(priority=3, description="Routine: Noise complaint on Elm Street")
    print("Logged [Priority 3]: Routine: Noise complaint on Elm Street")

    # 2. Critical call arriving second
    system.log_incident(priority=1, description="Critical: Cardiac arrest at Central Station")
    print("Logged [Priority 1]: Critical: Cardiac arrest at Central Station")

    # 3. Another routine call arriving third
    system.log_incident(priority=3, description="Routine: Minor parking dispute on 4th Ave")
    print("Logged [Priority 3]: Routine: Minor parking dispute on 4th Ave")

    # 4. Critical call arriving fourth
    system.log_incident(priority=1, description="Critical: Multi-vehicle highway collision with entrapment")
    print("Logged [Priority 1]: Critical: Multi-vehicle highway collision with entrapment")

    print("\n--- Dispatch Execution Order ---")
    while system.heap:
        prio, desc = system.dispatch_next()
        print(f"-> Dispatched [Priority {prio}]: {desc}")