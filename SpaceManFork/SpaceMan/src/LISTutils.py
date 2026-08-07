# LISTutils.py

import random
import json
import requests
import os
import math

from typing import List, Optional, Tuple

from entity import (
    Packet,
    LoRaCFG,
    Device,
    Position,
    Network
)

########################################
# Real LoRa Time-on-Air Calculator
########################################

def calculate_lora_toa(
    payload_size,
    sf,
    bw,
    cr=1,
    preamble=8,
    crc=1,
    ih=0,
    de=None
):

    bw_hz = bw * 1000

    ########################################
    # Low Data Rate Optimization
    ########################################

    if de is None:
        de = 1 if (sf >= 11 and bw == 125) else 0

    ########################################
    # Symbol duration
    ########################################

    t_sym = (2 ** sf) / bw_hz

    ########################################
    # Preamble duration
    ########################################

    t_preamble = (preamble + 4.25) * t_sym

    ########################################
    # Payload symbols
    ########################################

    payload_symb_nb = 8 + max(
        math.ceil(
            (
                8 * payload_size
                - 4 * sf
                + 28
                + 16 * crc
                - 20 * ih
            )
            /
            (4 * (sf - 2 * de))
        ) * (cr + 4),
        0
    )

    ########################################
    # Payload duration
    ########################################

    t_payload = payload_symb_nb * t_sym

    ########################################
    # Total ToA
    ########################################

    return t_preamble + t_payload


########################################
# TLE Download
########################################

def fetch_tle_from_celestrak(
    group: str = "active",
    filename: str = "tle_active.txt"
) -> List[Tuple[str, str, str]]:

    if not os.path.exists(filename):

        print(
            f"--- > TLE file '{filename}' "
            f"not found. Downloading from CelesTrak..."
        )

        url = (
            "https://celestrak.org/NORAD/elements/"
            f"gp.php?GROUP={group}&FORMAT=tle"
        )

        response = requests.get(url)

        response.raise_for_status()

        with open(filename, "w") as f:

            f.write(response.text)

    else:

        print(
            f"--- > TLE file '{filename}' "
            f"found locally. Using cached copy."
        )

    ########################################
    # Read TLEs
    ########################################

    with open(filename, "r") as f:

        lines = f.read().strip().splitlines()

    tle_list = []

    for i in range(0, len(lines), 3):

        name = lines[i].strip()

        line1 = lines[i + 1].strip()

        line2 = lines[i + 2].strip()

        tle_list.append(
            (name, line1, line2)
        )

    return tle_list


########################################
# Filter Satellites
########################################

def filter_tles_by_name(
    tle_list: List[Tuple[str, str, str]],
    names: List[str]
) -> List[Tuple[str, str, str]]:

    names_lower = [n.lower() for n in names]

    return [
        tle
        for tle in tle_list
        if tle[0].lower() in names_lower
    ]


########################################
# Random Transmissions
########################################

def random_transmissions(
    network,
    payloads,
    lora_cfgs,
    t_start=0,
    t_end=1000,
    n_packets=1,
    seed=None
):

    rng = random.Random(seed)
    
    for device in network.devices.all_devices():

        times = sorted(
            #round(random.uniform(t_start, t_end), 3)
            round(rng.uniform(t_start, t_end), 3)
            for _ in range(n_packets)
        )

        valid_transmissions = []

        for t in times:

            pkt_payload = random.choice(payloads)

            cfg = random.choice(lora_cfgs)

            toa = calculate_lora_toa(
                len(pkt_payload),
                cfg.sf,
                cfg.bw
            )

            if not valid_transmissions:

                valid_transmissions.append(
                    (t, toa, pkt_payload, cfg)
                )

            else:

                last_t, last_toa, _, _ = (
                    valid_transmissions[-1]
                )

                ########################################
                # Avoid self-overlap
                ########################################

                if t >= last_t + last_toa:

                    valid_transmissions.append(
                        (t, toa, pkt_payload, cfg)
                    )

        ########################################
        # Create packets
        ########################################

        for t, toa, pkt_payload, cfg in valid_transmissions:

            pkt = Packet(
                pkt_payload,
                t
            )

            device.transmit(
                pkt,
                cfg
            )


########################################
# Payload Generation
########################################

def generate_payloads(
    min_len: int = 1,
    max_len: int = 222,
    save_to: Optional[str] = None
) -> List[bytes]:

    payloads = [
        bytes(range(n))
        for n in range(min_len, max_len + 1)
    ]

    if save_to:

        with open(save_to, "w") as f:

            json.dump(
                [p.hex() for p in payloads],
                f,
                indent=2
            )

    return payloads


########################################
# Load Devices
########################################

def load_devices_from_json(network, path):

    with open(path, "r") as f:

        devices_data = json.load(f)

    for dev in devices_data:

        dx = Device(
            dev["devEui"],
            Position(
                dev["lat"],
                dev["lon"],
                alt=dev.get("alt")
            ),
            network=network
        )

        network.devices.add_device(dx)


########################################
# Collision Detection
########################################

def check_collisions(network):

    txs = network.transmissions

    n = len(txs)

    collided_indices = set()

    for i in range(n):

        dev_i, pkt_i, cfg_i = txs[i]

        start_i = pkt_i.txTime

        toa_i = calculate_lora_toa(
            len(pkt_i.payload),
            cfg_i.sf,
            cfg_i.bw
        )

        end_i = start_i + toa_i

        for j in range(i + 1, n):

            dev_j, pkt_j, cfg_j = txs[j]

            ########################################
            # Same SF
            ########################################

            if cfg_i.sf != cfg_j.sf:
                continue

            ########################################
            # Same frequency
            ########################################

            if cfg_i.frequency != cfg_j.frequency:
                continue

            start_j = pkt_j.txTime

            toa_j = calculate_lora_toa(
                len(pkt_j.payload),
                cfg_j.sf,
                cfg_j.bw
            )

            end_j = start_j + toa_j

            ########################################
            # Overlap condition
            ########################################

            if (
                (start_i < end_j)
                and
                (end_i > start_j)
            ):

                collided_indices.add(i)

                collided_indices.add(j)

    ########################################
    # Build output lists
    ########################################

    collided = []

    non_colliding = []

    for idx, tx in enumerate(txs):

        if idx in collided_indices:

            collided.append(tx)

        else:

            non_colliding.append(tx)

    return collided, non_colliding
