"""Module for calculating operating points of TEC module.

The equations and theory used here is mostly taken from:
https://www.electronics-cooling.com/2008/08/a-simple-method-to-estimate-the-physical-characteristics-of-a-thermoelectric-cooler-from-vendor-datasheets/
"""

# System imports
from __future__ import annotations

import logging

# Library imports
from pydantic import BaseModel, Field

# Local imports

# Typing imports

logger = logging.getLogger(__name__)


class ThermoElectricCooler(BaseModel):
    """Definition of a TEC (ThermoElectric Cooler) module."""

    mfn: str = Field(
        description="The manufacturers part number for the device.",
    )
    datasheet_link: str = Field(description="Link to the datasheet for the device.")
    v_max: float = Field(
        description=(
            "Voltage [V] operating point for max delta T and hot side temp of 27°C."
        )
    )
    i_max: float = Field(
        description=(
            "Current [A] operating point for max delta T and hot side temp of 27°C."
        )
    )
    q_max_27: float = Field(
        description=(
            "Max cooling capacity [W] when operating at i_max and v_max and hot side "
            "temp of 27°C and delta T of 0°C."
        )
    )
    q_max_50: float = Field(
        description=(
            "Max cooling capacity [W] when operating at i_max and v_max and hot side "
            "temp of 50°C and delta T of 0°C."
        )
    )
    delta_t_max_27: float = Field(
        description=(
            "Max delta T from hot side to cool side [°C/°K] when operating at i_max "
            "and v_max and hot side temp of 27°C and 0W."
        )
    )
    delta_t_max_50: float = Field(
        description=(
            "Max delta T from hot side to cool side [°C/°K] when operating at i_max "
            "and v_max and hot side temp of 50°C and 0W."
        )
    )

    def figure_of_merit(self, t_hot: float) -> float:
        """Calc the figure of merit of the TEC module at a given hot side temp.

        See reference link at top of file: EQN 19.
        """
        return 2 * self.delta_t_max_27 / (t_hot - self.delta_t_max_27) ** 2

    def seebeck_coefficient(self, t_hot: float) -> float:
        """Calc the Seebeck coefficient of the TEC module at a given hot side temp.

        See reference link at top of file: EQN 20.
        """
        return self.v_max / t_hot

    def thermal_conductance(self, t_hot: float) -> float:
        """Calc the thermal conductance of the TEC module at a given hot side temp.

        See reference link at top of file: EQN 21.
        """
        return ((t_hot - self.delta_t_max_27) * self.v_max * self.i_max) / (
            2 * t_hot * self.delta_t_max_27
        )

    def module_resistance(self, t_hot: float) -> float:
        """Calc the resistance of the TEC module at a given hot side temp.

        See reference link at top of file: EQN 22.
        """
        return (t_hot - self.delta_t_max_27) * self.v_max / (t_hot * self.i_max)

    def cooling_power(self, current: float, t_hot: float, t_cold: float) -> float:
        """Calculate the cooling power of the TEC module.

        See reference link at top of file: EQN 8.
        """
        r = self.module_resistance(t_hot=t_hot)
        s_m = self.seebeck_coefficient(t_hot=t_hot)
        k_m = self.thermal_conductance(t_hot=t_hot)
        i = current
        dt = t_hot - t_cold

        return (s_m * t_cold * i) - (0.5 * i**2 * r) - (k_m * dt)

    def voltage(self, current: float, t_hot: float, t_cold: float) -> float:
        """Calculate the voltage across the TEC module.

        See reference link at top of file: EQN 9.
        """
        r = self.module_resistance(t_hot=t_hot)
        i = current
        s_m = self.seebeck_coefficient(t_hot=t_hot)
        dt = t_hot - t_cold

        return s_m * dt + r * i

    def operating_params(
        self, current: float, t_hot: float, t_cold: float
    ) -> tuple[float, float, float]:
        """Calculate the operating point of the TEC module."""
        voltage = self.voltage(current=current, t_hot=t_hot, t_cold=t_cold)
        electrical_power = voltage * current
        cooling_power = self.cooling_power(current=current, t_hot=t_hot, t_cold=t_cold)

        coefficient_of_performance = cooling_power / electrical_power
        return voltage, cooling_power, coefficient_of_performance

    def coefficient_of_performance(
        self, current: float, t_hot: float, t_cold: float
    ) -> float:
        """Calculate the operating point of the TEC module.

        See reference link at top of file: EQN 10.
        """
        voltage = self.voltage(current=current, t_hot=t_hot, t_cold=t_cold)
        electrical_power = voltage * current
        cooling_power = self.cooling_power(current=current, t_hot=t_hot, t_cold=t_cold)

        return cooling_power / electrical_power
