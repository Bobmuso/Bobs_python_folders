class SuburbHashTable:
    def __init__(self):
        self.table = {}

    def add_suburb(self, suburb_name: str, incident_count: int = 0):
        """Adds or updates a suburb in the hash table."""
        key = suburb_name.strip().title()
        self.table[key] = incident_count

    def find_suburb(self, suburb_name: str) -> dict:
        """Looks up a suburb instantly in O(1) average time."""
        key = suburb_name.strip().title()
        if key in self.table:
            return {"suburb": key, "incidents": self.table[key], "status": "Found"}
        return {"error": f"Suburb '{suburb_name}' not found in index."}

    def remove_suburb(self, suburb_name: str) -> bool:
        """
        [EXTENSION] Removes a suburb from the hash table index 
        in O(1) average time complexity.
        """
        key = suburb_name.strip().title()
        if key in self.table:
            del self.table[key]
            return True
        return False


# ==========================================
# Demonstration & Verification
# ==========================================
if __name__ == "__main__":
    hash_index = SuburbHashTable()

    # 1. Populate initial suburbs
    suburbs_data = [
        ("Ridgeview", 45),
        ("Pinehurst", 12),
        ("Silverton", 30),
        ("Midtown", 78)
    ]
    for name, count in suburbs_data:
        hash_index.add_suburb(name, count)

    print("=== Initial State: Before Removal ===")
    print("Lookup 'Pinehurst':", hash_index.find_suburb("Pinehurst"))
    print("Total Suburbs in Index:", len(hash_index.table))

    print("\n=== Executing Removal Operation ===")
    removed = hash_index.remove_suburb("Pinehurst")
    print(f"Removal Status for 'Pinehurst': {'Success' if removed else 'Failed'}")

    print("\n=== Final State: After Removal ===")
    print("Lookup 'Pinehurst' (Expected Error):", hash_index.find_suburb("Pinehurst"))
    print("Total Suburbs in Index:", len(hash_index.table))