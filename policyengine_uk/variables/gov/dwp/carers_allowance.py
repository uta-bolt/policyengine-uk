from policyengine_uk.model_api import *


class receives_carers_allowance(Variable):
    value_type = bool
    entity = Person
    label = "Receives Carer's Allowance"
    definition_period = YEAR

    def formula(person, period, parameters):
        return person("carers_allowance", period) > 0


class carers_allowance(Variable):
    value_type = float
    entity = Person
    label = "Carer's Allowance"
    definition_period = YEAR
    unit = GBP

    def formula(person, period, parameters):
        receives_ca = person("carers_allowance_reported", period) > 0
        rate = parameters(period).gov.dwp.carers_allowance.rate
        return receives_ca * rate * WEEKS_IN_YEAR


class carers_allowance_reported(Variable):
    value_type = float
    entity = Person
    label = "Carer's Allowance (reported)"
    definition_period = YEAR
    unit = GBP
