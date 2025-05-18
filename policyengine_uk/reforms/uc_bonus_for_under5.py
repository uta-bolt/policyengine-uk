from policyengine_uk.model_api import *

# # Define bonus variable
# class uc_child_element_bonus_under_5(Variable):
#     value_type = float
#     entity = BenUnit
#     label = "UC bonus for children under 5"
#     definition_period = MONTH
#     unit = GBP

#     def formula(benunit, period):
#         is_under_5 = benunit.any(benunit.members("age", period) < 5)
#         return is_under_5 * 100.0
class uc_child_element_bonus_under_5(Variable):
    value_type = float
    entity = BenUnit
    label = "UC child element bonus for under 5s"
    definition_period = YEAR
    unit = GBP

    def formula(benunit, period):
        has_under5 = benunit.any(benunit.members("age", period) < 5)
        return 100.0 * has_under5  # 👈 Hardcoded instead of parameter
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
        bonus = benunit("uc_child_element_bonus_under_5", period)
        return base + bonus
    
class num_households_with_under5(Variable):
    value_type = float
    entity = BenUnit
    label = "Number of households with a child under 5"
    definition_period = YEAR
    unit = "count"

    def formula(benunit, period):
        has_under5 = benunit.any(benunit.members("age", period) < 5)
        return has_under5.astype(float)
    
# Export this as `reform`
class reform(Reform):
    def apply(self):
        if "uc_child_element_bonus_under_5" not in self.variables:
            self.add_variable(uc_child_element_bonus_under_5)
        if "num_households_with_under5" not in self.variables:
            self.add_variable(num_households_with_under5)    
        self.update_variable(universal_credit)
