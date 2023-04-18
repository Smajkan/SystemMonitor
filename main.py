import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import tkinter as tk

def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    mem_used = round(mem.used/1024/1024/1024, 2)
    mem_total = round(mem.total/1024/1024/1024, 2)
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_used = round(disk.used/1024/1024/1024, 2)
    disk_total = round(disk.total/1024/1024/1024, 2)
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv
    return {
        'CPU Usage': cpu_percent,
        'Memory Usage': mem_percent,
        'Memory Used': mem_used,
        'Memory Total': mem_total,
        'Disk Usage': disk_percent,
        'Disk Used': disk_used,
        'Disk Total': disk_total,
        'Bytes Sent': bytes_sent,
        'Bytes Received': bytes_recv
    }

def update_gui():
    system_info = get_system_info()
    cpu_label.config(text=f'CPU Usage: {system_info["CPU Usage"]}%')
    mem_label.config(text=f'Memory Usage: {system_info["Memory Usage"]}% ({system_info["Memory Used"]}GB / {system_info["Memory Total"]}GB)')
    disk_label.config(text=f'Disk Usage: {system_info["Disk Usage"]}% ({system_info["Disk Used"]}GB / {system_info["Disk Total"]}GB)')
    sent_label.config(text=f'Bytes Sent: {system_info["Bytes Sent"]}')
    recv_label.config(text=f'Bytes Received: {system_info["Bytes Received"]}')
    cpu_usage_data.append(system_info['CPU Usage'])
    cpu_usage_plot.clear()
    cpu_usage_plot.bar(range(len(cpu_usage_data)), cpu_usage_data, align='center')
    cpu_usage_plot.set_ylim([0, 100])
    cpu_usage_plot.set_xlabel('Time (s)')
    cpu_usage_plot.set_ylabel('CPU Usage (%)')
    cpu_usage_canvas.draw()
    root.after(1000, update_gui)

root = tk.Tk()
root.title('System Monitor')
root.geometry('600x300')

title_label = tk.Label(root, text='System Monitor', font=('Arial', 18))
title_label.pack(pady=10)

cpu_label = tk.Label(root, text='CPU Usage: %', font=('Arial', 14), fg='white', bg='#006666')
mem_label = tk.Label(root, text='Memory Usage: %', font=('Arial', 14), fg='white', bg='#006666')
disk_label = tk.Label(root, text='Disk Usage: %', font=('Arial', 14), fg='white', bg='#006666')
sent_label = tk.Label(root, text='Bytes Sent: ', font=('Arial', 14), fg='white', bg='#006666')
recv_label = tk.Label(root, text='Bytes Received: ', font=('Arial', 14), fg='white', bg='#006666')

cpu_label.pack(fill='x', padx=10)
mem_label.pack(fill='x', padx=10)
disk_label.pack(fill='x', padx=10)
sent_label.pack(fill='x', padx=10)
recv_label.pack(fill='x', padx=10)

fig = plt.Figure(figsize=(5, 3), dpi=100)
cpu_usage_plot = fig.add_subplot(111)
cpu_usage_data = []
cpu_usage_canvas = FigureCanvasTkAgg(fig, master=root)
cpu_usage_canvas.get_tk_widget().pack(side='left', fill='both', expand=1)

update_gui()

# Start the Tkinter event loop
root.mainloop()
