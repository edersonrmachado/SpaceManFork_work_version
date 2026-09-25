from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class GPSPosition:
    latitude: float
    longitude: float
    name: Optional[str] = None

    def __str__(self) -> str:
        pos_str = f"{self.latitude:.6f}, {self.longitude:.6f}"
        return f"[{self.name}] {pos_str}" if self.name else pos_str


@dataclass
class LoraConfig:
    """
    LoRa config dataclass
    """
    sf: int
    bw: float
    fc: float
    payload_len: int
    cr: Optional[int] = 1
    crc: Optional[int] = 2
    ih: Optional[bool] = False
    ldro: Optional[int] = 0 # 0=OFF 1=ON 2=AUTO
    preamble_len: Optional[int] = 8
