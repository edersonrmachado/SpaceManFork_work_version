# entity.py

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timezone

from skyfield.api import EarthSatellite, wgs84


########################################
# Data Classes
########################################

@dataclass
class LoRaCFG:
    sf: int
    bw: int
    frequency: float


@dataclass
class Position:
    lat: float
    lon: float
    alt: Optional[float] = None


@dataclass
class Packet:
    payload: bytes
    txTime: float


########################################
# Device
########################################

class Device:

    def __init__(self, devEui: str, position: Position, network=None):

        self.devEui = devEui
        self.position = position

        self.buffer: List[Tuple[Packet, LoRaCFG]] = []

        self.network = network

    def transmit(self, packet: Packet, cfg: LoRaCFG):

        self.buffer.append((packet, cfg))

        if self.network:

            self.network.route_packet_to_gateway(
                self,
                packet,
                cfg
            )


########################################
# Device Manager
########################################

class DeviceManager:

    def __init__(self):

        self._devices: Dict[str, Device] = {}

    def add_device(self, device: Device):

        self._devices[device.devEui] = device

    def get_device(self, devEui: str):

        return self._devices.get(devEui)

    def all_devices(self):

        return list(self._devices.values())

    def show_all_devices(self):

        for dev in self._devices.values():

            print(f"{dev.devEui}: {dev.position}")


########################################
# Gateway
########################################

class Gateway:

    def __init__(
        self,
        gatewayId: str,
        satellite: Optional["Satellite"] = None
    ):

        self.gatewayId = gatewayId

        self.satellite: Optional[Satellite] = satellite

        self.buffer: List[
            Tuple[Device, Packet, LoRaCFG]
        ] = []

        if satellite:

            satellite.assign_gateway(self)

    @property
    def position(self):

        if self.satellite:

            return self.satellite.position

        return None

    def receive(
        self,
        device,
        packet: Packet,
        cfg: LoRaCFG
    ):

        self.buffer.append(
            (device, packet, cfg)
        )


########################################
# Satellite
########################################

class Satellite:

    def __init__(
        self,
        satId: str,
        tle_line1: str,
        tle_line2: str
    ):

        self.id = satId

        self.tle_line1 = tle_line1
        self.tle_line2 = tle_line2

        self._satellite_obj: EarthSatellite = EarthSatellite(
            tle_line1,
            tle_line2,
            satId
        )

        self.position: Optional[Position] = None

        self.gateway: Optional[Gateway] = None

    def assign_gateway(self, gateway: "Gateway"):

        self.gateway = gateway

        gateway.satellite = self

    def update_position(
        self,
        ts,
        simulation_time=None
    ):

        if simulation_time is None:

            t = ts.now()

        elif isinstance(simulation_time, (int, float)):

            dt = datetime.fromtimestamp(
                simulation_time,
                tz=timezone.utc
            )

            t = ts.from_datetime(dt)

        else:

            t = ts.from_datetime(simulation_time)

        geocentric = self._satellite_obj.at(t)

        subpoint = geocentric.subpoint()

        self.position = Position(
            lat=float(subpoint.latitude.degrees),
            lon=float(subpoint.longitude.degrees),
            alt=float(subpoint.elevation.m)
        )

    def elevation_from_device(
        self,
        device_position,
        ts,
        unix_time
    ):

        dt = datetime.fromtimestamp(
            unix_time,
            tz=timezone.utc
        )

        t = ts.from_datetime(dt)

        ground_station = wgs84.latlon(
            device_position.lat,
            device_position.lon,
            elevation_m=device_position.alt or 0
        )

        difference = self._satellite_obj - ground_station

        topocentric = difference.at(t)

        alt, az, distance = topocentric.altaz()

        return alt.degrees

    def visible_during_transmission(
        self,
        device_position,
        ts,
        tx_start,
        tx_end,
        min_elevation=30
    ):

        elev_start = self.elevation_from_device(
            device_position,
            ts,
            tx_start
        )

        elev_end = self.elevation_from_device(
            device_position,
            ts,
            tx_end
        )

        return (
            elev_start >= min_elevation
            and
            elev_end >= min_elevation
        )


########################################
# Network
########################################

class Network:

    def __init__(self):

        self.devices = DeviceManager()

        self.gateways: Dict[str, Gateway] = {}

        self.satellites: Dict[str, Satellite] = {}

        self.servers: List = []

        self.transmissions: List[
            Tuple[Device, Packet, LoRaCFG]
        ] = []

    def add_gateway(self, gateway: Gateway):

        self.gateways[gateway.gatewayId] = gateway

    def add_satellite(self, satellite: Satellite):

        self.satellites[satellite.id] = satellite

    def log_transmission(
        self,
        device: Device,
        packet: Packet,
        cfg: LoRaCFG
    ):

        self.transmissions.append(
            (device, packet, cfg)
        )

    def route_packet_to_gateway(
        self,
        device: Device,
        packet: Packet,
        cfg: LoRaCFG
    ):

        self.log_transmission(
            device,
            packet,
            cfg
        )

    def all_entities(self):

        return (
            self.devices.all_devices()
            + list(self.gateways.values())
            + list(self.servers)
        )

    def show_transmissions(self):

        for dev, pkt, cfg in self.transmissions:

            print(
                f"{dev.devEui} -> "
                f"{len(pkt.payload)} bytes "
                f"at {pkt.txTime} "
                f"(SF={cfg.sf}, "
                f"BW={cfg.bw}, "
                f"Freq={cfg.frequency})"
            )
