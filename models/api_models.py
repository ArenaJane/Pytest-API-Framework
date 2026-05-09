from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class RequestSpec:
    method: str
    url: str
    json: Optional[Dict[str, Any]] = None

@dataclass
class ExpectedSpec:
    status_code: int
    contains: Optional[Dict[str, Any]] = None

@dataclass
class YamlTestCase:
    name: str
    request: RequestSpec
    expected: ExpectedSpec