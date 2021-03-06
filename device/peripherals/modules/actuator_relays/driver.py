# Import standard python modules
import time, threading

# Import python types
from typing import NamedTuple, Optional, Dict

# Import device utilities
from device.utilities import bitwise, logger
from device.utilities.communication.i2c.main import I2C
from device.utilities.communication.i2c.exceptions import I2CError
from device.utilities.communication.i2c.mux_simulator import MuxSimulator

# Import driver elements
from device.peripherals.modules.actuator_relays import exceptions, simulator

class ArduinoRelaysDriver:
    """Driver for ArduinoRelays digital to analog converter."""

    def __init__(
        self,
        name: str,
        i2c_lock: threading.RLock,
        bus: int,
        address: int,
        mux: Optional[int] = None,
        channel: Optional[int] = None,
        simulate: bool = False,
        mux_simulator: Optional[MuxSimulator] = None,
    ) -> None:
        """Initializes ArduinoRelays."""

        # Initialize logger
        logname = "ArduinoRelays({})".format(name)
        self.logger = logger.Logger(logname, "peripherals")

        # Initialize i2c lock
        self.i2c_lock = i2c_lock

        # Check if simulating
        if simulate:
            self.logger.info("Simulating driver")
            Simulator = ArduinoRelaysSimulator
        else:
            Simulator = None

        # Initialize I2C
        try:
            self.i2c = I2C(
                name="ArduinoRelays-{}".format(name),
                i2c_lock=i2c_lock,
                bus=bus,
                address=address,
                mux=mux,
                channel=channel,
                mux_simulator=mux_simulator,
                PeripheralSimulator=Simulator,
            )
        except I2CError as e:
            raise exceptions.InitError(logger=self.logger) from e

    def set_high(self, port: int, retry: bool = True, disable_mux: bool = False) -> None:
        """Sets port high."""
        self.logger.debug("Setting port {} high".format(port))

        # Check valid port range
        if port < 0 or port > 4:
            message = "port out of range, must be within 0-3"
            raise exceptions.SetHighError(message=message, logger=self.logger)

        # Lock thread in case we have multiple io expander instances
        with self.i2c_lock:

            # Send set output command
            try:
                self.i2c.write(bytes([port, 1]), disable_mux=disable_mux)
            except I2CError as e:
                raise exceptions.SetHighError(logger=self.logger) from e

    def set_low(self, port: int, retry: bool = True, disable_mux: bool = False) -> None:
        """Sets port low."""
        self.logger.debug("Setting port {} low".format(port))

        # Check valid port range
        if port < 0 or port > 4:
            message = "port out of range, must be within 0-3"
            raise exceptions.SetLowError(message=message, logger=self.logger)

        # Lock thread in case we have multiple io expander instances
        with self.i2c_lock:

            # Send set output command
            try:
                self.i2c.write(bytes([port, 0]), disable_mux=disable_mux)
            except I2CError as e:
                raise exceptions.SetHighError(logger=self.logger) from e
