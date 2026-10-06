import argparse

# bool type
def str_to_bool(value):
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(
        "Expected true/false"
    )


ARGUMENTS = {
    # Endpoint / IoT node
    "central_point_lat": (
        "endpoint.geometry.central_point.lat",
        float,
        "Latitude [deg] ref. for ED area"
    ),
    "central_point_lon": (
        "endpoint.geometry.central_point.lon",
        float,
        "Longitude [deg] ref. for ED area"
    ),
    "circle_radius": (
        "endpoint.geometry.circle_radius_km",
        float,
        "ED region radius [km]"
    ),
    "num_eds": (
        "endpoint.number_of_eds",
        int,
        "Number of end devices"
    ),
    "pkt_per_ed": (
        "endpoint.pkt_per_endpoint",
        int,
        "Packets per endpoint"
    ),

    # LoRa
    "sf": (
        "lora.sf",
        int,
        "Spreading factor [7-12]"
    ),
    "bw": (
        "lora.bw",
        float,
        "Bandwidth [kHz]"
    ),
    "freq": (
        "lora.frequency",
        float,
        "Carrier frequency [MHz]"
    ),
    "payload_len": (
        "lora.payload_len",
        int,
        "PHY payload length [bytes]"
    ),
    "cr": (
        "lora.cr",
        int,
        "Coding rate [1-4] for 4/5-4/8"
    ),
    "crc": (
        "lora.crc",
        int,
        "CRC: 1 = enabled, 0 = disabled"
    ),
    "ih": (
        "lora.ih",
        str_to_bool,
        "Implicit header: true = implicit, false = explicit"
    ),
    "ldro": (
        "lora.ldro",
        int,
        "Low data rate optimization: 1 = enabled, 0 = disabled"
    ),
    "preamble_len": (
        "lora.preamble_len",
        int,
        "Preamble length [symbols]"
    ),

    # Satellite
    "num_sats": (
        "satellite.num_sats",
        int,
        "Number of satellites"
    ),
    "min_elev": (
        "satellite.min_elevation_angle",
        float,
        "Minimum elevation angle [deg]"
    ),

    # IoT node / transmitter
    "pt_dbm": (
        "link_margin.iot_node.pt_dbm",
        float,
        "ED transmission power [dBm]"
    ),
    "lftx": (
        "link_margin.iot_node.lftx",
        float,
        "Transmitter feeder loss [dB]"
    ),
    "gt": (
        "link_margin.iot_node.gt",
        float,
        "Transmitter antenna gain [dBi]"
    ),

    # Propagation losses
    "la": (
        "link_margin.propagation_losses.la",
        float,
        "Atmospheric attenuation loss [dB]"
    ),
    "li": (
        "link_margin.propagation_losses.li",
        float,
        "Ionospheric attenuation loss [dB]"
    ),
    "ld": (
        "link_margin.propagation_losses.ld",
        float,
        "Depointing loss [dB]"
    ),
    "lp": (
        "link_margin.propagation_losses.lp",
        float,
        "Polarization mismatch loss [dB]"
    ),

    # Satellite receiver
    "gr": (
        "link_margin.satellite_receiver.gr",
        float,
        "Satellite receiver antenna gain [dBi]"
    ),
    "lfrx": (
        "link_margin.satellite_receiver.lfrx",
        float,
        "Receiver feeder loss [dB]"
    ),
    "nf": (
        "link_margin.satellite_receiver.nf",
        float,
        "Receiver noise figure [dB]"
    ),
    "temp_0": (
        "link_margin.satellite_receiver.temp_0",
        float,
        "Reference temperature [K]"
    ),
    "gf": (
        "link_margin.satellite_receiver.gf",
        float,
        "Receiver line gain [dB]"
    ),
    "ta": (
        "link_margin.satellite_receiver.ta",
        float,
        "Antenna noise temperature [K]"
    ),

    # Doppler
    "doppler_points": (
        "doppler.derivative_num_of_points",
        int,
        "Number of points for Doppler derivative"
    ),
    "doppler_step": (
        "doppler.derivative_step_sec",
        float,
        "Doppler derivative step [s]"
    ),
}


def parse_arguments():

    parser = argparse.ArgumentParser()

    for name, (config_path, argument_type, help_text) in ARGUMENTS.items():

        parser.add_argument(
            f"--{name}",
            type=argument_type,
            default=None,
            metavar="",
            help=help_text
        )

    return parser.parse_args()



def set_nested_attribute(obj, path, value):

    parts = path.split(".")

    for part in parts[:-1]:
        obj = getattr(obj, part)

    setattr(obj, parts[-1], value)


def apply_overrides(config, args):

    for arg_name, (config_path, _,_) in ARGUMENTS.items():

        value = getattr(args, arg_name)

        if value is not None:
            set_nested_attribute(
                config,
                config_path,
                value
            )


