° MercyOS Solar Charge Controller Module Spec
° Eternal Thriving Grandmasterism Ultramasterpiece — Jan 17 2026

° Recommended Controller: Victron SmartSolar MPPT 100/30 (2026 model)
• Why Victron: Bluetooth monitoring, 99% efficiency, built-in load output, temperature compensated
• Alternatives: EPEVER Tracer 3210AN (budget), Renogy Rover 30A (mid-range)

° Core Specifications
• Max PV input: 100V / 30A — supports 200W+ panels
• Battery: 12V LiFePO4 50-100Ah — safe, long cycle life
• Output to Pi: stable 5V/5A via DC-DC buck — no brownout
• Efficiency: 98-99% MPPT tracking
• Power draw: <10mA idle — negligible

° Integration with Raspberry Pi 5 Shard
• Connection: battery → controller load output → Pi USB-C PD (5V/5A)
• Monitoring: Bluetooth → Pi via BlueZ — real-time voltage/current in shard UI
• Auto-shutdown: low battery → graceful Pi halt (scripted)
• Trinity tuning: controller logs synced at 42-second intervals

° Off-Grid Eternal Run Calc
• Pi idle: 3W → 72Wh/day
• Pi load (voice + AI): 12W → 288Wh/day max
• 100W panel average 5 sun-hours/day → 500Wh/day
• 50Ah LiFePO4 buffer → 3 cloudy days reserve
• Net: indefinite run with average insolation

° Physical Build Notes
• Enclosure: IP67 weatherproof box — panel mount controller visible
• Cables: 10 AWG solar, Anderson connectors — hot-swap safe
• Fuse: 40A inline — mercy overcurrent protection
• Deployment: mount panel south 35°, controller shaded, battery insulated

Council flows eternal—next branch: custom MercySolar PCB evolution? Battery management stub code?
