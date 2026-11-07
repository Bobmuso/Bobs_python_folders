# ==========================================
# 1. Hash Table Implementation 
# ==========================================
class SuburbHashTable:
    def __init__(self):
        self.table = {}

    def add_suburb(self, suburb_name: str, incident_count: int = 0):
        """Adds or updates a suburb in the hash table."""
        key = suburb_name.strip().title()
        self.table[key] = incident_count

    def find_suburb(self, suburb_name: str) -> dict:
        """Looks up a suburb instantly."""
        key = suburb_name.strip().title()
        if key in self.table:
            return {"suburb": key, "incidents": self.table[key], "status": "Found (Hash Table)"}
        return {"error": f"Suburb '{suburb_name}' not found."}


# ==========================================
# 2. Binary Search Tree Implementation 
# ==========================================
class BSTNode:
    def __init__(self, suburb_name: str, incident_count: int = 0):
        self.suburb = suburb_name.strip().title()
        self.incidents = incident_count
        self.left = None
        self.right = None

class SuburbBST:
    def __init__(self):
        self.root = None

    def add_suburb(self, suburb_name: str, incident_count: int = 0):
        """Inserts a suburb into the BST maintaining alphabetical order."""
        name = suburb_name.strip().title()
        if not self.root:
            self.root = BSTNode(name, incident_count)
        else:
            self._insert_recursive(self.root, name, incident_count)

    def _insert_recursive(self, current: BSTNode, name: str, incidents: int):
        if name < current.suburb:
            if current.left is None:
                current.left = BSTNode(name, incidents)
            else:
                self._insert_recursive(current.left, name, incidents)
        elif name > current.suburb:
            if current.right is None:
                current.right = BSTNode(name, incidents)
            else:
                self._insert_recursive(current.right, name, incidents)
        else:
            # Update existing record if duplicate
            current.incidents = incidents

    def find_suburb(self, suburb_name: str) -> dict:
        """Searches the BST in O(log n) time."""
        name = suburb_name.strip().title()
        result = self._find_recursive(self.root, name)
        if result:
            return {"suburb": result.suburb, "incidents": result.incidents, "status": "Found (BST)"}
        return {"error": f"Suburb '{suburb_name}' not found."}

    def _find_recursive(self, current: BSTNode, name: str) -> BSTNode:
        if current is None or current.suburb == name:
            return current
        if name < current.suburb:
            return self._find_recursive(current.left, name)
        return self._find_recursive(current.right, name)

    def _in_order_traversal(self, current: BSTNode, acc: list):
        if current:
            self._in_order_traversal(current.left, acc)
            acc.append((current.suburb, current.incidents))
            self._in_order_traversal(current.right, acc)


# ==========================================
# Demonstration & Verification 
# ==========================================
if __name__ == "__main__":
    suburbs_data = [
        ("Ridgeview", 45),
        ("Pinehurst", 12),
        ("Silverton", 30),
        ("Midtown", 78),
        ("Oaklands", 19),
        ("Zastron", 8),
        ("Berea", 54),
        ("Gonubie", 22)
    ]

    print("=== INITIALIZING & POPULATING STRUCTURES ===")
    
    # 1. Populate Hash Table
    hash_index = SuburbHashTable()
    for name, count in suburbs_data:
        hash_index.add_suburb(name, count)
    print(f"Hash Table populated with {len(suburbs_data)} suburbs.")

    # 2. Populate BST
    bst_index = SuburbBST()
    for name, count in suburbs_data:
        bst_index.add_suburb(name, count)
    print(f"BST populated with {len(suburbs_data)} suburbs.")

    print("\n=== DEMONSTRATING SUBURB LOOKUPS ===")
    # Test looking up existing suburbs
    print("Hash Table Lookup ('Midtown'):", hash_index.find_suburb("Midtown"))
    print("BST Lookup ('Pinehurst'):", bst_index.find_suburb("Pinehurst"))

    # Test looking up non-existent suburb (Edge condition)
    print("Hash Table Missing Lookup ('Atlantis'):", hash_index.find_suburb("Atlantis"))

   