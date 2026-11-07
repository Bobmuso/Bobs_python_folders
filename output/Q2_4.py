class SafeRouteSystem:
    def __init__(self):
        self.vehicle_registry = {}
        self.incident_heap = []
        self._sequence_counter = 0

    def register_vehicle(self, reg_number: str, vehicle_type: str, status: str, crew_lead: str):
        key = reg_number.strip().upper()
        self.vehicle_registry[key] = {
            "vehicle_type": vehicle_type,
            "status": status,
            "crew_lead": crew_lead
        }

    def lookup_vehicle(self, reg_number: str) -> dict:
        key = reg_number.strip().upper()
        if key not in self.vehicle_registry:
            return {"error": f"Lookup Failed: Vehicle '{reg_number}' not found."}
        return self.vehicle_registry[key]

    def log_incident(self, priority, description: str):
        if not isinstance(priority, int) or not (1 <= priority <= 5):
            print(f"-> [TC4 REJECTED]: Invalid priority '{priority}'. Must be 1-5.")
            return False
        self._sequence_counter += 1
        self.incident_heap.append((priority, self._sequence_counter, description))
        self._sift_up(len(self.incident_heap) - 1)
        return True

    def dispatch_next(self):
        if not self.incident_heap:
            print("-> [TC3 WARNING]: No incidents waiting in queue. System idle.")
            return None
        self.incident_heap[0], self.incident_heap[-1] = self.incident_heap[-1], self.incident_heap[0]
        min_item = self.incident_heap.pop()
        if self.incident_heap:
            self._sift_down(0)
        return min_item[0], min_item[2]

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
# Automated Test Runner Execution
# ==========================================
if __name__ == "__main__":
    system = SafeRouteSystem()

    print("=== TEST CASE 1: Priority Incident Intake & Dispatch (Normal) ===")
    system.log_incident(3, "Routine noise complaint")
    system.log_incident(1, "Cardiac arrest emergency")
    system.log_incident(1, "Highway collision")
    
    print("Executing Dispatches:")
    while system.incident_heap:
        prio, desc = system.dispatch_next()
        print(f"   Dispatched -> [Priority {prio}]: {desc}")

    print("\n=== TEST CASE 2: Vehicle Lookup (Normal) ===")
    system.register_vehicle("CA 456-789", "Ambulance", "Available", "Paramedic J. Smith")
    res = system.lookup_vehicle("CA 456-789")
    print(f"   Lookup Result: {res}")

    print("\n=== TEST CASE 3: Empty Queue Dispatch (Edge Condition) ===")
    system.dispatch_next()

    print("\n=== TEST CASE 4: Invalid Priority & Non-Existent Lookup (Failure Conditions) ===")
    system.log_incident(10, "Invalid priority test")  # Out of range priority
    missing_res = system.lookup_vehicle("XY 999-ZZ")  # Unregistered vehicle
    print(f"   Missing Vehicle Lookup Result: {missing_res}")