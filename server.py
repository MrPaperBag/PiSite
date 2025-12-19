from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

PORT = 80

def cmd(command):
    return subprocess.check_output(command, shell=True).decode().strip()

def get_stats():
    # Pi model (most reliable)
    try:
        pi_model = cmd("tr -d '\\0' </proc/device-tree/model")
    except:
        pi_model = "Raspberry Pi"

    # CPU architecture
    cpu_arch = cmd("lscpu | grep 'Model name' | cut -d: -f2").strip()
    if not cpu_arch:
        cpu_arch = cmd("lscpu | grep 'Architecture' | cut -d: -f2").strip()

    # SoC
    try:
        soc = cmd("vcgencmd otp_dump | grep 30: | cut -d: -f2")
        soc = "BCM" + soc[:4]
    except:
        soc = "Broadcom SoC"

    # CPU temperature
    cpu_temp = float(cmd("vcgencmd measure_temp | cut -d= -f2 | cut -d\"'\" -f1"))
    cpu_bar = min(int(cpu_temp), 100)

    # RAM
    mem = cmd("free -m").splitlines()[1].split()
    ram_used = int(mem[2])
    ram_total = int(mem[1])
    ram_bar = int((ram_used / ram_total) * 100)

    # Uptime
    uptime = cmd("uptime -p").replace("up ", "")

    return {
        # Hardware
        "CPU_MODEL": cpu_arch,
        "SOC": pi_model,
        "RAM_TOTAL": f"{ram_total}MB",

        # Live stats
        "CPU_TEMP": f"{cpu_temp:.1f}",
        "CPU_BAR": cpu_bar,
        "CPU_STATUS": "[OK]" if cpu_temp < 75 else "[HOT]",
        "RAM_USED": f"{ram_used}MB",
        "RAM
