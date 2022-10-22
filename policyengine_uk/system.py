from pathlib import Path
from policyengine_uk.entities import entities
from policyengine_core.taxbenefitsystems import TaxBenefitSystem
from policyengine_core.simulations import (
    Simulation as CoreSimulation,
    Microsimulation as CoreMicrosimulation,
    IndividualSim as CoreIndividualSim,
)
from policyengine_uk.data.datasets.frs.enhanced.stages.imputation.enhanced_frs import (
    EnhancedFRS,
)
from policyengine_uk.parameters.gov.ofgem.price_cap.add_price_cap_parameters import (
    add_price_cap_parameters,
)

COUNTRY_DIR = Path(__file__).parent


class CountryTaxBenefitSystem(TaxBenefitSystem):
    parameters_dir = COUNTRY_DIR / "parameters"
    variables_dir = COUNTRY_DIR / "variables"
    auto_carry_over_input_variables = True

    def __init__(self):
        super().__init__(entities)

        self.parameters = add_price_cap_parameters(
            self.parameters,
            start_year=2019,
            start_quarter=1,
            end_year=2027,
            end_quarter=4,
        )

        self.parameters.add_child("baseline", self.parameters.clone())


system = CountryTaxBenefitSystem()

parameters = system.parameters
variables = system.variables


class Simulation(CoreSimulation):
    default_tax_benefit_system = CountryTaxBenefitSystem
    default_tax_benefit_system_instance = system
    default_calculation_period = 2022
    default_input_period = 2022


class Microsimulation(CoreMicrosimulation):
    default_tax_benefit_system = CountryTaxBenefitSystem
    default_tax_benefit_system_instance = system
    default_dataset = EnhancedFRS
    default_dataset_year = 2022
    default_calculation_period = 2022
    default_input_period = 2022


class IndividualSim(CoreIndividualSim):  # Deprecated
    tax_benefit_system = CountryTaxBenefitSystem
    entities = {entity.key: entity for entity in entities}
    default_dataset = EnhancedFRS
    required_entities = None


BASELINE_VARIABLES = {
    variable.name: variable for variable in system.variables.values()
}
