from openfisca_uk.model_api import *


@uprated(by="uprating.september_cpi")
class AFCS(Variable):
    value_type = float
    entity = Person
    label = "Armed Forces Compensation Scheme"
    definition_period = YEAR
    unit = GBP

    def formula(person, period, parameters):
        return person("AFCS_reported", period)


class AFCS_reported(Variable):
    value_type = float
    entity = Person
    label = "Armed Forces Compensation Scheme (reported)"
    definition_period = YEAR
    unit = GBP
