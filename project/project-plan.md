# Project Plan

## Title
<!-- Give your project a short title. -->
Correlation analysis between newly registered cars and Greenhouse gas emissions in the Europe.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
Is the type of car engine a significant factor contributing to climate change? What other vehicle features play a crucial role in influencing it?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
*Greenhouse gas emissions from transport account for 25% of the total EU greenhouse gas emissions. In order to achieve climate neutrality by 2050, as specified in the European Green Deal, there is a target to reduce greenhouse gas emissions from the transport sector by 90%.*[^r1]

The goal is to explore the latest Passenger cars[^r2], with a particular focus on engine-related features. We can further refine our research by focusing on specific regions to determine if the same pattern emerges. Depending on the results, we can then consider exploring more databases to enhance our analysis if we find the correlation we are seeking.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1:  Europa(Average CO2 emissions per km from new passenger cars)

* Metadata URL: <https://ec.europa.eu/eurostat/cache/metadata/en/sdg_12_30_esmsip2.htm>
* Data URL: <https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/sdg_12_30/?format=SDMX-CSV&compressed=true>
* Data Type: CSV

The indicator is defined as the average carbon dioxide (CO2) emissions per km by new passenger cars in a given year. The reported emissions are based on type-approval and can deviate from the actual CO2 emissions of new cars. Since 2021, the emissions are measured with a new test procedure (Worldwide harmonized Light vehicles Test Procedure WLTP), compared to the New European Driving Cycle (NEDC) procedure used until 2020. The WLTP aims to reflect better real driving conditions and WLTP values are systematically higher than NEDC values. This change leads to a break in time series between 2020 and 2021.

### Datasource2:  Europa(New passenger cars by type of motor energy)

* Metadata URL: <https://ec.europa.eu/eurostat/cache/metadata/en/rail_if_esms.htm>
* Data URL: <https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/road_eqr_carpda/?format=SDMX-CSV&compressed=true>
* Data Type: CSV

The data in this dataset comes from the Common Questionnaire for Transport Statistics, developed and surveyed by Eurostat in cooperation between the United Nations Economic Commission for Europe (UNECE) and the International Transport Forum (ITF) at OECD.

### Side data sources: Europa

These data sources are abbreviation used in the other data sources.

* Data Code list URL: <https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/GEO/?compressed=true&format=TSV&lang=en>
* Data Type: TSV
* Unit Abbr URL: <https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/UNIT/?compressed=true&format=TSV&lang=en>
* Data Type: TSV
* Motor Energy Abbr URL: <https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/MOT_NRG/?compressed=true&format=TSV&lang=en>
* Data Type: TSV

## WIKI

Here is the link to wiki for the projects or exercises if they need more explanation.

* [Week-03][l1]
* [Week-04][l2]
* [Week-06][l3]

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

### Project Work 02

* [Project needs at least two open data source][i2]
* [Project can cover next exercises][i3]
* [Write the project plan][i4]

### Project Work 03

* [Create pipeline for project][i5]
* [Update project-plan.md for Project Work 03][i6]

### Project Work 04

* [Write test for pipeline][i7]

### Project Work 05

* [Create a workflow using GitHub actions][i8]

### Project Work 06

* [Final report][i9]

* [Update final ETL database to meet the requirements][i10]

[i2]: https://github.com/rafoolin/made-template/issues/2
[i3]: https://github.com/rafoolin/made-template/issues/3
[i4]: https://github.com/rafoolin/made-template/issues/4
[i5]: https://github.com/rafoolin/made-template/issues/13
[i6]: https://github.com/rafoolin/made-template/issues/12
[i7]: https://github.com/rafoolin/made-template/issues/18
[i8]: https://github.com/rafoolin/made-template/issues/20
[i9]: https://github.com/rafoolin/made-template/issues/22
[i10]: https://github.com/rafoolin/made-template/issues/23

## References and footnotes

[^r1]: EC, 2021, Communication from the Commission to the European Parliament, the Council, the European Economic and Social Committee and the Committee of the Regions ‘Fit for 55’: delivering the EU’s 2030 Climate Target on the way to climate neutrality, COM(2021) 550 final

[^r2]: [Glossary:Passenger_car](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Passenger_car)

[l1]: https://github.com/rafoolin/made-template/wiki/week_03
[l2]: https://github.com/rafoolin/made-template/wiki/week_04
[l3]: https://github.com/rafoolin/made-template/wiki/week_06
