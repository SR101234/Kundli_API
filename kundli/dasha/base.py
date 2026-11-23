"""Abstract base class for Dasha calculation engines."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List


class BaseDasha(ABC):
    @abstractmethod
    def calculate_dasha_timeline(
        self,
        birth_datetime: datetime,
        moon_longitude: float,
        target_datetime: datetime = None
    ) -> Dict[str, Any]:
        """Generate the dasha timeline and running period."""
        pass
