import time

def run_performance_benchmark():
    # Define two distinct dataset scales for provincial growth simulation
    dataset_sizes = [10000, 100000]
    
    print(f"{'Dataset Size (n)':<18} | {'Hash Table Lookup (s)':<22} | {'Linear Search (s)':<20}")
    print("-" * 68)

    for n in dataset_sizes:
        # Populate structures with mock vehicle data
        hash_table = {}
        vehicle_list = []
        
        for i in range(n):
            reg = f"REG {i:06d} GP"
            record = {"reg": reg, "type": "Ambulance", "status": "Available"}
            hash_table[reg] = record
            vehicle_list.append(record)
            
        target_reg = f"REG {n - 1:06d} GP"  # worst-case for linear search
        
        # Benchmark Hash Table over 1,000 lookups
        start_time = time.perf_counter()
        for _ in range(1000):
            _ = hash_table.get(target_reg)
        hash_time = (time.perf_counter() - start_time) / 1000.0
        
        # Benchmark Linear Search 1,000 lookups
        start_time = time.perf_counter()
        for _ in range(1000):
            found = None
            for item in vehicle_list:
                if item["reg"] == target_reg:
                    found = item
                    break
        linear_time = (time.perf_counter() - start_time) / 1000.0
        
        print(f"{n:<18} | {hash_time:<22.8f} | {linear_time:<20.8f}")

if __name__ == "__main__":
    run_performance_benchmark()