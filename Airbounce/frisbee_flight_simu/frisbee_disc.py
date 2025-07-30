from collections import OrderedDict, namedtuple
from numbers import Number
from typing import List, Optional, Set

import numpy as np
from scipy.integrate import solve_ivp

from frisbee_flight_simu.physics_model import Environment_Variables
from frisbee_flight_simu.physics_model import Coeff_Model
from frisbee_flight_simu.eom import EOM

class Frisbee_Disc:
    _default_initial_conditions = OrderedDict(
        {
            "x": 0,
            "y": 0,
            "z": 1.0,
            "vx": 10.0,
            "vy": 0,
            "vz": 0,
            "phi": 0,
            "theta": 0,
            "gamma": 0,
            "dphi": 0,
            "dtheta": 0,
            "dgamma": 62.0,
        }
    )

    _default_physical_attributes = {
         # "area": 0.017401,  # m^2
         "area": 0.034631,  # m^2
         # "area": 0.041541,  # m^2

        "I_zz": 0.0023052,  # kg*m^2
        # "I_zz": 0.0020052,  # kg*m^2
        # "I_xx": 0.001019,  # kg*m^2
        "I_xx": 0.001219,  # kg*m^2

         "mass": 0.0953,     # kg
        # "mass": 0.0889,     # kg
         # "mass": 0.1432,     # kg
    }

    def __init__(self, model = Coeff_Model(), eom: Optional[EOM] = None, **kwargs):
         self.model = model;
         self.set_physical_attributes(**kwargs);
         self.set_default_initial_conditions(**kwargs);
         self.reset_initial_conditions();
         self.eom = eom or EOM(model=self.model,area=self.area,I_xx=self.I_xx,I_zz=self.I_zz,mass=self.mass);

    def compute_trajectory(self, flight_time = 3.0, n_times = 100, return_scipy_results = False,**kwargs):
        t_span = kwargs.pop("t_span", (0, flight_time));
        t_eval: np.ndarray = kwargs.pop("t_eval", np.linspace(t_span[0], t_span[1], n_times));

        result = solve_ivp(fun=self.eom.compute_derivatives,t_span=t_span,y0=list(self.initial_conditions.values()),t_eval=t_eval,**kwargs);

        if kwargs.get("dense_output", False):
            return result;

        # Set the current coordinates to the last point
        self.current_coordinates = result.y[:, -1];

        # Create the results object
        fpr = Result(times=result.t, *result.y);

        # If specified, return a results object
        if return_scipy_results:
            return fpr, result;
        else:
            return fpr;

    def reset_initial_conditions(self):
        self.initial_conditions = self.default_initial_conditions;
        return

    def set_default_initial_conditions(self, **kwargs):
        initial_conditions = self._default_initial_conditions.copy();

        valid_keys: Set[str] = set(initial_conditions.keys()).union(set(self._default_physical_attributes.keys()));

        for key, value in kwargs.items():
            assert key in valid_keys, f"invalid key {key}"
            if key in self._default_physical_attributes:
                pass
            msg = f"invalid type for {key}={value}; {type(value)}";

            assert isinstance(value, Number), msg;
            initial_conditions[key] = value;

        self.default_initial_conditions = initial_conditions;
        return

    def set_physical_attributes(self, **kwargs):
        for key, value in self._default_physical_attributes.items():
            setattr(self, key, kwargs.get(key, value));
        return

    @property
    def environment(self):
        return self.eom.environment;

    @property
    def coordinate_names(self):
        return list(self._default_initial_conditions.keys());


class Result(namedtuple("Result", list(Frisbee_Disc._default_initial_conditions.keys()) + ["times"])):
     pass
