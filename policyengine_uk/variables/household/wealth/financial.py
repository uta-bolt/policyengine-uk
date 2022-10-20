from policyengine_uk.model_api import *


@uprated(
    by="household.wealth.national_balance_sheet.household.financial_net_worth"
)
class gross_financial_wealth(Variable):
    label = "Gross financial wealth"
    entity = Household
    definition_period = YEAR
    value_type = float
    unit = GBP


@uprated(
    by="household.wealth.national_balance_sheet.household.financial_net_worth"
)
class net_financial_wealth(Variable):
    label = "Net financial wealth"
    entity = Household
    definition_period = YEAR
    value_type = float
    unit = GBP
