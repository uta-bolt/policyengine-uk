from policyengine_uk.model_api import *


class uc_30hr_bonus(Variable):
    value_type = float
    entity = BenUnit
    label = "Bonus for reaching 30 hours of work for HH with children"
    definition_period = YEAR
    unit = GBP

    def formula(benunit, period, parameters):
        has_child = benunit.any(benunit.members("age", period) < 16)
        threshold = 30.00 * 12.21 * 52
        earned_income = benunit("uc_earned_income", period)
        print(f"Threshold: £{threshold}")
        print(f"Max earned income: £{np.max(earned_income)}")
        print(f"Households with children: {np.sum(has_child)}")
        print(f"Households above threshold: {np.sum(earned_income > threshold)}")
        print(
            f"Households with children above threshold: {np.sum((earned_income > threshold) & has_child)}"
        )

        if earned_income > threshold:
            bonus = 1069 * has_child
        else:
            bonus = 0
        return bonus


# Modify universal credit to include the bonus
class universal_credit(Variable):
    value_type = float
    entity = BenUnit
    label = "Universal Credit (with child under 5 bonus)"
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
