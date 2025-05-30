from policyengine_uk.model_api import *


# class uc_income_reduction(Variable):
#     value_type = float
#     entity = BenUnit
#     label = "phase_in income for Universal Credit"
#     definition_period = YEAR
#     unit = GBP
#     defined_for = "is_uc_eligible"

#     def formula(benunit, period, parameters):
#         increased_max = 5000  # hardcoded for now
#         phase_in_rate = 1.4  # hardcoded for now
#         person = benunit.members
#         is_child = person("is_child_or_QYP", period)
#         has_children = benunit.any(is_child)
#         p = parameters(period).gov.dwp.universal_credit.means_test
#         earned_income = benunit("uc_earned_income", period)
#         earned_income_reduction = p.reduction_rate * earned_income
#         earned_income_increase = (
#             phase_in_rate * earned_income * has_children
#         )  # only if there are children in the HH
#         unearned_income_reduction = benunit("uc_unearned_income", period)
#         maximum_credit = benunit("uc_maximum_amount", period)
#         maximum_credit = (
#             maximum_credit + increased_max * has_children
#         )  # only if there are children in the HH
#         # I am basically adding a negative reduction
#         total_reduction = (
#             earned_income_reduction + unearned_income_reduction - earned_income_increase
#         )

#         return min_(
#             maximum_credit,
#             total_reduction,
#         )


# # Export this as `reform`
# class reform(Reform):
#     def apply(self):
#         self.update_variable(uc_income_reduction)
#


# class uc_maximum_amount(Variable):
#     value_type = float
#     entity = BenUnit
#     label = "maximum Universal Credit amount (with phase-in)"
#     documentation = "Modified to include phase-in: household income increases by 1.2x earned income up to £3000"
#     definition_period = YEAR
#     unit = GBP
#     defined_for = "is_uc_eligible"

#     def formula(benunit, period, parameters):
#         # Get the standard UC maximum (sum of all elements)
#         standard_allowance = benunit("uc_standard_allowance", period)
#         child_element = benunit("uc_child_element", period)
#         disability_elements = benunit("uc_disability_elements", period)
#         carer_element = benunit("uc_carer_element", period)
#         housing_costs_element = benunit("uc_housing_costs_element", period)
#         childcare_element = benunit("uc_childcare_element", period)

#         standard_maximum = (
#             standard_allowance
#             + child_element
#             + disability_elements
#             + carer_element
#             + housing_costs_element
#             + childcare_element
#         )

#         # Get earned income
#         earned_income = benunit("uc_earned_income", period)

#         # Phase-in policy parameters
#         phase_in_threshold = 3000  # £3000
#         flat_end = 4000  # £4000
#         multiplier = 1.2  # 1.2x multiplier

#         # Phase 1: 0 to £3000 - household income should be 1.2 * earned_income
#         # So total UC needed = (1.2 * earned_income) - earned_income = 0.2 * earned_income
#         phase1_uc_needed = 0.2 * earned_income

#         # Phase 2: £3000 to £4000 - flat household income at £3600
#         # So UC needed = £3600 - earned_income
#         flat_household_income = multiplier * phase_in_threshold  # £3600
#         phase2_uc_needed = flat_household_income - earned_income

#         # Determine which phase we're in
#         in_phase1 = earned_income <= phase_in_threshold
#         in_phase2 = (earned_income > phase_in_threshold) & (earned_income <= flat_end)
#         in_phase3 = earned_income > flat_end

#         # Calculate required maximum UC for each phase
#         phase_in_maximum = (
#             in_phase1 * phase1_uc_needed
#             + in_phase2 * phase2_uc_needed
#             + in_phase3 * standard_maximum  # Use standard calculation for phase 3
#         )

#         # The maximum should be at least what's needed for the phase-in
#         # but also respect the standard maximum for normal UC elements
#         return max_(phase_in_maximum, standard_maximum)


# class uc_income_reduction(Variable):
#     value_type = float
#     entity = BenUnit
#     label = "reduction from income for Universal Credit (phase-in compatible)"
#     definition_period = YEAR
#     unit = GBP
#     defined_for = "is_uc_eligible"

#     def formula(benunit, period, parameters):
#         p = parameters(period).gov.dwp.universal_credit.means_test
#         earned_income = benunit("uc_earned_income", period)
#         unearned_income_reduction = benunit("uc_unearned_income", period)

#         # Phase-in policy parameters
#         phase_in_threshold = 3000
#         flat_end = 4000

#         # For phases 1 and 2, we want minimal reduction to preserve the phase-in effect
#         # For phase 3, use normal UC taper

#         in_phase1 = earned_income <= phase_in_threshold
#         in_phase2 = (earned_income > phase_in_threshold) & (earned_income <= flat_end)
#         in_phase3 = earned_income > flat_end

#         # Phase 1 & 2: No earned income reduction (let the modified maximum handle it)
#         # Phase 3: Normal UC taper
#         earned_income_reduction = in_phase3 * (p.reduction_rate * earned_income)

#         # Total reduction includes unearned income (unchanged)
#         total_reduction = earned_income_reduction + unearned_income_reduction


#         return max_(0, total_reduction)
# class uc_standard_allowance(Variable):
#     value_type = float
#     entity = BenUnit
#     label = "Universal Credit standard allowance (modified for phase-in)"
#     definition_period = YEAR
#     unit = GBP

#     def formula(benunit, period, parameters):
#         # Get the normal standard allowance calculation
#         p = parameters(period).gov.dwp.universal_credit.standard_allowance
#         claimant_type = benunit("uc_standard_allowance_claimant_type", period)
#         normal_standard_allowance = p.amount[claimant_type] * MONTHS_IN_YEAR

#         # Get earned income for phase-in logic
#         earned_income = benunit("uc_earned_income", period)

#         # Phase-in parameters
#         phase_in_threshold = 3000  # £3000
#         flat_end = 8000  # £4000
#         multiplier = 1.2  # 1.2x multiplier

#         # Phase 1: 0 to £3000 - provide UC to achieve 1.2 * earned_income household income
#         # So UC needed = 0.2 * earned_income
#         phase1_allowance = 1.2 * earned_income

#         # Phase 2: £3000 to £4000 - flat household income at £3600
#         # So UC needed = £3600 - earned_income
#         flat_household_income = multiplier * phase_in_threshold  # £3600
#         phase2_allowance = flat_household_income - earned_income

#         # Phase 3: £4000+ - transition back to normal standard allowance with taper
#         # We'll calculate this to smoothly transition

#         # Determine which phase applies
#         in_phase1 = earned_income <= phase_in_threshold
#         in_phase2 = (earned_income > phase_in_threshold) & (earned_income <= flat_end)
#         in_phase3 = earned_income > flat_end

#         # For phase 3, we need to think about how to transition
#         # At £4000, UC should be £3600 - £4000 = -£400, but UC can't be negative
#         # So let's make it 0 and then use normal UC taper logic

#         uc_at_flat_end = max_(0, flat_household_income - flat_end)  # = max(0, -400) = 0

#         # If UC hits 0 at the end of phase 2, then for phase 3 we can either:
#         # 1. Keep it at 0, or
#         # 2. Use normal standard allowance but with income reduction

#         # Option 1: Keep UC at 0 for high earners (simpler)
#         phase3_allowance = 0

#         # Calculate the allowance based on phase
#         modified_allowance = (
#             in_phase1 * phase1_allowance
#             + in_phase2 * phase2_allowance
#             + in_phase3 * phase3_allowance
#         )

#         # Ensure allowance is never negative
#         return max_(0, modified_allowance)


# class uc_child_element(Variable):
#     value_type = float
#     entity = BenUnit
#     label = "Universal Credit child element (with phase-in)"
#     documentation = "UC child element enhanced with phase-in policy"
#     definition_period = YEAR
#     unit = GBP

#     def formula(benunit, period, parameters):
#         # Get the standard UC child element calculation first
#         try:
#             num_children = benunit("benunit_count_children", period)
#             p = parameters(period).gov.dwp.universal_credit.elements.child
#             child_limit = parameters(
#                 period
#             ).gov.dwp.universal_credit.elements.child.limit
#             eligible_children = min_(num_children, child_limit)
#             standard_child_element = eligible_children * p.amount * MONTHS_IN_YEAR
#         except:
#             num_children = benunit("benunit_count_children", period)
#             standard_child_element = (
#                 num_children * 3235
#             )  # Approximate annual child element

#         # Get employment income for phase-in logic
#         employment_income = benunit("employment_income", period)

#         # Phase-in parameters
#         phase_in_threshold = 3000.0  # End of phase 1
#         flat_end = 5000.0  # End of phase 2 (flat section)

#         # Phase 1: 0 to £3000 - add 0.2 * employment_income
#         phase1_addition = 0.2 * employment_income
#         phase1_total = standard_child_element + phase1_addition

#         # Phase 2: £3000 to £4000 - flat (keep the same addition as at £3000)
#         phase2_addition = 0.2 * phase_in_threshold  # = 0.2 * 3000 = £600
#         phase2_total = standard_child_element + phase2_addition

#         # Phase 3: £4000+ - back to standard
#         phase3_total = standard_child_element

#         # Fixed logic: check the right thresholds
#         result = where(
#             employment_income <= phase_in_threshold,
#             phase1_total,  # Phase 1: 0 to £3000
#             where(
#                 employment_income <= flat_end,  # ← Fixed: now checks flat_end
#                 phase2_total,  # Phase 2: £3000 to £4000 (flat)
#                 phase3_total,  # Phase 3: £4000+
#             ),
#         )

#         # Only apply if there are children
#         has_children = num_children > 0
#         final_result = where(has_children, result, standard_child_element)

#         return max_(0, final_result)


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


class reform(Reform):
    def apply(self):
        if "uc_phase_in_addition" not in self.variables:
            self.add_variable(uc_phase_in_addition)
        self.update_variable(uc_child_element)
