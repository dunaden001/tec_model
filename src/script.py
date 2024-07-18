"""Script to determine operating points of target TEC module.."""

# System imports
from __future__ import annotations

import logging
from typing import cast

import matplotlib.pyplot as plt
import numpy as np

# Library imports
from matplotlib.axes import Axes

# Local imports
from tec_model.cui_devices_cp35 import CP353047

# Typing imports

logger = logging.getLogger(__name__)


hot_side_sink_rj = 0.5  # °C/W

t_cold = 5 + 273.15  # K

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)  # type: ignore[misc]
ax1 = cast(Axes, ax1)
ax2 = cast(Axes, ax2)
ax3 = cast(Axes, ax3)
ax4 = cast(Axes, ax4)

fig.suptitle(f"CP353047 operating points.\nTc = {t_cold - 273.15}°C.")
ax1.set_xlabel("Current (A)")
ax2.set_xlabel("Current (A)")
ax3.set_xlabel("Current (A)")
ax4.set_xlabel("Current (A)")

ax1.set_ylabel("Voltage (V)")
ax2.set_ylabel("Cooling Power (W)")
ax3.set_ylabel("COP")
ax4.set_ylabel("Ambient Temperature (°C)")

currents = np.linspace(1, 5.0, 20)

t_hots = np.linspace(27 + 273.15, 55 + 273.15, 6)
colors = [f"C{i}" for i in range(len(t_hots))]

line_vs = []
line_qs = []
line_cops = []

for t_hot, color in zip(t_hots, colors, strict=True):
    voltages: list[float] = []
    cooling_powers: list[float] = []
    cops: list[float] = []
    t_ambients: list[float] = []

    for current in currents:
        voltage, cooling_power, cop = CP353047.operating_params(
            current=current, t_hot=t_hot, t_cold=t_cold
        )
        input_power = voltage * current
        t_ambient = t_hot - (input_power + cooling_power) * hot_side_sink_rj
        t_ambient_c = t_ambient - 273.15

        voltages.append(voltage)
        cooling_powers.append(cooling_power)
        cops.append(cop)
        t_ambients.append(t_ambient_c)

    t_hot_c = t_hot - 273.15
    label = f"Th = {t_hot_c:.2f}°C"
    line_v = ax1.plot(currents, voltages, f"{color}o-", label=label)
    line_q = ax2.plot(currents, cooling_powers, f"{color}o-", label=label)
    line_cop = ax3.plot(currents, cops, f"{color}o-", label=label)
    line_t_ambient = ax4.plot(currents, t_ambients, f"{color}o-", label=label)

    line_vs += line_v
    line_qs += line_q
    line_cops += line_cop

ax1.legend(handles=line_vs)
ax2.legend(handles=line_qs)
ax3.legend(handles=line_cops)
ax4.legend(handles=line_cops)

plt.show()
