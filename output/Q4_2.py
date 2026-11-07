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
            current.incidents = incidents

    def generate_alphabetical_report(self) -> list:
        """
        Produces an alphabetical listing of all indexed suburbs
        """
        sorted_suburbs = []
        self._in_order(self.root, sorted_suburbs)
        return sorted_suburbs

    def _in_order(self, node: BSTNode, result_list: list):
        if node is not None:
            # 1. Visit left subtree (all suburbs alphabetically earlier)
            self._in_order(node.left, result_list)
            # 2. Visit current node
            result_list.append((node.suburb, node.incidents))
            # 3. Visit right subtree (all suburbs alphabetically later)
            self._in_order(node.right, result_list)


# ==========================================
# Execution & Evidence of Output
# ==========================================
if __name__ == "__main__":
    bst_index = SuburbBST()
    
    # Populating in arbitrary, unsorted order
    unsorted_suburbs = [
        ("Ridgeview", 45), ("Pinehurst", 12), ("Silverton", 30),
        ("Midtown", 78), ("Oaklands", 19), ("Zastron", 8),
        ("Berea", 54), ("Gonubie", 22)
    ]
    
    for name, count in unsorted_suburbs:
        bst_index.add_suburb(name, count)

    print("=== SafeRoute Monthly Alphabetical Suburb Report ===")
    report = bst_index.generate_alphabetical_report()
    for index, (suburb, count) in enumerate(report, start=1):
        print(f"{index}. {suburb:<12} | Total Incidents: {count}")