from collections import Counter

def analyze_tle_inclinations(tle_file_path):
    inclinations = []
    
    with open(tle_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # TLEs consist of lines where Line 2 contains the inclination 
    # in character indices 8 to 16
    for i in range(len(lines)):
        line = lines[i].strip()
        # Identify Line 2 of the TLE (usually starts with '2 ')
        if line.startswith('2 '):
            try:
                # Extract the inclination value (columns 8 to 16 in the TLE specification)
                inc_str = line[8:16].strip()
                # Round to 2 decimal places to group close planes
                inc = round(float(inc_str), 2)
                inclinations.append(inc)
            except ValueError:
                continue

    # Count how many satellites belong to each inclination plane
    inclination_counts = Counter(inclinations)
    
    # Calculate the average inclination
    if inclinations:
        average_inclination = sum(inclinations) / len(inclinations)
    else:
        average_inclination = 0.0

    print("--- Orbital Planes Distribution (Inclination) ---")
    print(f"{'Inclination (°)':<15} | {'Satellite Count':<15}")
    print("-" * 33)
    for inc, count in sorted(inclination_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{inc:<15} | {count:<15}")
        
    print("-" * 33)
    print(f"Average Inclination: {average_inclination:.2f}")

# --- Example of usage ---
# Make sure the generated satellites.tle file is in the folder
analyze_tle_inclinations('satellites.tle')