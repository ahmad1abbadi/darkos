import psutil
import time
import gc
from concurrent.futures import ThreadPoolExecutor
from blessings import Terminal
import concurrent.futures
import os
from threading import Lock
import multiprocessing
from multiprocessing import Process, Queue

# Initialize blessings terminal
term = Terminal()

def get_cpu_core_count():
    core_count = psutil.cpu_count(logical=False)
    return core_count

def get_cpu_info():
    cpu_info = {
        "CPU Count": psutil.cpu_count(logical=False),
        "Logical CPU Count": psutil.cpu_count(logical=True),
        "CPU Frequency": psutil.cpu_freq().current,
        "Max CPU Frequency": psutil.cpu_freq().max,
        "Memory Usage": psutil.virtual_memory().percent,
        "Available Memory": psutil.virtual_memory().available,
        "Total Memory": psutil.virtual_memory().total,
    }

    cpu_freqs = psutil.cpu_freq(percpu=True)
    for core, freq_info in enumerate(cpu_freqs):
        cpu_info[f"Core {core + 1} Frequency"] = freq_info.current
        cpu_info[f"Core {core + 1} Max Frequency"] = freq_info.max

    return cpu_info, cpu_freqs

def get_cpu_usage(process):
    return process.info['pid'], process.info['cpu_percent'], len(process.info['cpu_affinity'])

def get_file_descriptor_info(pid):
    try:
        files = psutil.Process(pid).open_files()
        file_names = [file.path for file in files]
        return file_names
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        print(f"Error getting file descriptor info for PID {pid}: {e}")
        return []

def get_shared_memory_info(pid):
    try:
        process = psutil.Process(pid)
        shared_memory_info = []

        for mmap in process.memory_maps(grouped=True):
            if mmap[0] == '[heap]':
                continue  # Skip heap memory
            if mmap[0].startswith('/dev/shm'):
                shared_memory_info.append({
                    'path': mmap[0],
                    'size': mmap[1].rss,  # Get the size from the RSS (Resident Set Size)
                })

        return shared_memory_info
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        print(f"Error getting shared memory info for PID {pid}: {e}")
        return []

def get_idle_cores():
    # Get the list of logical CPU cores
    logical_cores = list(range(psutil.cpu_count(logical=True)))

    # Get the list of currently busy cores
    busy_cores = set(psutil.cpu_percent(percpu=True, interval=0.1))

    # Find idle cores (not in busy_cores)
    idle_cores = [core for core in logical_cores if core not in busy_cores]

    return idle_cores

def get_core_score(core, current_cpu_load, cpu_freqs):
    # Calculate a score for the core based on current CPU load and frequency
    freq_score = cpu_freqs[core].current / max(cpu_freqs[core].max, 1)  # Normalize frequency
    load_score = 1 - current_cpu_load / 100  # Invert load for higher load to have a lower score
    return freq_score * load_score

def get_high_frequency_cores(cpu_freqs, num_cores=4):
    # Get the list of cores sorted by frequency in descending order
    sorted_cores = sorted(range(len(cpu_freqs)), key=lambda x: cpu_freqs[x].current, reverse=True)
    return sorted_cores[:num_cores]

def adjust_cpu_and_priority(process, num_cores_to_assign, cpu_freqs):
    try:
        # Get the current CPU load for the process
        current_cpu_load = process.cpu_percent(interval=0.1)

        # Remember the previous affinity
        previous_affinity = process.cpu_affinity()

        # Get idle cores
        idle_cores = get_idle_cores()

        # Get high-frequency cores
        high_frequency_cores = get_high_frequency_cores(cpu_freqs, num_cores_to_assign)

        # Prioritize high-frequency cores with low current CPU load
        sorted_cores = sorted(high_frequency_cores, key=lambda core: get_core_score(core, current_cpu_load, cpu_freqs), reverse=True)

        # Assign the first num_cores_to_assign cores to the process only if the affinity has changed
        if set(sorted_cores) != set(previous_affinity):
            process.cpu_affinity(sorted_cores)

            # Set the priority of the process to a higher value
            process.nice(-10)  # Adjust the nice value as needed

            print(f"Adjusted CPU affinity and priority for PID {process.info['pid']}")
        else:
            print(f"No need to adjust CPU affinity for PID {process.info['pid']}")
    except (psutil.NoSuchProcess, IndexError, psutil.AccessDenied) as e:
        print(f"Error adjusting CPU affinity and priority: {e}")

def optimize_memory_for_high_cpu_process(process, recommended_memory_gb=6):
    try:
        # Get detailed memory information
        mem_info = process.memory_full_info()

        # Convert recommended_memory_gb to kilobytes
        recommended_memory_kb = recommended_memory_gb * 1024 * 1024

        # Calculate dynamically adjusted release amount based on current memory usage
        release_amount_gb = max((mem_info.rss - recommended_memory_kb) / (1024 * 1024), 0)

        if release_amount_gb > 0:
            # Example: Release dynamically calculated amount of memory
            process.memory_info().rss -= int(release_amount_gb * 1024 * 1024)
            print(f"Released {release_amount_gb:.2f} GB of memory for PID {process.info['pid']}")

            # Trigger garbage collection to handle remaining cleanup
            gc.collect()

        else:
            print(f"No unnecessary memory to release for PID {process.info['pid']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        print(f"Error optimizing memory for process: {e}")

class ProcessInfo:
    def __init__(self, pid, cpu_usage, file_descriptors):
        self.pid = pid
        self.cpu_usage = cpu_usage
        self.file_descriptors = file_descriptors

class SharedMemory:
    def __init__(self, size):
        self.data = bytearray(size)
        self.lock = Lock()

    def set_value(self, offset, value):
        with self.lock:
            self.data[offset:offset+len(value)] = value.encode()

    def get_value(self, offset, size):
        with self.lock:
            return self.data[offset:offset+size].decode()

def get_c_process_file_info(process_to_check):
    # Replace with your platform-specific logic to identify C processes
    for process in psutil.process_iter():
        if process.info['pid'] == process_to_check.info['pid']:
            # Extract file information from the process (e.g., file descriptors, paths)
            file_info = get_file_descriptor_info(process.info['pid'])
            shared_memory_info = get_shared_memory_info(process.info['pid'])
            return file_info, shared_memory_info  # Replace with actual file information
    return None

def io_operation(shared_memory_segment, process_to_check, pid, result_queue):
    try:
        # Obtain file information and shared memory info from the specified process
        file_info, shared_memory_info = get_c_process_file_info(process_to_check)

        with shared_memory_segment.lock:
            # Assuming shared_memory_info is a dictionary containing relevant information
            serialized_process_info = pickle.dumps(ProcessInfo(process_to_check.info['pid'],
                                                              process_to_check.info['cpu_percent'],
                                                              file_info))
            
            # Assuming shared_memory_info contains necessary metadata, adjust the offsets accordingly
            shared_memory_segment.set_value(0, f"pid:{process_to_check.info['pid']}")
            shared_memory_segment.set_value(4, len(serialized_process_info).to_bytes(4, byteorder="big"))
            shared_memory_segment.set_value(8, serialized_process_info)

            # Continue with the rest of the function logic
            data = shared_memory_segment.read().decode()

            if data.startswith("pid:"):
                offset = 4
                pid_value = int(data[4:offset])
                offset += 4
                cpu_usage_size = int(data[offset:offset+4])
                offset += 4
                cpu_usage = data[offset:offset+cpu_usage_size]
                offset += cpu_usage_size
                file_descriptors_size = int(data[offset:offset+4])
                offset += 4
                file_descriptors = data[offset:offset+file_descriptors_size]
                process_info = pickle.loads(cpu_usage + file_descriptors)

                # Use pid_value as needed in the function
                # ...

                # I/O processing logic with process_info
                processed_data = "Processed result"

                # Put the processed data into the result_queue
                result_queue.put(processed_data)

            else:
                data = json.loads(data)
                file_paths = data["file_paths"]
                results = multiprocessing.Pool().map(read_file_async, file_paths)
                for result in results:
                    process_data(result)

    except Exception as e:
        logger.error(f"Error in I/O operation: {e}")

def cpu_memory():
    try:
        # Create a Queue for communication within the same process
        result_queue = Queue()

        with ThreadPoolExecutor() as executor:
            while True:
                cpu_info_future = executor.submit(get_cpu_info)
                processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'cpu_affinity'])
                cpu_usage_futures = list(executor.map(get_cpu_usage, processes))

                cpu_info, cpu_freqs = cpu_info_future.result()

                cpu_core_count = get_cpu_core_count()

                high_usage_process = max(processes, key=lambda process: process.info['cpu_percent'], default=None)

                if high_usage_process:
                    adjust_cpu_and_priority(high_usage_process, num_cores_to_assign, cpu_freqs)

                if high_usage_process and high_usage_process.info['cpu_percent'] > 50:
                    optimize_memory_for_high_cpu_process(high_usage_process, recommended_memory_gb=5)

                    # Check if the process has more than 10 files for I/O parallelization

                    shared_memory.set_value(0, pid.to_bytes(4, byteorder="big"))
                    shared_memory.set_value(4, len(serialized_process_info).to_bytes(4, byteorder="big"))
                    shared_memory.set_value(8, serialized_process_info)

                    # Call io_operation with the result_queue and high_usage_process
                    io_operation(shared_memory, high_usage_process, pid, result_queue)

                    # Retrieve the processed data from the result_queue
                    processed_data = result_queue.get()

                    # Get file information for the high CPU process
                    file_info = get_file_descriptor_info(high_usage_process.info['pid'])
                    num_files = len(file_info)
                    print(f"Number of files in use by PID {high_usage_process.info['pid']}: {num_files}")

                low_usage_processes = [process for process in processes
                                       if process.info['cpu_percent'] < 5 and process.info['create_time'] < time.time() - 10]

                for process in low_usage_processes:
                    idle_cores = get_idle_cores()
                    low_scoring_cores = get_high_frequency_cores(cpu_freqs, num_cores_to_assign)
                    sorted_cores = sorted(low_scoring_cores,
                                          key=lambda core: get_core_score(core, 0, cpu_freqs),
                                          reverse=False)
                    process.cpu_affinity(sorted_cores)

                    print(f"Assigned low-scoring cores for PID {process.info['pid']}")

                with term.fullscreen():
                    print(term.clear)
                    print("CPU Info:")
                    for key, value in cpu_info.items():
                        print(f"{key}: {value}")

                    print("\nCPU Usage:")
                    for process_pid, process_usage, process_core_count in cpu_usage_futures:
                        print(f"PID {process_pid}: {process_usage}% (Using {process_core_count} cores)")
                        num_files = len(get_file_descriptor_info(process_pid))
                        print(f"Number of files for PID {process_pid}: {num_files}")

                    print("\nMemory Info:")
                    print(f"Memory Usage: {cpu_info['Memory Usage']}%")
                    print(f"Available Memory: {cpu_info['Available Memory']} bytes")
                    print(f"Total Memory: {cpu_info['Total Memory']} bytes")

                time.sleep(0.5)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    cpu_memory()

