class SafeRouteSystem:
    def __init__(self):
        # R2: Vehicle Registry 
        self.vehicle_registry = {}
        
        # R1: Priority Queue 
        self.incident_heap = []
        self._sequence_counter = 0

    # ==========================================
    # R2: Vehicle Lookup & Registration
    # ==========================================
    def register_vehicle(self, reg_number: str, vehicle_type: str, status: str, crew_lead: str):
        if not reg_number or not isinstance(reg_number, str):
            raise ValueError("Registration number must be a valid non-empty string.")
        key = reg_number.strip().upper()
        self.vehicle_registry[key] = {
            "vehicle_type": vehicle_type,
            "status": status,
            "crew_lead": crew_lead
        }

    def lookup_vehicle(self, reg_number: str) -> dict:
        """Handles non-existent vehicle registrations."""
        if not reg_number or not isinstance(reg_number, str):
            return {"error": "Invalid registration format provided."}
        
        key = reg_number.strip().upper()
        # Check if the vehicle exists in the hash table
        if key not in self.vehicle_registry:
            return {"error": f"Lookup Failed: Vehicle registration '{reg_number}' not found in network."}
        
        return self.vehicle_registry[key]

    # ==========================================
    # R1: Incident Intake & Priority Management
    # ==========================================
    def log_incident(self, priority, description: str):
        """Validates priority/severity before inserting into the heap."""
        # Check for missing, non-integer, or out-of-range priority values
        if not isinstance(priority, int) or not (1 <= priority <= 5):
            print(f"-> [Validation Error Rejected]: Incident '{description}' has invalid priority '{priority}'. Must be an integer between 1 (Critical) and 5 (Routine).")
            return False

        if not description or not description.strip():
            print("-> [Validation Error Rejected]: Incident description cannot be empty.")
            return False

        self._sequence_counter += 1
        item = (priority, self._sequence_counter, description.strip())
        self.incident_heap.append(item)
        self._sift_up(len(self.incident_heap) - 1)
        print(f"-> [Logged Successfully]: [Priority {priority}] {description}")
        return True

    def dispatch_next(self):
        """Handles empty queue dispatch attempts safely."""
        if not self.incident_heap:
            print("-> [Dispatch Warning]: No incidents currently waiting in the queue. Dispatch system is idle.")
            return None
        
        self.incident_heap[0], self.incident_heap[-1] = self.incident_heap[-1], self.incident_heap[0]
        min_item = self.incident_heap.pop()
        if self.incident_heap:
            self._sift_down(0)
            
        priority, _, description = min_item
        return priority, description

    # Heap Helper Methods
    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.incident_heap[index] < self.incident_heap[parent]:
                self.incident_heap[index], self.incident_heap[parent] = self.incident_heap[parent], self.incident_heap[index]
                index = parent
            else:
                break

    def _sift_down(self, index):
        length = len(self.incident_heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < length and self.incident_heap[left] < self.incident_heap[smallest]:
                smallest = left
            if right < length and self.incident_heap[right] < self.incident_heap[smallest]:
                smallest = right

            if smallest != index:
                self.incident_heap[index], self.incident_heap[smallest] = self.incident_heap[smallest], self.incident_heap[index]
                index = smallest
            else:
                break


# ==========================================
# Demonstration of Error Handling & Edge Cases
# ==========================================
if __name__ == "__main__":
    system = SafeRouteSystem()

    # Setup valid data
    system.register_vehicle("CA 456-789", "Ambulance", "Available", "Paramedic J. Smith")

    print("1. Handling Empty Queue Dispatch ")
    system.dispatch_next()  # Attempting to dispatch when queue is empty

    print("\n 2. Handling Non-Existent Vehicle Lookup ")
    result = system.lookup_vehicle("XY 999-ZZ")  # Vehicle not in registry
    print(f"Lookup Result: {result}")

    print("\n 3. Handling Invalid Priority / Severity ")
    system.log_incident(priority="Emergency", description="Structure fire on 5th Ave") # Invalid type (string)
    system.log_incident(priority=10, description="Flooding on Main Road")              # Out of range (max is 5)
    system.log_incident(priority=1, description="Cardiac arrest at Maple Street")      # Valid priority