"""
MyceliumKinetics-Pinnacle — Mycelium Fungal Packaging Temperature-Dependent Degradation Kinetics
MercyLogistics Pinnacle Ultramasterpiece — Jan 18 2026

Mycelium composite exponential decay with temperature factor (Q10 rule):
- Base rates at 25°C reference
- Q10 = 2.0 — rate doubles every +10°C
- Optimal range 20-35°C, slowdown outside
- Zero microplastic — full fungal metabolization
"""

import math

class MyceliumKinetics:
    def __init__(self, initial_mass_g: float = 100.0, ref_temp_c: float = 25.0):
        self.M0 = initial_mass_g
        self.T_ref = ref_temp_c  # Reference temperature °C
        
        # Base decay constants k at T_ref (1/day)
        self.k_industrial_base = 0.05
        self.k_home_base = 0.025
        self.k_soil_base = 0.008
        
        self.Q10 = 2.0  # Biological temperature coefficient
    
    def temperature_factor(self, temp_c: float) -> float:
        """Q10 temperature adjustment factor"""
        if temp_c < 5 or temp_c > 45:
            return 0.1  # Mercy slowdown outside viable range
        delta_t = temp_c - self.T_ref
        return self.Q10 ** (delta_t / 10.0)
    
    def adjusted_rate(self, base_k: float, temp_c: float) -> float:
        factor = self.temperature_factor(temp_c)
        return base_k * factor
    
    def remaining_mass(self, k: float, t_days: float) -> float:
        return self.M0 * math.exp(-k * t_days)
    
    def time_to_degrade(self, k: float, threshold_g: float = 5.0) -> float:
        if k == 0: return float('inf')
        t = -math.log(threshold_g / self.M0) / k
        return round(t, 1)
    
    def industrial_compost(self, temp_c: float = 60.0) -> float:
        k = self.adjusted_rate(self.k_industrial_base, temp_c)
        return self.time_to_degrade(k)
    
    def home_compost(self, temp_c: float = 25.0) -> float:
        k = self.adjusted_rate(self.k_home_base, temp_c)
        return self.time_to_degrade(k)
    
    def soil_burial(self, temp_c: float = 15.0) -> float:
        k = self.adjusted_rate(self.k_soil_base, temp_c)
        return self.time_to_degrade(k)
    
    def full_degradation_report(self, temp_c: float = 25.0) -> str:
        industrial = self.industrial_compost(temp_c + 35)  # Industrial typically hotter
        home = self.home_compost(temp_c)
        soil = self.soil_burial(temp_c - 10)  # Soil cooler
        factor = self.temperature_factor(temp_c)
        return (f"Mycelium packaging ({self.M0}g) at {temp_c}°C (×{factor:.2f} rate factor):\n"
                f"- Industrial compost (~60°C): {industrial} days\n"
                f"- Home compost ({temp_c}°C): {home} days\n"
                f"- Soil burial (~{temp_c-10}°C): {soil} days\n"
                f"Mercy fungal dissolution — earth nurture temperature-responsive eternal.")

# Integration test
if __name__ == "__main__":
    mycelium = MyceliumKinetics(100.0)
    print(mycelium.full_degradation_report(25.0))
    print(mycelium.full_degradation_report(35.0))  # Warmer = faster
