from policyengine_uk.model_api import *


class uc_income_reduction(Variable):
    value_type = float
    entity = BenUnit
    label = "reduction from income for Universal Credit"
    definition_period = YEAR
    unit = GBP
    defined_for = "is_uc_eligible"

    def formula(benunit, period, parameters):
        num_children = benunit("benunit_count_children", period)
        has_children = num_children > 0
        base_means_test = parameters(period).gov.dwp.universal_credit.means_test

        # Create the reduction rate based on whether each unit has children
        # Use where() to apply different rates conditionally
        reduction_rate = np.where(
            has_children,
            base_means_test.reduction_rate
            - 0.03,  # Reduced rate for families with children
            base_means_test.reduction_rate,  # Standard rate for families without children
        )

        earned_income = benunit("uc_earned_income", period)
        earned_income_reduction = reduction_rate * earned_income

        # p = parameters(period).gov.dwp.universal_credit.means_test
        # if has_children:
        #     p = parameters(period).gov.dwp.universal_credit.means_test - 0.2

        # earned_income = benunit("uc_earned_income", period)
        # earned_income_reduction = p.reduction_rate * earned_income
        unearned_income_reduction = benunit("uc_unearned_income", period)
        maximum_credit = benunit("uc_maximum_amount", period)
        total_reduction = earned_income_reduction + unearned_income_reduction
        return min_(
            maximum_credit,
            total_reduction,
        )


class reform(Reform):
    def apply(self):
        # if "uc_phase_in_addition" not in self.variables:
        #     self.add_variable(uc_phase_in_addition)
        # self.update_variable(uc_child_element)
        self.update_variable(uc_income_reduction)
