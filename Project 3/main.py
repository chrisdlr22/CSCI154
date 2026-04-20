import numpy as np

def generate_customers(num_customers=160, hours=8):
    """Generates a list of dictionaries representing customers and their needs."""
    # Customers arrive uniformly across the 8-hour working day
    arrivals = np.random.uniform(0, hours, num_customers)
    arrivals.sort() # Sort chronologically
    
    customers = []
    for arrival_time in arrivals:
        # Generate work units N(5, 0.5) truncated to [5, 15]
        work_units = -1
        while not (5 <= work_units <= 15):
            work_units = np.random.normal(5, 0.5)
            
        # At 10 work-units/hr, service time in hours is work_units / 10
        service_time = work_units / 10.0 
        
        customers.append({
            "arrival_time": arrival_time,
            "work_units": work_units,
            "service_time": service_time
        })
        
    return customers

def simulate_bank_fifo(customers, num_windows=10, operating_hours=8):
    """Simulates a standard FIFO queue and returns wait times and unserved count."""
    # Track when each window will next be free (initially all are free at t=0)
    windows_free_time = [0.0] * num_windows 
    wait_times = []
    unserved_count = 0
    
    for customer in customers:
        arrival = customer["arrival_time"]
        
        # The earliest available window is the one with the minimum free time
        windows_free_time.sort()
        earliest_window_time = windows_free_time[0]
        
        # If the bank is closed before service can even start, the customer is unserved
        if arrival > operating_hours or max(arrival, earliest_window_time) > operating_hours:
            unserved_count += 1
            continue
            
        # Service starts either when the customer arrives, or when the window frees up
        service_start = max(arrival, earliest_window_time)
        wait_time = service_start - arrival
        wait_times.append(wait_time)
        
        # Update this window's free time to when it will finish with this customer
        windows_free_time[0] = service_start + customer["service_time"]
        
    # Convert wait times to minutes for easier reading
    wait_times_minutes = [w * 60 for w in wait_times]
    avg_wait = np.mean(wait_times_minutes) if wait_times_minutes else 0
    
    return avg_wait, unserved_count

# ==========================================
# Main Execution and Experimentation
# ==========================================
if __name__ == "__main__":
    np.random.seed(42) # For reproducible results
    
    # Run a single day as a test
    daily_customers = generate_customers()
    
    # 1. Base Scenario: 10 Windows
    avg_wait_10, unserved_10 = simulate_bank_fifo(daily_customers, num_windows=10)
    print(f"--- Standard Setup (10 Windows) ---")
    print(f"Average Wait: {avg_wait_10:.2f} minutes")
    print(f"Unserved Customers: {unserved_10}\n")
    
    # 2. Add an extra window
    avg_wait_11, unserved_11 = simulate_bank_fifo(daily_customers, num_windows=11)
    print(f"--- Extra Window (11 Windows) ---")
    print(f"Average Wait: {avg_wait_11:.2f} minutes")
    print(f"Unserved Customers: {unserved_11}\n")
    
    # 3. Remove a window
    avg_wait_9, unserved_9 = simulate_bank_fifo(daily_customers, num_windows=9)
    print(f"--- One Less Window (9 Windows) ---")
    print(f"Average Wait: {avg_wait_9:.2f} minutes")
    print(f"Unserved Customers: {unserved_9}\n")