from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime


# ===================================================================
# 1. FEEDSTOCK DEFINITION
# ===================================================================
@dataclass
class Feedstock:
    """Real solid feedstock definition (biomass, tyre waste, etc.)"""
    id: str
    name: str
    category: str  # "Biomass", "TyreWaste", "Coal", "Plastic", "RDF"

    ultimate_analysis: Dict[str, float]  # C, H, O, N, S, Ash (mass fraction)
    proximate_analysis: Dict[str, float]  # Moisture, VM, FixedCarbon, Ash (mass fraction)

    pseudo_composition: Dict[str, float]  # e.g. {"Cellulose": 0.45, "Lignin": 0.30, ...}

    source: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def validate(self) -> bool:
        total_u = sum(self.ultimate_analysis.values())
        total_p = sum(self.proximate_analysis.values())
        total_pc = sum(self.pseudo_composition.values())

        if abs(total_u - 1.0) > 0.05:
            print(f"Warning: Ultimate sum = {total_u:.3f} (should ≈ 1.0)")
        if abs(total_p - 1.0) > 0.05:
            print(f"Warning: Proximate sum = {total_p:.3f} (should ≈ 1.0)")
        if abs(total_pc - 1.0) > 0.05:
            print(f"Warning: Pseudo-composition sum = {total_pc:.3f} (should ≈ 1.0)")
        return True


# ===================================================================
# 2. KINETIC MECHANISM (Core of the library)
# ===================================================================
@dataclass
class KineticMechanism:
    """One literature-based kinetic mechanism for a pseudo-component"""
    id: str
    author: str
    year: int
    reference: str
    doi: Optional[str] = None

    # Links
    feedstock_id: str
    pseudo_component: str  # "Cellulose", "Hemicellulose", "NaturalRubber", "SBR"...

    # Reaction details
    reaction_type: str  # "Drying", "Devolatilization", "CharGasification", "CharCombustion"
    reaction_scheme: str  # "SingleStep", "TwoStep", "Competing", "DAEM", "ShrinkingCore"

    # Operating conditions (critical for selection)
    agent: str  # "N2", "O2", "Steam", "Air", "CO2", "Autothermal", "Oxyfuel"
    temperature_range: Tuple[float, float]  # (T_min_K, T_max_K)
    particle_size_range: Tuple[float, float]  # (d_min_mm, d_max_mm)
    pressure_range: Tuple[float, float]  # (P_min_bar, P_max_bar)
    heating_rate_range: Tuple[float, float]  # (°C/min)

    # Kinetic parameters (supports multi-step reactions)
    parameters: List[Dict]  # List of dicts: A, E, n, etc.

    notes: Optional[str] = None
    limitations: Optional[str] = None
    confidence: str = "Medium"  # "High", "Medium", "Low"

    def validate(self) -> bool:
        if not self.parameters:
            print(f"Warning: No parameters defined for {self.id}")
            return False
        return True
