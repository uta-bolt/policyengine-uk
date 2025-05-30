from policyengine_uk.model_api import *


class uc_30hr_bonus(Variable):
    value_type = float
    entity = BenUnit
    label = "Bonus for reaching 30 hours of work for HH with children"
    definition_period = YEAR
    unit = GBP

    def formula(benunit, period, parameters):
        has_child = benunit.any(benunit.members("age", period) < 16)
        threshold = 30.00 * 12.21 * 52  # About £19,092
        earned_income = benunit("uc_earned_income", period)

        # Get baseline to check if they actually receive UC
        baseline = benunit.simulation.get_branch("baseline", clone_system=True)
        received_uc = (
            baseline.calculate("universal_credit", period, map_to="benunit") > 0
        )
        amount = 1069
        base_year = "2026-01-01"  # Base year for the £1069 amount
        base_cpi = parameters.gov.benefit_uprating_cpi(base_year)
        current_cpi = parameters.gov.benefit_uprating_cpi(period)
        uprated_amount = amount * (current_cpi / base_cpi)
        print(uprated_amount)
        bonus = np.where(
            (earned_income > threshold) & has_child & received_uc, uprated_amount, 0
        )

        # Only give bonus to households that:
        # 1. Have children under 16
        # 2. Earn above threshold
        # 3. Actually receive UC

        return bonus


# Modify universal credit to include the bonus
class universal_credit(Variable):
    value_type = float
    entity = BenUnit
    label = "Universal Credit (with 30hr bonus)"
    definition_period = YEAR
    unit = GBP

    def formula(benunit, period):
        # Create a baseline branch to access the original universal_credit value
        baseline = benunit.simulation.get_branch("baseline", clone_system=True)
        base = baseline.calculate("universal_credit", period, map_to="benunit")
        bonus = benunit("uc_30hr_bonus", period)

        return base + bonus


# Export this as `reform`
class reform(Reform):
    def apply(self):
        if "uc_30hr_bonus" not in self.variables:
            self.add_variable(uc_30hr_bonus)
        self.update_variable(universal_credit)
