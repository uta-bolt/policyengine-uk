from openfisca_uk.model_api import *


@uprated(by="wealth.national_balance_sheet.household.land")
class owned_land(Variable):
    entity = Household
    label = "Owned land"
    documentation = "Total value of all land-only plots owned by the household"
    unit = GBP
    definition_period = YEAR
    value_type = float
    quantity_type = STOCK


class land_value(Variable):
    label = "Land value"
    documentation = (
        "Estimated total land value (directly and indirectly owned)"
    )
    entity = Household
    definition_period = YEAR
    value_type = float
    unit = GBP
    quantity_type = STOCK

    def formula(household, period):
        VARIABLES = [
            "household_land_value",
            "corporate_land_value",
        ]
        return add(household, period, VARIABLES)


class household_land_value(Variable):
    entity = Household
    label = "Land value"
    documentation = (
        "Estimated total land value directly owned by the household"
    )
    unit = GBP
    definition_period = YEAR
    value_type = float
    quantity_type = STOCK

    def formula(household, period, parameters):
        wealth = parameters(period).wealth
        property_wealth_intensity = (
            wealth.land.value.aggregate_household_land_value
            / wealth.property_wealth
        )
        property_wealth = household("property_wealth", period)
        owned_land = household("owned_land", period)
        return property_wealth * property_wealth_intensity + owned_land


class corporate_land_value(Variable):
    entity = Household
    label = "Land value"
    documentation = "Estimated total land value indirectly owned by the household from corporate holdings"
    unit = GBP
    definition_period = YEAR
    value_type = float
    quantity_type = STOCK

    def formula(household, period, parameters):
        wealth = parameters(period).wealth
        corporate_wealth = household("corporate_wealth", period)
        corporate_wealth_intensity = (
            wealth.land.value.aggregate_corporate_land_value
            / wealth.corporate_wealth
        )
        return corporate_wealth * corporate_wealth_intensity
