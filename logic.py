from collections import deque

# 1. DSA: Using a Queue (deque) for Alert Processing
# Why: In a real system, alerts come in bursts. A Queue (FIFO) 
# ensures we process them in the exact order they occurred.
class AlertManager:
    def __init__(self, max_alerts=50):
        # We use a deque for O(1) append and pop performance
        self.alert_queue = deque(maxlen=max_alerts)

    def trigger_alert(self, server_name: str, metric_value: float):
        """
        Logic: String manipulation and conditional filtering.
        """
        # Programming Logic: Clean the string (Capitalize)
        clean_name = server_name.strip().upper()
        
        if metric_value > 90.0:
            msg = f"CRITICAL: {clean_name} is at {metric_value}% CPU!"
            self.alert_queue.append(msg)
            return True
        return False

    def get_next_alert(self):
        # DSA: Pop from the start of the queue
        if self.alert_queue:
            return self.alert_queue.popleft()
        return "System Stable: No Alerts."

# 2. ALGORITHMS: Ranking Logic
# Demonstrating sorting (Internal Quick Sort/Merge Sort logic)
def get_top_stressed_servers(server_list):
    """
    Takes a list of server objects and sorts them by CPU usage.
    Complexity: O(n log n)
    """
    # Logic: Using a lambda to sort complex objects
    return sorted(server_list, key=lambda x: x.cpu_usage, reverse=True)

# 3. STRING MANIPULATION & LOGIC
def format_ip_safely(ip_address: str):
    """
    Logic: Sanitizing input data before it hits the database.
    """
    return ip_address.replace(" ", "").strip()