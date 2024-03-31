import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
import queue

class Nixmap:
    def __init__(self, ip, start_port, end_port, result_queue):
        self.ip = ip
        self.start_port = start_port
        self.end_port = end_port
        self.result_queue = result_queue

    def scan(self):
        for port in range(self.start_port, self.end_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((self.ip, port))
                    if result == 0:
                        self.result_queue.put(f'Port {port} is open\n')
            except Exception as e:
                self.result_queue.put(f'Error scanning port {port}: {str(e)}\n')

    def start(self):
        threading.Thread(target=self.scan).start()

def start_scan():
    ip = host_entry.get()
    # You can adjust the port range if needed
    nixmap = Nixmap(ip, 1, 65535, result_queue)
    nixmap.start()

def process_queue():
    while not result_queue.empty():
        result = result_queue.get()
        results_text.insert(tk.END, result)
    root.after(100, process_queue)

root = tk.Tk()
root.geometry('600x400')

result_queue = queue.Queue()

host_entry = tk.Entry(root)
host_entry.pack()

scan_button = tk.Button(root, text='Scan', command=start_scan)
scan_button.pack()

results_text = tk.scrolledtext.ScrolledText(root)
results_text.pack()

root.after(100, process_queue)
root.mainloop()
