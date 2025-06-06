from pyrk.utilities.ur import units

class ConductivityModel(object):
    '''This class defines the model for thermal conductivity: k'''

    def __init__(self,
                 a= 0 * units.watt / (units.meter * units.kelvin),
                 b= 0 * units.watt / (units.meter * units.kelvin) / units.kelvin,
                 model="linear"):
        
        """
        Initialates the ConductivityModel object.
        :param model: The keyword for a model type.
        :type model: string
        :param a: first coefficient of the model
        :type a: float.
        :param b: second coefficient of the model.
        :type b: float
        """

        self.a = a.to(units.watt / (units.meter * units.kelvin))
        self.b = b.to(units.watt / (units.meter * units.kelvin) / units.kelvin)

        self.implemented = {'constant': self.constant,
                            'linear': self.linear}

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Conductivity model type "
            msg += model
            msg += " is not an implemented conductivity model. Options are:"
            for m in self.implemented.keys():
                msg += m
            raise ValueError(msg)
    
    def k(self, temp=0 * units.kelvin):
        """
        Returns the thermal conductivity based on the temperature.

        :param temp: the temperature
        :type temp: float.
        """
        return self.implemented[self.model](temp)
    
    def constant(self, temp=0 * units.kelvin):
        """
        Returns a constant thermal conductivity, a.

        :param temp: The temperature of the object
        :type temp: float.
        """
        # returns 1 since thats what the original code did with no temperature dependence
        return 1 * units.watt / (units.meter * units.kelvin)
    
    def linear(self, temp=0.0 * units.kelvin):
        """
        Returns a linear dependence on temperature ($ a + b*temp$) .

        :param temp: The temperature of the object
        :type temp: float. units of kelvin
        """
        #converts kelvin to celsius to match the original model
        ret = self.a + self.b * (temp - (273.15 * units.kelvin))
        return ret