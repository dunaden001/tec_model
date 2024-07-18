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

CP35147 = ThermoElectricCooler(
    mfn="CP35147",
    datasheet_link=CP35_DATASHEET_LINK,
    v_max=2.1,
    i_max=3.5,
    q_max_27=3.9,
    q_max_50=4.3,
    delta_t_max_27=68,
    delta_t_max_50=75,
)

CP35247 = ThermoElectricCooler(
    mfn="CP35247",
    datasheet_link=CP35_DATASHEET_LINK,
    v_max=3.8,
    i_max=3.5,
    q_max_27=7.0,
    q_max_50=7.7,
    delta_t_max_27=68,
    delta_t_max_50=75,
)

CP35301547 = ThermoElectricCooler(
    mfn="CP35301547",
    datasheet_link=CP35_DATASHEET_LINK,
    v_max=4.2,
    i_max=3.5,
    q_max_27=7.9,
    q_max_50=8.7,
    delta_t_max_27=68,
    delta_t_max_50=75,
)

CP35347 = ThermoElectricCooler(
    mfn="CP35347",
    datasheet_link=CP35_DATASHEET_LINK,
    v_max=8.6,
    i_max=3.5,
    q_max_27=16,
    q_max_50=17.8,
    delta_t_max_27=70,
    delta_t_max_50=77,
)

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

CP35447 = ThermoElectricCooler(
    mfn="CP353047",
    datasheet_link=CP35_DATASHEET_LINK,
    v_max=15.4,
    i_max=3.5,
    q_max_27=29.0,
    q_max_50=32.0,
    delta_t_max_27=70.0,
    delta_t_max_50=77.0,
)

CP354047 = ThermoElectricCooler(
    mfn="CP354047",
    datasheet_link=CP35_DATASHEET_LINK,
    v_max=24.1,
    i_max=3.5,
    q_max_27=49.0,
    q_max_50=53.0,
    delta_t_max_27=70.0,
    delta_t_max_50=77.0,
)
