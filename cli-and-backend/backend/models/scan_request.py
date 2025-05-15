from pydantic import BaseModel
from typing import List, Optional

class ScanRequest(BaseModel):
    domain: str
    sources: List[str]
    use_virustotal: Optional[bool] = False
    use_abuseipdb: Optional[bool] = False
    output_format: Optional[str] = "json"
