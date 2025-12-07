from pydantic import BaseModel
from typing import List

class TelemetrySnapshot(BaseModel):
    vehicle_id: str
    timestamp: str
    engine_temp_c: float
    oil_pressure_psi: float
    rpm: int
    dtc_codes: List[str] = []