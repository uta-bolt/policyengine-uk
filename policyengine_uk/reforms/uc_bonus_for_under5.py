from policyengine_uk.model_api import *
from policyengine_core.reforms.reform import Reform
class uc_child_element_bonus_under_5(Variable):
    value_type = float
    entity = BenUnit
    label = "UC child element bonus for children under 5"
    definition_period = MONTH
    unit = GBP

    def formula(benunit, period):
        is_under_5 = benunit.sum(benunit.members("age", period) < 5)
        print("👶 Number of children under 5:", is_under_5)
        return is_under_5 * 100


class modified_universal_credit(Variable):
    value_type = float
    entity = BenUnit
    label = "Universal Credit with under-5 bonus"
    definition_period = MONTH
    unit = GBP

    def formula(benunit, period):
        base = benunit("universal_credit", period, reform="baseline")
        bonus = benunit("uc_child_element_bonus_under_5", period)
        print("💸 Base UC:", base)
        print("🎁 Bonus UC:", bonus)
        return base + bonus


class AddUCChildUnder5Bonus(Reform):
    def apply(self):
        #self.add_variable(uc_child_element_bonus_under_5)
        self.update_variable(modified_universal_credit, name="universal_credit")