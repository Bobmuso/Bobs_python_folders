import heapq
import random
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple


VALID_PRIORITIES = {"routine", "critical"}


class IncidentPriorityQueue:
    """Fifo-with-priority queue: critical incidents go before routine incidents."""

    def __init__(self):
        self._heap: List[Tuple[int, int, str]] = []
        self._sequence = 0

    def add_incident(self, description: str, priority: str) -> None:
        normalized = priority.strip().lower()
        if normalized not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority '{priority}'. Use 'routine' or 'critical'."
            )
        if not description or not description.strip():
            raise ValueError("Incident description cannot be empty.")
        priority_rank = -1 if normalized == "critical" else 0
        heapq.heappush(self._heap, (priority_rank, self._sequence, description.strip()))
        self._sequence += 1

    def dispatch_next(self) -> str:
        if not self._heap:
            raise IndexError("No incidents are waiting to be dispatched.")
        _, _, incident = heapq.heappop(self._heap)
        return incident

    def peek(self) -> str:
        if not self._heap:
            raise IndexError("No incidents are waiting to be dispatched.")
        _, _, incident = self._heap[0]
        return incident

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return len(self) > 0


def demo_incident_queue():
    print("\n2.1 - Incident priority queue")
    queue = IncidentPriorityQueue()
    incidents = [
        ("Noise complaint near River Road", "routine"),
        ("Cardiac arrest outside Northfield Clinic", "critical"),
        ("Minor fender-bender near Riverside Ave", "routine"),
        ("Structure fire with trapped residents", "critical"),
    ]

    for description, priority in incidents:
        queue.add_incident(description, priority)

    print("Dispatch order:")
    while queue:
        print(" -", queue.dispatch_next())


class VehicleRegistry:
    """Hash-table based lookup keyed by registration/fleet number."""

    def __init__(self):
        self._vehicles: Dict[str, Dict[str, Any]] = {}

    def add_vehicle(self, registration: str, **details: Any) -> None:
        key = registration.strip().upper()
        if not key:
            raise ValueError("Registration number cannot be empty.")
        self._vehicles[key] = {"registration": key, **details}

    def get_vehicle(self, registration: str) -> Dict[str, Any]:
        key = registration.strip().upper()
        if key not in self._vehicles:
            raise KeyError(f"Vehicle '{registration}' was not found.")
        return self._vehicles[key]

    def __contains__(self, registration: str) -> bool:
        return registration.strip().upper() in self._vehicles

    def __len__(self):
        return len(self._vehicles)


def demo_vehicle_registry():
    print("\n2.2 - Vehicle registry")
    registry = VehicleRegistry()
    registry.add_vehicle("AB 123", unit_type="Ambulance", crew="Alpha-1", suburb="Riverside")
    registry.add_vehicle("CF 456", unit_type="Fire engine", crew="Bravo-2", suburb="Northfield")
    registry.add_vehicle("TR 789", unit_type="Traffic-response", crew="Charlie-7", suburb="Harbour Point")

    print("Vehicle lookup result for AB 123:")
    print(registry.get_vehicle("AB 123"))


class HashTable:
    """Simple hash table for suburb lookup."""

    def __init__(self, size: int = 11):
        self.size = size
        self.table: List[Optional[List[Tuple[str, Any]]]] = [None] * size

    def _hash(self, key: str) -> int:
        return sum(ord(ch) for ch in key) % self.size

    def add(self, key: str, value: Any) -> None:
        index = self._hash(key)
        bucket = self.table[index]
        if bucket is None:
            self.table[index] = [(key, value)]
            return
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def find(self, key: str) -> Any:
        index = self._hash(key)
        bucket = self.table[index]
        if bucket is None:
            raise KeyError(f"Suburb '{key}' not found.")
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        raise KeyError(f"Suburb '{key}' not found.")

    def items(self) -> Iterable[Tuple[str, Any]]:
        for bucket in self.table:
            if bucket:
                for item in bucket:
                    yield item

    def __contains__(self, key: str) -> bool:
        try:
            self.find(key)
            return True
        except KeyError:
            return False


class SuburbNode:
    def __init__(self, suburb: str, incident_count: int = 0):
        self.suburb = suburb
        self.incident_count = incident_count
        self.left: Optional[SuburbNode] = None
        self.right: Optional[SuburbNode] = None


class SuburbBST:
    """Binary search tree for suburb records and ordering."""

    def __init__(self):
        self.root: Optional[SuburbNode] = None

    def add(self, suburb: str, incident_count: int = 0) -> None:
        suburb = suburb.strip()
        if not suburb:
            raise ValueError("Suburb name cannot be empty.")

        def insert(node: Optional[SuburbNode]) -> SuburbNode:
            if node is None:
                return SuburbNode(suburb, incident_count)
            if suburb.lower() < node.suburb.lower():
                node.left = insert(node.left)
            elif suburb.lower() > node.suburb.lower():
                node.right = insert(node.right)
            else:
                node.incident_count = max(node.incident_count, incident_count)
            return node

        self.root = insert(self.root)

    def find(self, suburb: str) -> SuburbNode:
        suburb = suburb.strip()

        def search(node: Optional[SuburbNode]) -> SuburbNode:
            if node is None:
                raise KeyError(f"Suburb '{suburb}' not found.")
            if suburb.lower() < node.suburb.lower():
                return search(node.left)
            if suburb.lower() > node.suburb.lower():
                return search(node.right)
            return node

        return search(self.root)

    def inorder(self) -> List[str]:
        result: List[str] = []

        def walk(node: Optional[SuburbNode]) -> None:
            if node is None:
                return
            walk(node.left)
            result.append(node.suburb)
            walk(node.right)

        walk(self.root)
        return result

    def add_incident(self, suburb: str) -> None:
        try:
            node = self.find(suburb)
            node.incident_count += 1
        except KeyError:
            self.add(suburb, incident_count=1)



def demo_suburb_indexes():
    print("\n4.1 - Suburb index structures")
    suburb_names = [
        "Riverside",
        "Harbour Point",
        "Northfield",
        "Cedar Valley",
        "Westmere",
        "Lakeside",
        "Oakridge",
        "Hillview",
    ]

    hash_table = HashTable()
    for suburb in suburb_names:
        hash_table.add(suburb, {"suburb": suburb, "incident_count": 0})

    bst = SuburbBST()
    for suburb in suburb_names:
        bst.add(suburb, incident_count=0)

    print("Hash table lookup for 'Northfield':")
    print(hash_table.find("Northfield"))
    print("BST lookup for 'Northfield':")
    print(bst.find("Northfield").suburb)

    print("\n4.2 - Alphabetical suburb listing")
    print("Alphabetical order from BST:")
    print(bst.inorder())

    print("\n4.3 - Extended BST to track incident counts")
    extended = SuburbBST()
    for suburb in ["Riverside", "Northfield", "Westmere", "Riverside", "Northfield"]:
        extended.add_incident(suburb)
    for suburb in ["Riverside", "Northfield", "Westmere"]:
        node = extended.find(suburb)
        print(f"{suburb}: {node.incident_count} incidents")


def path_exists(graph: Dict[str, Iterable[str]], start: str, goal: str, visited: Optional[set] = None) -> bool:
    if start == goal:
        return True
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbour in graph.get(start, []):
        if neighbour == goal:
            return True
        if neighbour not in visited and path_exists(graph, neighbour, goal, visited):
            return True
    return False


def demo_path_search():
    print("\n3.1 - Recursive DFS path check")
    road_network = {
        "depot": ["Northfield", "River Road"],
        "Northfield": ["depot", "Harbour Point"],
        "River Road": ["depot", "Harbour Point", "Oakridge"],
        "Harbour Point": ["Northfield", "River Road", "Cedar Hill"],
        "Oakridge": ["River Road"],
        "Cedar Hill": ["Harbour Point"],
    }
    print("Path from depot to Cedar Hill exists?", path_exists(road_network, "depot", "Cedar Hill"))
    print("Path from depot to Oakridge exists?", path_exists(road_network, "depot", "Oakridge"))


def benchmark_lookup_performance() -> None:
    print("\n2.5 - Lookup performance comparison")
    sizes = [1000, 10000]
    iterations = 2000

    print(f"{'Data size':>10} {'Dict lookup':>12} {'List lookup':>12}")
    for size in sizes:
        vehicle_dict = {f"VF-{i:05d}": {"registration": f"VF-{i:05d}", "crew": f"Crew-{i%50}"} for i in range(size)}
        registry_keys = list(vehicle_dict)

        start = time.perf_counter()
        for _ in range(iterations):
            target = random.choice(registry_keys)
            _ = target in vehicle_dict
        dict_time = time.perf_counter() - start

        list_vehicles = registry_keys
        start = time.perf_counter()
        for _ in range(iterations):
            target = random.choice(registry_keys)
            _ = target in list_vehicles
        list_time = time.perf_counter() - start

        print(f"{size:>10} {dict_time:>12.6f}s {list_time:>12.6f}s")

    print("\nInterpretation: as the dataset grows, the hash-table lookup remains effectively constant on average,")
    print("while the unsorted list lookup grows linearly because each membership check scans more entries.")
    print("This supports the decision to use a hash-table for rapid vehicle lookup in a provincial network.")



def run_demo() -> None:
    print("SafeRoute proof-of-concept")
    demo_incident_queue()
    demo_vehicle_registry()
    demo_path_search()
    demo_suburb_indexes()
    benchmark_lookup_performance()

    print("\n2.3 - Error handling")
    queue = IncidentPriorityQueue()
    try:
        queue.dispatch_next()
    except IndexError as exc:
        print(exc)

    registry = VehicleRegistry()
    try:
        registry.get_vehicle("ZZ-999")
    except KeyError as exc:
        print(exc)

    try:
        queue.add_incident("", "critical")
    except ValueError as exc:
        print(exc)

    try:
        queue.add_incident("Unclear task", "urgent")
    except ValueError as exc:
        print(exc)

    print("\n2.4 - Test cases")

    def normal_dispatch_case():
        q = IncidentPriorityQueue()
        q.add_incident("Routine job", "routine")
        return q.dispatch_next()

    def priority_order_case():
        q = IncidentPriorityQueue()
        q.add_incident("Routine job", "routine")
        q.add_incident("Critical cardiac arrest", "critical")
        first = q.dispatch_next()
        second = q.dispatch_next()
        return [first, second]

    test_cases = [
        ("normal dispatch", normal_dispatch_case, "Routine job"),
        ("priority ordering", priority_order_case, ["Critical cardiac arrest", "Routine job"]),
        ("missing vehicle lookup", lambda: registry.get_vehicle("ZZ-999"), "KeyError"),
        ("invalid priority", lambda: IncidentPriorityQueue().add_incident("Invalid", "urgent"), "ValueError"),
    ]

    for name, action, expected in test_cases:
        try:
            result = action()
            if isinstance(expected, list):
                print(f"{name}: expected {expected!r}, actual {result!r}")
            else:
                print(f"{name}: expected {expected!r}, actual {result!r}")
        except Exception as exc:
            print(f"{name}: expected {expected!r}, actual {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    run_demo()
