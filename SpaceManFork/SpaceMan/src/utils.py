import random
import json
import requests
import os

from typing import List, Optional
from entity import Packet, LoRaCFG,Device, Position, Network
from typing import List, Tuple

FIXED_TOA = 2.7  # seconds, placeholder



def fetch_tle_from_celestrak(group: str = "active", filename: str = "tle_active.txt") -> List[Tuple[str, str, str]]:
    """
    Downloads TLEs for a given group from CelesTrak, but only if local file doesn't exist.
    Returns a list of tuples: (satellite_name, tle_line1, tle_line2)
    """
    # Check if file exists
    if not os.path.exists(filename):
        print(f"--- > TLE file '{filename}' not found. Downloading from CelesTrak...")
        url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "w") as f:
            f.write(response.text)
    else:
        print(f"--- > TLE file '{filename}' found locally. Using cached copy.")

    # Read TLEs from file
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()

    tle_list = []
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        tle_list.append((name, line1, line2))

    return tle_list

def filter_tles_by_name(tle_list: List[Tuple[str, str, str]], names: List[str]) -> List[Tuple[str, str, str]]:
    """
    Filter a list of TLEs to include only satellites whose names are in `names`.
    Case-insensitive match.
    """
    names_lower = [n.lower() for n in names]
    return [tle for tle in tle_list if tle[0].lower() in names_lower]

def random_transmissions(
    network,
    payloads,
    lora_cfgs,
    t_start=0,
    t_end=1000,
    n_packets=1,
    toa=2.7
):

    for device in network.devices.all_devices():

        # Step 1: generate sorted random times
        times = sorted(
            round(random.uniform(t_start, t_end), 3)
            for _ in range(n_packets)
        )

        valid_times = []

        for t in times:
            if not valid_times:
                valid_times.append(t)
            else:
                # ensure no self-overlap
                if t >= valid_times[-1] + toa:
                    valid_times.append(t)

        # If we lost some packets due to overlap,
        # you can optionally resample until count == n_packets

        for t in valid_times:
            pkt_payload = random.choice(payloads)
            cfg = random.choice(lora_cfgs)
            pkt = Packet(pkt_payload, t)
            device.transmit(pkt, cfg)



def generate_payloads(
    min_len: int = 1,
    max_len: int = 222,
    save_to: Optional[str] = None
) -> List[bytes]:
    """
    Generate payloads from min_len to max_len bytes.
    If save_to is provided, also save payloads as hex strings to JSON.
    """
    payloads = [bytes(range(n)) for n in range(min_len, max_len + 1)]

    if save_to:
        with open(save_to, "w") as f:
            json.dump([p.hex() for p in payloads], f, indent=2)

    return payloads

def load_devices_from_json(network, path):
    with open(path, "r") as f:
        devices_data = json.load(f)

    for dev in devices_data:
        dx = Device(
            dev["devEui"],
            Position(dev["lat"], dev["lon"], alt=dev.get("alt")),
            network=network
        )
        network.devices.add_device(dx)



def check_collisions(network):
    FIXED_TOA = 2.7

    txs = network.transmissions
    n = len(txs)

    collided_indices = set()

    for i in range(n):
        dev_i, pkt_i, cfg_i = txs[i]
        start_i = pkt_i.txTime
        end_i = start_i + FIXED_TOA

        for j in range(i + 1, n):
            dev_j, pkt_j, cfg_j = txs[j]

            # Same SF and same frequency
            if cfg_i.sf != cfg_j.sf:
                continue
            if cfg_i.frequency != cfg_j.frequency:
                continue

            start_j = pkt_j.txTime
            end_j = start_j + FIXED_TOA

            # Proper overlap condition
            if (start_i < end_j) and (end_i > start_j):
                collided_indices.add(i)
                collided_indices.add(j)

    collided = []
    non_colliding = []

    for idx, tx in enumerate(txs):
        if idx in collided_indices:
            collided.append(tx)
        else:
            non_colliding.append(tx)

    return collided, non_colliding
