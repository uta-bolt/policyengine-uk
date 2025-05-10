from policyengine_uk import Simulation
from policyengine_core.model_api import *

situation = {
    "people": {
        "person": {
            "age": {2025: 30},
            "employment_income": {2025: 30_000},
        },
    },
    "benunits": {
        "benunit": {
            "members": ["person"],
        },
    },
    "households": {
        "household": {
            "members": ["person"],
        }
    },
}

simulation = Simulation(situation=situation)

simulation.calculate("income_tax", 2025)



increase_basic_rate = {"gov.hmrc.income_tax.rates.uk[0].rate": 0.25}


baseline = Simulation(situation=situation)
reformed = Simulation(situation=situation, reform=increase_basic_rate)

baseline_income_tax = baseline.calculate("income_tax", 2025)[0]
reformed_income_tax = reformed.calculate("income_tax", 2025)[0]

print(
    f"Raising the basic rate to 25% would increase this person's income tax by £{reformed_income_tax - baseline_income_tax:.2f}"
)
