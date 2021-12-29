# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.0] - 2021-12-29

### Added

* Minimum tax credit benefit amount.

## [0.8.1] - 2021-12-29

### Removed

* Benefit unit- and household-level saved random numbers for take-up.

## [0.8.0] - 2021-12-27

### Added

* Historical Working Tax Credit parameters since 2002 (previously since 2016).
* Legislative references for Working Tax Credit parameters.

### Changed

* Working Tax Credit child care parameters represent the maximum amount, prior to the share covered.

### Fixed

* Apply Working Tax Credit old-age provision to 60-year-olds.
* Qualify people working 30 hours for the Working Tax Credit.
* Point AFCS to AFCS_reported instead of AA_reported.
* Fix units on some variables.

## [0.7.17] - 2021-12-23

### Added

* Units for some variables.

### Changed

* Code refactoring.

## 0.4.0 - 2021-07-05

### Added

* Tests for variable naming conventions.
* Postcode lookup optional features available.
* LHA rates for all BRMA areas added.

### Changed

* OpenFisca-UK now runs from the official OpenFisca-Core.

## 0.3.0

### Added

* New interface for microsimulation.
* Sources in tax logic.
* Tests.

### Changed

* Microdata now generated and loaded in-model.
* Variable time periods made more consistent.
* Derivative calculations made more efficient and have more options.

## 0.2.3 - 2021-04-21

### Changed

* MicroDataFrame and MicroSeries returned by default.

### Fixed

* Bugs.

## 0.2.2

### Added

* Jupyter-Book documentation.
* More detailed disability variables.

### Fixed

* IndividualSim reform handling.

## 0.2.1

### Changed

* Improved documentation of parameters.
* Tests now occur in 2021 to ensure FY20-21 parameters are used.

### Fixed

* Bug in CB-HITC that caused overestimation.

## 0.2.0 - 2020-12-05

### Changed

* Time periods now appropriate, using an implementation of WEEK for most benefits.
* MTRs handled properly and include a breakdown.
* Simulation tools are improved and included in a class.

## 0.1.0 - 2020-11-08

### Added

* Income Tax and National Insurance.
* All benefits are at least taken from survey reporting (can be switched on-off).
* Child Benefit is modelled, others such as Income Support, JSA (both types), Tax Credits can be simulated/reformed but require more reviewing in how to account for discrepancies caused by take-up rates.
* Four budget-neutral UBI reforms are implemented.
* 15 test cases (unit and integration) testing benefits and taxes.
* Simulation helper tools.
