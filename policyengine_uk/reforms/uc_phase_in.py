from policyengine_uk.model_api import *


class uc_income_reduction(Variable):
    value_type = float
    entity = BenUnit
    label = "phase_in income for Universal Credit"
    definition_period = YEAR
    unit = GBP
    defined_for = "is_uc_eligible"

    def formula(benunit, period, parameters):
        increased_max = 1000  # hardcoded for now
        phase_in_rate = 0.1  # hardcoded for now
        person = benunit.members
        is_child = person("is_child_or_QYP", period)
        has_children = benunit.any(is_child)
        p = parameters(period).gov.dwp.universal_credit.means_test
        earned_income = benunit("uc_earned_income", period)
        earned_income_reduction = p.reduction_rate * earned_income
        earned_income_increase = (
            phase_in_rate * earned_income * has_children
        )  # only if there are children in the HH
        unearned_income_reduction = benunit("uc_unearned_income", period)
        maximum_credit = benunit("uc_maximum_amount", period)
        maximum_credit = (
            maximum_credit + increased_max * has_children
        )  # only if there are children in the HH
        # I am basically adding a negative reduction
        total_reduction = (
            earned_income_reduction + unearned_income_reduction - earned_income_increase
        )

        return min_(
            maximum_credit,
            total_reduction,
        )


# Export this as `reform`
class reform(Reform):
    def apply(self):
        self.update_variable(uc_income_reduction)
