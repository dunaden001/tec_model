"""Module definitions for the CP35 range of devices from CUI Devices."""

# System imports
from __future__ import annotations

import logging

# Library imports
# Local imports
from tec_model.thermoelectric_cooler import ThermoElectricCooler

# Typing imports

logger = logging.getLogger(__name__)

CP35_DATASHEET_LINK = "https://www.cuidevices.com/product/resource/cp35.pdf"

CP353047 = ThermoElectricCooler(
    mfn="CP353047",
    datasheet_link=CP35_DATASHEET_LINK,
    v_max=11.8,
    i_max=3.5,
    q_max_27=24.0,
    q_max_50=26.0,
    delta_t_max_27=70.0,
    delta_t_max_50=77.0,
)
