"""Script to determine operating points of target TEC module.."""

# System imports
from __future__ import annotations

import logging

# Library imports
import numpy as np

# Local imports
from tec_model.cui_devices_cp35 import CP353047, CP354047

# Typing imports

logger = logging.getLogger(__name__)


hot_side_sink_rj = 0.5  # °C/W

t_cold = 5 + 273.15  # K

currents = np.linspace(1, 5.0, 20).tolist()

t_hots = np.linspace(27 + 273.15, 55 + 273.15, 6).tolist()


CP353047.plot_operating_regions(
    t_cold=t_cold,
    t_hots=t_hots,
    currents=currents,
    hot_side_sink_rj=hot_side_sink_rj,
)


CP354047.plot_operating_regions(
    t_cold=t_cold,
    t_hots=t_hots,
    currents=currents,
    hot_side_sink_rj=hot_side_sink_rj,
)
