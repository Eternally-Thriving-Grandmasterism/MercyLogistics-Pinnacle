"""
MyceliumKinetics-Pinnacle — Mycelium Fungal Packaging Temperature + Humidity + pH + Light + Oxygen + Pressure + Microbial Activity Degradation Kinetics
MercyLogistics Pinnacle Ultramasterpiece — Jan 18 2026

Mycelium composite exponential decay with full environmental + microbial factors:
- Base rates at 25°C / 90% RH / pH 7.0 / 100 lux / 21% O₂ / 101 kPa reference
- Q10 = 2.0 temperature coefficient
- Humidity Gaussian peak 90% RH (×2.0 max)
- pH Gaussian peak 7.0 (×1.0 max)
- Light Gaussian peak low light (×1.2 max), UV inhibition
- Oxygen Gaussian peak 21% O₂ (×1.5 max aerobic)
- Pressure Gaussian peak 101 kPa (×1.0)
- Microbial activity Gaussian synergy (temperature 20-30°C + humidity 70-90% → ×1.8 max)
- Zero microplastic — full fungal + microbial metabolization
"""

import math

class MyceliumKinetics:
    def __init__(self, initial_mass_g: float = 100.0,
                 ref_temp_c: float = 25.0,
                 ref_rh_percent: float = 90.0,
                 ref_ph: float = 7.0,
                 ref_lux: float = 100.0,
                 ref_o2_percent: float = 21.0,
                 ref_pressure_kpa: float = 101.3):
        self.M0 = initial_mass_g
        self.T_ref = ref_temp_c
        self.RH_ref = ref_rh_percent
        self.pH_ref = ref_ph
        self.lux_ref = ref_lux
        self.o2_ref = ref_o2_percent
        self.pressure_ref = ref_pressure_kpa
        
        # Base decay constants k at reference (1/day)
        self.k_industrial_base = 0.05
        self.k_home_base = 0.025
        self.k_soil_base = 0.008
        
        self.Q10 = 2.0
        self.humidity_peak = 90.0
        self.humidity_width = 20.0
        self.humidity_max_boost = 2.0
        self.ph_peak = 7.0
        self.ph_width = 2.0
        self.ph_max_boost = 1.0
        self.light_peak = 100.0
        self.light_width = 200.0
        self.light_max_boost = 1.2
        self.uv_inhibition_threshold = 5000
        self.oxygen_peak = 21.0
        self.oxygen_width = 10.0
        self.oxygen_max_boost = 1.5
        self.pressure_peak = 101.3
        self.pressure_width = 20.0
        self.pressure_max_boost = 1.0
        
        # Microbial activity synergy (temperature + humidity optimal)
        self.microbial_temp_peak = 25.0
        self.microbial_temp_width = 10.0
        self.microbial_rh_peak = 80.0
        self.microbial_rh_width = 20.0
        self.microbial_max_boost = 1.8
    
    def temperature_factor(self, temp_c: float) -> float:
        if temp_c < 5 or temp_c > 45:
            return 0.1
        delta_t = temp_c - self.T_ref
        return self.Q10 ** (delta_t / 10.0)
    
    def humidity_factor(self, rh_percent: float) -> float:
        rh = max(0, min(100, rh_percent))
        deviation = rh - self.humidity_peak
        boost = math.exp(-(deviation ** 2) / (2 * self.humidity_width ** 2))
        return 1.0 + boost * (self.humidity_max_boost - 1.0)
    
    def ph_factor(self, ph: float) -> float:
        ph = max(0, min(14, ph))
        deviation = ph - self.ph_peak
        boost = math.exp(-(deviation ** 2) / (2 * self.ph_width ** 2))
        return 1.0 + boost * (self.ph_max_boost - 1.0)
    
    def light_factor(self, lux: float) -> float:
        if lux > self.uv_inhibition_threshold:
            return 0.3
        deviation = lux - self.light_peak
        boost = math.exp(-(deviation ** 2) / (2 * self.light_width ** 2))
        return 1.0 + boost * (self.light_max_boost - 1.0)
    
    def oxygen_factor(self, o2_percent: float) -> float:
        o2 = max(0, min(100, o2_percent))
        deviation = o2 - self.oxygen_peak
        boost = math.exp(-(deviation ** 2) / (2 * self.oxygen_width ** 2))
        return 1.0 + boost * (self.oxygen_max_boost - 1.0)
    
    def pressure_factor(self, pressure_kpa: float) -> float:
        pressure = max(50, min(150, pressure_kpa))
        deviation = pressure - self.pressure_peak
        boost = math.exp(-(deviation ** 2) / (2 * self.pressure_width ** 2))
        return 0.5 + boost * 0.5
    
    def microbial_activity_factor(self, temp_c: float, rh_percent: float) -> float:
        """Microbial synergy — optimal temperature + humidity"""
        temp_dev = temp_c - self.microbial_temp_peak
        rh_dev = rh_percent - self.microbial_rh_peak
        temp_boost = math.exp(-(temp_dev ** 2) / (2 * self.microbial_temp_width ** 2))
        rh_boost = math.exp(-(rh_dev ** 2) / (2 * self.microbial_rh_width ** 2))
        return 1.0 + (temp_boost * rh_boost) * (self.microbial_max_boost - 1.0)
    
    def combined_environment_factor(self, temp_c: float, rh_percent: float, ph: float, lux: float, o2_percent: float, pressure_kpa: float) -> float:
        microbial = self.microbial_activity_factor(temp_c, rh_percent)
        return (self.temperature_factor(temp_c) *
                self.humidity_factor(rh_percent) *
                self.ph_factor(ph) *
                self.light_factor(lux) *
                self.oxygen_factor(o2_percent) *
                self.pressure_factor(pressure_kpa) *
                microbial)
    
    def adjusted_rate(self, base_k: float, temp_c: float, rh_percent: float, ph: float, lux: float, o2_percent: float, pressure_kpa: float) -> float:
        factor = self.combined_environment_factor(temp_c, rh_percent, ph, lux, o2_percent, pressure_kpa)
        return base_k * factor
    
    def remaining_mass(self, k: float, t_days: float) -> float:
        return self.M0 * math.exp(-k * t_days)
    
    def time_to_degrade(self, k: float, threshold_g: float = 5.0) -> float:
        if k == 0: return float('inf')
        t = -math.log(threshold_g / self.M0) / k
        return round(t, 1)
    
    def industrial_compost(self, temp_c: float = 60.0, rh_percent: float = 95.0, ph: float = 7.0, lux: float = 50.0, o2_percent: float = 21.
