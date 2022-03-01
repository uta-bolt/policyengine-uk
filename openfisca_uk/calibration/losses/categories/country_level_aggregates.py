from openfisca_uk.calibration.losses.loss_category import LossCategory
import tensorflow as tf
from openfisca_uk import Microsimulation
from typing import Iterable, List, Tuple
from openfisca_uk.parameters import parameters


class CountryLevelAggregates(LossCategory):
    weight = 1
    label = "Country-level aggregates"
    parameter_folder = parameters.calibration.country_level_aggregates

    def get_loss_subcomponents(
        sim: Microsimulation, household_weights: tf.Tensor, year: int
    ) -> Iterable[Tuple]:
        aggregates = CountryLevelAggregates.parameter_folder
        variables = aggregates.children
        hh_country = sim.calc("country").values
        for variable in variables:
            countries = variables[variable].children
            for country in countries:
                parameter = aggregates.children[variable].children[country]
                in_country = hh_country == country
                values = sim.calc(variable, period=year).values
                entity = sim.simulation.tax_benefit_system.variables[
                    variable
                ].entity.key
                household_totals = sim.map_to(values, entity, "household")
                aggregate = tf.reduce_sum(
                    household_weights * in_country * household_totals
                )
                target = parameter(f"{year}-01-01")
                yield parameter.name + "." + str(year), aggregate, target
