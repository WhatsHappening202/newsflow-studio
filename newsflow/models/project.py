from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Project:
    name: str
    description: str
    location: str
    created: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )