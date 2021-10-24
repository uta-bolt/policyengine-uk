from openfisca_uk.tools.general import *
from openfisca_uk.entities import *


class earned_income(Variable):
    value_type = float
    entity = Person
    label = u"Total earned income"
    definition_period = YEAR

    def formula(person, period, parameters):
        COMPONENTS = [
            "employment_income",
            "self_employment_income",
            "pension_income",
        ]
        return add(person, period, COMPONENTS)


class sublet_income(Variable):
    value_type = float
    entity = Person
    label = u"Income received from sublet agreements"
    definition_period = YEAR


class miscellaneous_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from other sources"
    definition_period = YEAR


class private_transfer_income(Variable):
    value_type = float
    entity = Person
    label = u"Private transfers"
    definition_period = YEAR


class lump_sum_income(Variable):
    value_type = float
    entity = Person
    label = u"Lump sum income"
    definition_period = YEAR


class market_income(Variable):
    value_type = float
    entity = Person
    label = u"Market income"
    definition_period = YEAR

    def formula(person, period, parameters):
        return (
            add(
                person,
                period,
                [
                    "employment_income",
                    "self_employment_income",
                    "savings_interest_income",
                    "dividend_income",
                    "miscellaneous_income",
                    "property_income",
                    "pension_income",
                    "private_transfer_income",
                    "maintenance_income",
                ],
            )
            - person("maintenance_expenses", period)
        )


class gross_income(Variable):
    value_type = float
    entity = Person
    label = u"Gross income, including benefits"
    definition_period = YEAR

    def formula(person, period, parameters):
        COMPONENTS = [
            "employment_income",
            "pension_income",
            "self_employment_income",
            "property_income",
            "savings_interest_income",
            "dividend_income",
            "miscellaneous_income",
            "benefits",
        ]
        return add(person, period, COMPONENTS)


class net_income(Variable):
    value_type = float
    entity = Person
    label = u"Net income"
    definition_period = YEAR

    def formula(person, period, parameters):
        return person("gross_income", period) - person("tax", period)


class hours_worked(Variable):
    value_type = float
    entity = Person
    label = u"Total amount of hours worked by this person"
    definition_period = YEAR


class in_work(Variable):
    value_type = bool
    entity = Person
    label = u"Worked some hours"
    definition_period = YEAR

    def formula(person, period, parameters):
        has_hours_worked = person("hours_worked", period) > 0
        has_earnings = (
            add(
                person, period, ["employment_income", "self_employment_income"]
            )
            > 0
        )
        return has_hours_worked | has_earnings


class weekly_hours(Variable):
    value_type = float
    entity = Person
    label = u"Average weekly hours for the year"
    definition_period = YEAR

    def formula(person, period, parameters):
        return person("hours_worked", period) / WEEKS_IN_YEAR


class EmploymentStatus(Enum):
    FT_EMPLOYED = "Full-time employed"
    PT_EMPLOYED = "Part-time employed"
    FT_SELF_EMPLOYED = "Full-time self-employed"
    PT_SELF_EMPLOYED = "Part-time self-employed"
    UNEMPLOYED = "Unemployed"
    RETIRED = "Retired"
    STUDENT = "Student"
    CARER = "Carer"
    LONG_TERM_DISABLED = "Long-term sick/disabled"
    SHORT_TERM_DISABLED = "Short-term sick/disabled"
    OTHER_INACTIVE = "Inactive for another reason"
    CHILD = "Child"


class employment_status(Variable):
    value_type = Enum
    entity = Person
    possible_values = EmploymentStatus
    default_value = EmploymentStatus.UNEMPLOYED
    label = u"Employment status of the person"
    definition_period = YEAR


class capital_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from savings or dividends"
    definition_period = YEAR

    def formula(person, period, parameters):
        return add(
            person, period, ["savings_interest_income", "dividend_income"]
        )


class maintenance_income(Variable):
    value_type = float
    entity = Person
    label = u"Maintenance payments"
    definition_period = YEAR


class household_net_income(Variable):
    value_type = float
    entity = Household
    label = u"Household net income"
    definition_period = YEAR

    def formula(household, period, parameters):
        return max_(
            0,
            aggr(household, period, ["net_income"])
            - household("council_tax", period),
        )


class household_net_income_ahc(Variable):
    value_type = float
    entity = Household
    label = u"Household net income, after housing costs"
    definition_period = YEAR

    def formula(household, period, parameters):
        return household("household_net_income", period) - household(
            "housing_costs", period
        )


class equiv_household_net_income(Variable):
    value_type = float
    entity = Household
    label = u"Equivalised household net income"
    definition_period = YEAR

    def formula(household, period, parameters):
        return household("household_net_income", period) / household(
            "household_equivalisation_bhc", period
        )


class equiv_household_net_income_ahc(Variable):
    value_type = float
    entity = Household
    label = u"Equivalised household net income, after housing costs"
    definition_period = YEAR

    def formula(household, period, parameters):
        return household("household_net_income_ahc", period) / household(
            "household_equivalisation_ahc", period
        )


class base_net_income(Variable):
    value_type = float
    entity = Person
    label = "Existing net income for the person to use as a base in microsimulation"
    definition_period = YEAR
