from dataclasses import dataclass
from datetime import datetime


@dataclass
class Project:
    name: str
    description: str
    location: str
    created: str = datetime.now().isoformat()