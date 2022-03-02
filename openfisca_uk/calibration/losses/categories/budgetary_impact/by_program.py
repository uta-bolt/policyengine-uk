from openfisca_uk.calibration.losses.loss_category import LossCategory
import tensorflow as tf
from openfisca_uk import Microsimulation
from typing import Iterable, List, Tuple
from openfisca_uk.parameters import parameters


class UKProgramAggregates(LossCategory):
    weight = 1
    label = "UK-wide program aggregates"
    parameter_folder = parameters.calibration.program_aggregates

    def get_loss_subcomponents(
        sim: Microsimulation, household_weights: tf.Tensor, year: int
    ) -> Iterable[Tuple]:
        aggregates = UKProgramAggregates.parameter_folder
        variables = aggregates.children
        for variable in variables:
            values = sim.calc(variable, period=year).values
            entity = sim.simulation.tax_benefit_system.variables[
                variable
            ].entity.key
            household_totals = sim.map_to(values, entity, "household")
            # Calculate aggregate error
            agg = tf.reduce_sum(household_weights * household_totals)
            parameter = aggregates.children[variable]
            actual = parameter(f"{year}-01-01")
            yield parameter.name + "." + str(year), agg, actual
