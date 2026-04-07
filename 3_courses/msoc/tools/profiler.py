import psutil, threading, time, atexit

# Global trackers
_peak_memory_mb = 0
_start_time = time.time()

process = psutil.Process()

def memory_monitor(interval=0.2):  # check memory 5× per second
    global _peak_memory_mb
    while True:
        mem = process.memory_info().rss / 1024**2
        _peak_memory_mb = max(_peak_memory_mb, mem)
        time.sleep(interval)

        
def run_profile():
    # Start the background monitor
    thread = threading.Thread(target=memory_monitor, daemon=True)
    thread.start()

    return thread

def report_profile():
    runtime = time.time() - _start_time
    print(f"Total runtime: {runtime:.2f} seconds")
    print(f"Peak memory usage: {_peak_memory_mb:.2f} MB")
