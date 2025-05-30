from policyengine_uk.model_api import *


class uc_child_element(Variable):
    value_type = float
    entity = BenUnit
    label = "Universal Credit child element (with phase-in)"
    definition_period = YEAR
    unit = GBP

    # Keep the original structure that adds up individual child elements
    adds = ["uc_individual_child_element", "uc_phase_in_addition"]


# Create a new variable for the phase-in addition
class uc_phase_in_addition(Variable):
    value_type = float
    entity = BenUnit
    label = "Universal Credit phase-in addition"
    documentation = "Additional UC child element for phase-in policy"
    definition_period = YEAR
    unit = GBP

    def formula(benunit, period, parameters):
        # Get employment income for phase-in logic
        employment_income = benunit("employment_income", period)

        # Only apply if there are children
        num_children = benunit("benunit_count_children", period)
        has_children = num_children > 0

        # Phase-in parameters
        phase_in_threshold = 3000.0  # End of phase 1
        flat_end = 4000.0  # End of phase 2 (flat section)

        # Phase 1: 0 to £3000 - add 0.2 * employment_income
        phase1_addition = 0.2 * employment_income

        # Phase 2: £3000 to £4000 - flat (keep the same addition as at £3000)
        phase2_addition = 0.2 * phase_in_threshold  # = 0.2 * 3000 = £600

        # Phase 3: £4000+ - no addition
        phase3_addition = 0.2 * phase_in_threshold  # 0.0

        # Apply phase logic
        addition = where(
            employment_income <= phase_in_threshold,
            phase1_addition,  # Phase 1: 0 to £3000
            where(
                employment_income <= flat_end,
                phase2_addition,  # Phase 2: £3000 to £4000 (flat)
                phase3_addition,  # Phase 3: £4000+
            ),
        )

        # Only apply if there are children
        final_addition = where(has_children, addition, 0.0)

        return max_(0, final_addition)


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
            - 0.02,  # Reduced rate for families with children
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
        if "uc_phase_in_addition" not in self.variables:
            self.add_variable(uc_phase_in_addition)
        self.update_variable(uc_child_element)
        self.update_variable(uc_income_reduction)
