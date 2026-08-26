#! /usr/bin/env python3
import json
import subprocess
import sys

is_mic = len(sys.argv) > 1 and sys.argv[1] == "mic"

def get_volume():
    target = "@DEFAULT_AUDIO_SOURCE@" if is_mic else "@DEFAULT_AUDIO_SINK@"
    try:
        out = subprocess.check_output(["wpctl", "get-volume", target]).decode().strip()
    except:
        return 0, False
    parts = out.split()
    if len(parts) < 2:
        return 0, False
    vol = int(float(parts[1]) * 100)
    muted = "[MUTED]" in out
    return vol, muted

def make_bar(vol):
    length = 15
    filled = int(vol / 100.0 * length)
    filled = min(filled, length)
    return "█" * filled + "░" * (length - filled)

def print_status():
    vol, muted = get_volume()
    if is_mic:
        icon = "󰍭" if muted else "󰍬"
        text = f"{icon}"
        tooltip = f"Mic Volume: {vol}%\n<tt>[{make_bar(vol)}]</tt>"
    else:
        if muted:
            icon = "󰸈"
        elif vol < 30:
            icon = ""
        elif vol < 70:
            icon = ""
        else:
            icon = " "
        text = f"{icon}"
        tooltip = f"Speaker Volume: {vol}%\n<tt>[{make_bar(vol)}]</tt>"
    
    out_json = {"text": text, "tooltip": tooltip}
    if muted:
        out_json["class"] = "muted"
    else:
        out_json["class"] = "unmuted"
    
    print(json.dumps(out_json), flush=True)

# Print initial status
print_status()

# Listen to changes using pactl subscribe
try:
    proc = subprocess.Popen(["pactl", "subscribe"], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        if "Event 'change' on sink" in line and not is_mic or "Event 'change' on source" in line and is_mic or "Event 'change' on server" in line:
            print_status()
except KeyboardInterrupt:
    pass
