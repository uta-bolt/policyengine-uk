import policyengine_uk
from policyengine_uk.model_api import *
from typing import Union


def set_parameter(
    path: Union[Parameter, str], value: float, period: str = "year:2015:10"
) -> Reform:
    if isinstance(path, Parameter):
        path = path.name

    def modifier(parameters: ParameterNode):
        node = parameters
        for name in path.split("."):
            try:
                if "[" not in name:
                    node = node.children[name]
                else:
                    try:
                        name, index = name.split("[")
                        index = int(index[:-1])
                        node = node.children[name].brackets[index]
                    except:
                        raise ValueError(
                            "Invalid bracket syntax (should be e.g. tax.brackets[3].rate"
                        )
            except:
                raise ValueError(
                    f"Could not find the parameter (failed at {name})."
                )
        node.update(period=period, value=value)
        return parameters

    class reform(Reform):
        def apply(self):
            self.modify_parameters(modifier)

    return reform


def change_parameter(
    path: Parameter, value: float, period: str = "year:2015:10"
) -> Reform:
    path = path.name

    def modifier(parameters: ParameterNode):
        node = parameters
        for name in path.split("."):
            try:
                if "[" not in name:
                    node = node.children[name]
                else:
                    try:
                        name, index = name.split("[")
                        index = int(index[:-1])
                        node = node.children[name].brackets[index]
                    except:
                        raise ValueError(
                            "Invalid bracket syntax (should be e.g. tax.brackets[3].rate"
                        )
            except:
                raise ValueError(
                    f"Could not find the parameter (failed at {name})."
                )
        node.update(period=period, value=node.get_at_instant(period))
        return parameters

    class reform(Reform):
        def apply(self):
            self.modify_parameters(modifier)

    return reform
