class VehicleRegistry:
    def __init__(self):
        # Internal hash table 
        self.registry = {}

    def register_vehicle(self, reg_number: str, vehicle_type: str, status: str, crew_lead: str):
        """
        Stores a vehicle record using its registration number as the lookup key.
        Normalizes the key (uppercase, stripped) to ensure robust lookups.
        """
        key = reg_number.strip().upper()
        self.registry[key] = {
            "vehicle_type": vehicle_type,
            "status": status,
            "crew_lead": crew_lead
        }

    def lookup_vehicle(self, reg_number: str) -> dict:
        """
        Retrieves a vehicle's details
        """
        key = reg_number.strip().upper()
        return self.registry.get(key, {"error": "Vehicle registration missing."})


# ==========================================
# Demonstration & Verification
# ==========================================
if __name__ == "__main__":
    fleet_system = VehicleRegistry()

    print("--- Registering Fleet Vehicles ---")
    
    # 1. Add first vehicle record
    fleet_system.register_vehicle(
        reg_number="CA 456-789", 
        vehicle_type="Advanced Life Support Ambulance", 
        status="Available", 
        crew_lead="Paramedic J. Smith"
    )
    print("Registered: CA 456-789 (Ambulance)")

    # 2. Add second vehicle record
    fleet_system.register_vehicle(
        reg_number="GP 999-WJ", 
        vehicle_type="Heavy Rescue Fire Engine", 
        status="En Route", 
        crew_lead="Capt. D. Molefe"
    )
    print("Registered: GP 999-WJ (Fire Engine)")

    # 3. Add third vehicle record
    fleet_system.register_vehicle(
        reg_number="EC 123-456", 
        vehicle_type="Rapid Traffic Response Unit", 
        status="On Scene", 
        crew_lead="Officer T. Khumalo"
    )
    print("Registered: EC 123-456 (Traffic Response)")

    print("\n--- Executing Target Vehicle Lookup ---")
    target_plate = "GP 999-WJ"
    details = fleet_system.lookup_vehicle(target_plate)
    
    print(f"Lookup Query: {target_plate}")
    print(f"Retrieved Details: {details}")