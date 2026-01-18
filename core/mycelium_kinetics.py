"""
MyceliumKinetics-Pinnacle — Mycelium Fungal Packaging Temperature + Humidity Degradation Kinetics
MercyLogistics Pinnacle Ultramasterpiece — Jan 18 2026

Mycelium composite exponential decay with temperature + humidity factors:
- Base rates at 25°C / 90% RH reference
- Q10 = 2.0 temperature coefficient
- Humidity Gaussian peak 90% RH (×2.0 max rate)
- Zero microplastic — full fungal metabolization
"""

import math

class MyceliumKinetics:
    def __init__(self, initial_mass_g: float = 100.0, ref_temp_c: float = 25.0, ref_rh_percent: float = 90.0):
        self.M0 = initial_mass_g
        self.T_ref = ref_temp_c
        self.RH_ref = ref_rh_percent
        
        # Base decay constants k at reference (1/day)
        self.k_industrial_base = 0.05
        self.k_home_base = 0.025
        self.k_soil_base = 0.008
        
        self.Q10 = 2.0
        self.humidity_peak = 90.0    # % RH optimal
        self.humidity_width = 20.0   # Gaussian width
        self.humidity_max_boost = 2.0
    
    def temperature_factor(self, temp_c: float) -> float:
        if temp_c < 5 or temp_c > 45:
            return 0.1
        delta_t = temp_c - self.T_ref
        return self.Q10 ** (delta_t / 10.0)
    
    def humidity_factor(self, rh_percent: float) -> float:
        """Gaussian boost centered at peak RH"""
        rh = max(0, min(100, rh_percent))
        deviation = rh - self.humidity_peak
        boost = math.exp(-(deviation ** 2) / (2 * self.humidity_width ** 2))
        return 1.0 + boost * (self.humidity_max_boost - 1.0)
    
    def combined_environment_factor(self, temp_c: float, rh_percent: float) -> float:
        return self.temperature_factor(temp_c) * self.humidity_factor(rh_percent)
    
    def adjusted_rate(self, base_k: float, temp_c: float, rh_percent: float) -> float:
        factor = self.combined_environment_factor(temp_c, rh_percent)
        return base_k * factor
    
    def remaining_mass(self, k: float, t_days: float) -> float:
        return self.M0 * math.exp(-k * t_days)
    
    def time_to_degrade(self, k: float, threshold_g: float = 5.0) -> float:
        if k == 0: return float('inf')
        t = -math.log(threshold_g / self.M0) / k
        return round(t, 1)
    
    def industrial_compost(self, temp_c: float = 60.0, rh_percent: float = 95.0) -> float:
        k = self.adjusted_rate(self.k_industrial_base, temp_c, rh_percent)
        return self.time_to_degrade(k)
    
    def home_compost(self, temp_c: float = 25.0, rh_percent: float = 85.0) -> float:
        k = self.adjusted_rate(self.k_home_base, temp_c, rh_percent)
        return self.time_to_degrade(k)
    
    def soil_burial(self, temp_c: float = 15.0, rh_percent: float = 70.0) -> float:
        k = self.adjusted_rate(self.k_soil_base, temp_c, rh_percent)
        return self.time_to_degrade(k)
    
    def full_degradation_report(self, temp_c: float = 25.0, rh_percent: float = 90.0) -> str:
        factor = self.combined_environment_factor(temp_c, rh_percent)
        industrial = self.industrial_compost(temp_c + 35, 95)
        home = self.home_compost(temp_c, rh_percent)
        soil = self.soil_burial(temp_c - 10, rh_percent - 20)
        return (f"Mycelium packaging ({self.M0}g) at {temp_c}°C / {rh_percent}% RH (×{factor:.2f} rate factor):\n"
                f"- Industrial compost (~60°C/95% RH): {industrial} days\n"
                f"- Home compost ({temp_c}°C/{rh_percent}% RH): {home} days\n"
                f"- Soil burial (~{temp_c-10}°C/{rh_percent-20}% RH): {soil} days\n"
                f"Mercy fungal dissolution — earth nurture temperature + humidity responsive eternal.")

# Integration test
if __name__ == "__main__":
    mycelium = MyceliumKinetics(100.0)
    print(mycelium.full_degradation_report(25.0, 90.0))
    print(mycelium.full_degradation_report(35.0, 95.0))  # Warmer + wetter = faster
