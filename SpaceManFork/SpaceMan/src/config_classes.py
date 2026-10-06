from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationConfig:
    print_simulation_debug: bool = False
    generate_payload_file: bool = False
    devices_filename: str = "config/endpoint_positions/devices.json"
    payload_generated_filename: str = "../data/random_payloads.json"
    
    simulation_start_year: int = 2026
    simulation_start_month: int = 10
    simulation_start_day: int = 8
    simulation_start_hour: int = 0
    simulation_start_minute: int = 0
    simulation_start_second: int = 0

    simulation_end_year: int = 2026
    simulation_end_month: int = 10
    simulation_end_day: int = 10
    simulation_end_hour: int = 0
    simulation_end_minute: int = 0
    simulation_end_second: int = 0

    results_file: str = "../data/results_example.csv"

@dataclass
class SatelliteConfig:
    num_sats: int = 5
    min_elevation_angle: float = 5.0
    tle_filename: str = "tle_active.txt"

@dataclass
class CentralPointConfig:
    lat: float = 48.8566 # paris
    lon: float = 2.3522
    
@dataclass
class EDGeometryConfig:
    central_point: CentralPointConfig
    circle_radius_km: float = 100.0
    distribution_seed: Optional[int] = None

@dataclass
class EndpointConfig:
    geometry: EDGeometryConfig
    number_of_eds: int = 20
    pkt_per_endpoint: int = 10
    policy_tx: str = "random_secure"

@dataclass
class LoRaConfig:
    sf: int = 7
    bw: float = 125.0
    frequency: float = 433.75
    payload_len: int = 59
    cr: Optional[int] = 1 # default 4/5
    crc: Optional[int] = 1 # 0 deactivated 1 activated (2 bytes)
    ih: Optional[bool] = False # False implicit True explicit
    ldro: Optional[int] = 0 # 0=OFF 1=ON 2=AUTO (activated Ts>16.38ms)
    preamble_len: Optional[int] = 8
    
@dataclass
class IoTNodeConfig:
    pt_dbm: float = 21.0
    lftx: float = 1.0
    gt: float = 0.0

@dataclass
class PropagationLossesConfig:
    la: float = -0.11
    li: float = -0.16
    ld: float = -3.0
    lp: float = -3.0

@dataclass
class SatelliteReceiverConfig:
    gr: float = 0.0
    lfrx: float = 1.0
    nf: float = 6.5
    temp_0: float = 290.0
    gf: float = -1.0
    ta: float = 290.0


@dataclass
class LinkMarginConfig:
    iot_node: IoTNodeConfig
    propagation_losses: PropagationLossesConfig
    satellite_receiver: SatelliteReceiverConfig

@dataclass
class DopplerConfig:
    derivative_num_of_points: int = 3
    derivative_step_sec: float = 10e-6

@dataclass
class Config:
    simulation: SimulationConfig
    satellite: SatelliteConfig
    endpoint: EndpointConfig
    lora: LoRaConfig
    link_margin: LinkMarginConfig
    doppler: DopplerConfig