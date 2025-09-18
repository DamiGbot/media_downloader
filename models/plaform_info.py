"""Platform information model."""

import re
from dataclasses import dataclass
from typing import List

@dataclass
class PlatformInfo:
    """Information about a supported platform."""
    name: str
    hosts: List[str]
    patterns: List[str]

    def matches_domain(self, domain: str) -> bool:
        return domain.lower() in [host.lower() for host in self.hosts]

    def matches_pattern(self, url: str) -> bool:
        return any(re.search(pattern, url, re.IGNORECASE) for pattern in self.patterns)