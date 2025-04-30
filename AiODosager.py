import tkinter as tk
from tkinter import ttk, messagebox
from scapy.all import IP, ICMP, TCP, send
import subprocess

# Function to handle Ping
def send_ping():
    site = entry_ping_site.get()
    count = entry_ping_count.get()

    if not site:
        messagebox.showerror("Error", "Please enter a site to ping.")
        return

    if not count.isdigit() or int(count) <= 0:
        messagebox.showerror("Error", "Please enter a valid number of pings.")
        return

    try:
        # Execute the ping command with the specified number of pings
        result = subprocess.run(
    ["ping", "-c", count, site],  # Use '-c' on Linux, NOT '-n'
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

        if result.returncode == 0:
            messagebox.showinfo("Ping Result", f"Ping successful:\n{result.stdout}")
        else:
            messagebox.showerror("Ping Result", f"Ping failed:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle ICMP Packet Sending
def send_icmp_packet():
    target_ip = entry_icmp_ip.get()
    packet_count = entry_icmp_count.get()

    if not target_ip:
        messagebox.showerror("Error", "Please enter a target IP address or hostname.")
        return

    if not packet_count.isdigit() or int(packet_count) <= 0:
        messagebox.showerror("Error", "Please enter a valid number of packets.")
        return

    try:
        # Create an IP packet
        ip_packet = IP(dst=target_ip)
        
        # Create an ICMP packet
        icmp_packet = ICMP()
        
        # Combine the IP and ICMP packets
        packet = ip_packet / icmp_packet
        
        # Send the packet the specified number of times
        for _ in range(int(packet_count)):
            send(packet, verbose=False)
        
        messagebox.showinfo("Success", f"{packet_count} ICMP packet(s) sent to {target_ip}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle SYN Packet Sending
def send_syn_packet():
    target_ip = entry_syn_ip.get()
    target_port = entry_syn_port.get()

    if not target_ip:
        messagebox.showerror("Error", "Please enter a target IP address.")
        return

    if not target_port.isdigit() or int(target_port) <= 0:
        messagebox.showerror("Error", "Please enter a valid port number.")
        return

    try:
        # Create an IP packet
        ip_packet = IP(dst=target_ip)
        
        # Create a TCP packet with SYN flag set
        tcp_packet = TCP(dport=int(target_port), flags="S")
        
        # Combine IP and TCP packets
        packet = ip_packet / tcp_packet
        
        # Send the packet
        send(packet, verbose=False)
        messagebox.showinfo("Success", f"SYN packet sent to {target_ip}:{target_port}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("AIO Dosager Network Tool Suite V.1.0")

# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create Ping Tab
ping_tab = ttk.Frame(notebook)
notebook.add(ping_tab, text="Ping")

tk.Label(ping_tab, text="Enter site to ping:").pack(pady=5)
entry_ping_site = tk.Entry(ping_tab, width=30)
entry_ping_site.pack(pady=5)

tk.Label(ping_tab, text="Enter number of pings:").pack(pady=5)
entry_ping_count = tk.Entry(ping_tab, width=10)
entry_ping_count.pack(pady=5)

ping_button = tk.Button(ping_tab, text="Ping", command=send_ping)
ping_button.pack(pady=10)

# Create ICMP Tab
icmp_tab = ttk.Frame(notebook)
notebook.add(icmp_tab, text="ICMP Packet")

tk.Label(icmp_tab, text="Enter target IP or hostname:").pack(pady=5)
entry_icmp_ip = tk.Entry(icmp_tab, width=30)
entry_icmp_ip.pack(pady=5)

tk.Label(icmp_tab, text="Enter number of packets:").pack(pady=5)
entry_icmp_count = tk.Entry(icmp_tab, width=10)
entry_icmp_count.pack(pady=5)

icmp_button = tk.Button(icmp_tab, text="Send ICMP Packet", command=send_icmp_packet)
icmp_button.pack(pady=10)

# Create SYN Tab
syn_tab = ttk.Frame(notebook)
notebook.add(syn_tab, text="SYN Packet")

tk.Label(syn_tab, text="Enter target IP:").pack(pady=5)
entry_syn_ip = tk.Entry(syn_tab, width=30)
entry_syn_ip.pack(pady=5)

tk.Label(syn_tab, text="Enter target port:").pack(pady=5)
entry_syn_port = tk.Entry(syn_tab, width=10)
entry_syn_port.pack(pady=5)

syn_button = tk.Button(syn_tab, text="Send SYN Packet", command=send_syn_packet)
syn_button.pack(pady=10)

# Run the application
root.mainloop()
