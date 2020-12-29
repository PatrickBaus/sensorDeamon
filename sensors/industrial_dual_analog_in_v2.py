# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright (C) 2020  Patrick Baus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

from .sensor import Sensor
from .tinkerforge.bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2 as Bricklet

class IndustrialDualAnalogInV2(Sensor):
    """
    API Wrapper for the Tinkerforge Industrial Dual Analog In Bricklet v2.x bricklet
    """
    UNIT = "V"
    # The type will be used for describing the sensor, like "Registering %TYPE sensor."
    TYPE = "voltage"
    DEVICE_IDENTIFIER = Bricklet.DEVICE_IDENTIFIER

    @property
    def unit(self):
        """
        Returns the SI unit of the measurand.
        """
        return self.UNIT

    @property
    def sensor_type(self):
        """
        Return the type of mesurand beeing measured.
        """
        return self.TYPE

    @property
    def sensor_callback_period(self):
        """
        Returns the callback period in ms.
        """
        return self.bricklet.get_temperature_callback_configuration().period

    @property
    def bricklet(self):
        """
        Returns the Tinkerforge API Bricklet object
        """
        return self.__bricklet

    def callback(self, value):
        """
        This method will be called by the API, when a new value is available.
        It does all the conversion to the apropriate SI unit specified by getUnit().
        value: the value as returned by the bricklet. This might not be in SI units.
        """
        # Return K.
        value = (value + 27315) / 100
        super().callback(value)

    def set_callback(self):
        """
        Sets the callback period and registers the method callback() with the Tinkerforge API.
        """
        self.bricklet.set_voltage_callback_configuration(period=self.callback_period, value_has_to_change=True, option="x", min=0, max=0)
        self.bricklet.register_callback(self.bricklet.CALLBACK_VOTAGE, self.callback)

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, the position, the hardware and firmware version as well as the device identifier.
        http://www.tinkerforge.com/en/doc/Software/Bricklets/AmbientLight_Bricklet_Python.html
        """
        return self.bricklet.get_identity()

    def __init__(self, uid, parent, callback_method, callback_period=0):
        """
        Create new sensor Object.
        uid: UID of the sensor
        parent: The SensorHost object to which the sensor is connected
        callbackMethod: The SensorHost callback to deliver to the data to.
        callbackPeriod: The callback period in ms. A value of 0 will turn off the callback.
        """
        super().__init__(uid, parent, callback_method, callback_period)

        self.__bricklet = Bricklet(uid, parent.ipcon)
        self.set_callback()
