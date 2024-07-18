"""Module for calculating operating points of TEC module.

The equations and theory used here is mostly taken from:
https://www.electronics-cooling.com/2008/08/a-simple-method-to-estimate-the-physical-characteristics-of-a-thermoelectric-cooler-from-vendor-datasheets/
"""

# System imports
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

# Library imports
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from pydantic import BaseModel, Field

# Local imports

# Typing imports
if TYPE_CHECKING:
    from pathlib import Path

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
    ) -> tuple[float, float, float, float]:
        """Calculate the operating point of the TEC module."""
        voltage = self.voltage(current=current, t_hot=t_hot, t_cold=t_cold)
        electrical_power = voltage * current
        cooling_power = self.cooling_power(current=current, t_hot=t_hot, t_cold=t_cold)
        figure_of_merit = self.figure_of_merit(t_hot=t_hot)

        coefficient_of_performance = cooling_power / electrical_power
        return voltage, cooling_power, coefficient_of_performance, figure_of_merit

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

    def plot_operating_regions(
        self,
        t_cold: float,
        currents: list[float],
        t_hots: list[float],
        hot_side_sink_rj: float,
        output_path: Path,
    ) -> None:
        """Plot the operating regions of the TEC module."""
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(  # type: ignore[misc]
            2, 3, figsize=(22, 15)
        )
        ax1 = cast(Axes, ax1)
        ax2 = cast(Axes, ax2)
        ax3 = cast(Axes, ax3)
        ax4 = cast(Axes, ax4)
        ax5 = cast(Axes, ax5)
        ax6 = cast(Axes, ax6)

        fig.suptitle(f"{self.mfn} operating points.\nTc = {t_cold - 273.15}°C.")
        ax1.set_xlabel("Current (A)")
        ax2.set_xlabel("Current (A)")
        ax3.set_xlabel("Current (A)")
        ax4.set_xlabel("Current (A)")
        ax5.set_xlabel("Current (A)")
        ax6.set_xlabel("Current (A)")

        ax1.set_ylabel("Voltage (V)")
        ax2.set_ylabel("Cooling Power (W)")
        ax3.set_ylabel("COP")
        ax4.set_ylabel("Ambient Temperature (°C)")
        ax5.set_ylabel("Figure of Merit")

        colors = [f"C{i}" for i in range(len(t_hots))]

        line_vs = []
        line_qs = []
        line_cops = []
        line_t_ambients = []
        line_figure_of_merits = []

        for t_hot, color in zip(t_hots, colors, strict=True):
            voltages: list[float] = []
            cooling_powers: list[float] = []
            cops: list[float] = []
            t_ambients: list[float] = []
            figure_of_merits: list[float] = []

            for current in currents:
                voltage, cooling_power, cop, figure_of_merit = self.operating_params(
                    current=current, t_hot=t_hot, t_cold=t_cold
                )
                input_power = voltage * current
                t_ambient = t_hot - (input_power + cooling_power) * hot_side_sink_rj
                t_ambient_c = t_ambient - 273.15

                voltages.append(voltage)
                cooling_powers.append(cooling_power)
                cops.append(cop)
                t_ambients.append(t_ambient_c)
                figure_of_merits.append(figure_of_merit)

            t_hot_c = t_hot - 273.15
            label = f"Th = {t_hot_c:.2f}°C"
            line_v = ax1.plot(currents, voltages, f"{color}o-", label=label)
            line_q = ax2.plot(currents, cooling_powers, f"{color}o-", label=label)
            line_cop = ax3.plot(currents, cops, f"{color}o-", label=label)
            line_t_ambient = ax4.plot(currents, t_ambients, f"{color}o-", label=label)
            line_figure_of_merit = ax5.plot(
                currents, figure_of_merits, f"{color}o-", label=label
            )

            line_vs += line_v
            line_qs += line_q
            line_cops += line_cop
            line_t_ambients += line_t_ambient
            line_figure_of_merits += line_figure_of_merit

        ax1.legend(handles=line_vs)
        ax2.legend(handles=line_qs)
        ax3.legend(handles=line_cops)
        ax4.legend(handles=line_t_ambients)
        ax5.legend(handles=line_figure_of_merits)

        plt.savefig(str(output_path.absolute()))
