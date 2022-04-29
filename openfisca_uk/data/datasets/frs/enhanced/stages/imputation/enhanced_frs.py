from openfisca_tools.data import Dataset, PrivateDataset
from openfisca_uk.data.datasets.frs.enhanced.utils import add_variables
from openfisca_uk.data.storage import OPENFISCA_UK_MICRODATA_FOLDER
from ..calibration import CalibratedFRS
import h5py
from .lcfs_imputation import impute_consumption
from .was_imputation import impute_wealth


class EnhancedFRS(PrivateDataset):
    name = "enhanced_frs"
    label = "Enhanced FRS"
    data_format = Dataset.TIME_PERIOD_ARRAYS
    folder_path = OPENFISCA_UK_MICRODATA_FOLDER
    filename_by_year = {2022: "enhanced_frs_2022_v0_22.h5"}

    def generate(self, year: int):
        if year not in CalibratedFRS.years:
            ok = input(
                f"Calibrated FRS not found for year {year}. Generate it? (y/n)"
            )
            if ok == "y":
                CalibratedFRS.generate(year)

        # Copy all data from the calibrated FRS

        calibrated_frs = CalibratedFRS.load(year)
        enhanced_frs = h5py.File(self.file(year), mode="w")
        for variable in calibrated_frs.keys():
            for period in calibrated_frs[variable].keys():
                enhanced_frs[f"{variable}/{period}"] = calibrated_frs[
                    variable
                ][period][...]
        calibrated_frs.close()
        enhanced_frs.close()

        pred_consumption = impute_consumption(year, dataset=self)
        add_variables(
            self,
            year,
            {
                f"{field}/{year}": pred_consumption[field]
                for field in pred_consumption.columns
            },
        )

        pred_wealth = impute_wealth(year, dataset=self)
        add_variables(
            self,
            year,
            {
                f"{field}/{year}": pred_wealth[field]
                for field in pred_wealth.columns
            },
        )
        from ..baseline_variables import generate_baseline_variables

        # Import here to avoid circular dependency
        generate_baseline_variables(self, year)

        from ..remove_zero_weight_households import (
            remove_zero_weight_households,
        )

        remove_zero_weight_households(self, year)


EnhancedFRS = EnhancedFRS()
