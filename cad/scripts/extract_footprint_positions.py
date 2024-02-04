"""
Simple script to read a *.kicad_pcb file and extract the positions of interesting foot prints
for CAD automation for the case and plate
"""

def extract_footprint_positions(lines):
    active = False
    switches = []
    mounts = []
    audio_jacks = []
    usb = []
    for line in lines:
        line = line.strip(" ()\n")
        if line.startswith("footprint"):
            if "Cherry" in line:
                active = "switch"
            elif "MountingHole" in line:
                active = "mount"
            elif "TRRS" in line or "PJ-342B" in line:
                active = "audio"
            elif "USB_C_Receptacle" in line:
                active = "usb"

        if line.startswith("at") and active:
            parts = line.split(" ")
            x = float(parts[1])
            y = float(parts[2])
            if active == "switch":
                switches.append((x,y))
            elif active == "mount":
                mounts.append((x,y))
            elif active == "audio":
                audio_jacks.append((x,y))
            elif active == "usb":
                usb.append((x,y))
            active = False
    
    return (switches, mounts, audio_jacks, usb)


def footprints_to_scad(switches, mounts, audio_jacks, usb):
    yield("function kb_footprint_centers() = [")
    for x,y in switches:
        yield(f"    [{x},{y}],")
    yield("];")
    yield("")
    yield("function kb_mount_centers() = [")
    for x,y in mounts:
        yield(f"    [{x},{y}],")
    yield("];")
    yield("")
    yield("function audio_jack_x() = [")
    for x,y in audio_jacks:
        yield(f"    {x},")
    yield("];")
    yield("")
    yield("function usb_c_x() = [")
    for x,y in usb:
        yield(f"    {x},")
    yield("];")


if __name__ == "__main__":
    import fileinput
    for output_line in footprints_to_scad(*extract_footprint_positions(fileinput.input())):
        print(output_line)
