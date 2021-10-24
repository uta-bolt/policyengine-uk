from openfisca_uk.tools.general import *
from openfisca_uk.entities import *

"""
The calculation of income tax is specified by the Income Tax Act 2007 s. 23
which outlines the main steps. Step 1 indicates that the components of 'total income'
should be added together, but the Act itself does not specify what those components are.
Instead, other Acts (the Income Tax (Earnings and Pensions) Act 2003 and the Income Tax 
(Trading and Other Income) Act 2005) impose the charges to income tax on each component of
income. The relevant sections of each act imposing charges to income tax are given 
for each component of income below. The components are guided by the article at 
https://www.pruadviser.co.uk/knowledge-literature/knowledge-library/the-seven-steps-required-to-calculate-an-individuals-income-tax-liability/
"""


@uprated(by="earnings")
class employment_income(Variable):
    value_type = float
    entity = Person
    label = u"Employment income"
    documentation = "Total income from employment"
    definition_period = YEAR
    reference = "Income Tax (Earnings and Pensions) Act 2003 s. 1(1)(a)"
    metadata = dict(
        policyengine=dict(
            roles=dict(
                adult=dict(
                    max=80000,
                ),
                child=dict(
                    max=20000,
                ),
            )
        )
    )


@uprated(by="earnings")
class pension_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from pensions"
    definition_period = YEAR
    reference = "Income Tax (Earnings and Pensions) Act 2003 s. 1(1)(b)"
    metadata = dict(
        policyengine=dict(
            roles=dict(
                adult=dict(
                    max=80000,
                ),
                child=dict(
                    hidden=True,
                ),
            )
        )
    )


class social_security_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from social security for tax purposes"
    definition_period = YEAR
    reference = "Income Tax (Earnings and Pensions) Act 2003 s. 1(1)(b)"

    def formula(person, period, parameters):
        COMPONENTS = [
            "state_pension",
            "incapacity_benefit",
            "JSA_contrib",
            "ESA_contrib",
            "carers_allowance",
        ]
        return add(person, period, COMPONENTS, options=[ADD])


@uprated(by="earnings")
class self_employment_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from trading profits for owned businesses"
    definition_period = YEAR
    reference = "Income Tax (Trading and Other Income) Act 2005 s. 1(1)(a)"
    metadata = dict(
        policyengine=dict(
            roles=dict(
                adult=dict(
                    max=80000,
                ),
                child=dict(
                    hidden=True,
                ),
            )
        )
    )


@uprated(by="earnings")
class property_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from rental of property"
    definition_period = YEAR
    reference = "Income Tax (Trading and Other Income) Act 2005 s. 1(1)(b)"
    metadata = dict(
        policyengine=dict(
            roles=dict(
                adult=dict(
                    max=80000,
                ),
                child=dict(
                    hidden=True,
                ),
            )
        )
    )


@uprated(by="earnings")
class savings_interest_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from interest on savings"
    definition_period = YEAR
    reference = "Income Tax (Trading and Other Income) Act 2005 s. 365(1)(a)"
    metadata = dict(
        policyengine=dict(
            roles=dict(
                adult=dict(
                    max=80000,
                ),
                child=dict(
                    hidden=True,
                ),
            )
        )
    )


@uprated(by="earnings")
class dividend_income(Variable):
    value_type = float
    entity = Person
    label = u"Income from dividends"
    definition_period = YEAR
    reference = "Income Tax (Trading and Other Income) Act 2005 s. 365(1)(b-d)"
    metadata = dict(
        policyengine=dict(
            type="yearly",
            roles=dict(
                adult=dict(
                    max=80000,
                ),
                child=dict(
                    hidden=True,
                ),
            ),
        )
    )
