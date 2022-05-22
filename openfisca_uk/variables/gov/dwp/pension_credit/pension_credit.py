from openfisca_uk.model_api import *


class pension_credit(Variable):
    label = "Pension Credit"
    entity = BenUnit
    definition_period = YEAR
    value_type = float
    unit = GBP
    reference = "https://www.legislation.gov.uk/ukpga/2002/16/contents"

    def formula(benunit, period, parameters):
        entitlement = benunit("pension_credit_entitlement", period)
        would_claim = benunit("would_claim_pc", period)
        return entitlement * would_claim
