from openfisca_uk.model_api import *


class winter_fuel_allowance_reported(Variable):
    value_type = float
    entity = Person
    label = "Winter fuel allowance"
    definition_period = YEAR
    unit = GBP


@uprated(by="uprating.september_cpi")
class winter_fuel_allowance(Variable):
    label = "Winter Fuel Allowance"
    entity = Household
    definition_period = YEAR
    value_type = float
    unit = GBP

    def formula(household, period, parameters):
        return aggr(household, period, ["winter_fuel_allowance_reported"])
