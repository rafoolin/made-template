
# Association between newly registered cars and Greenhouse gas[^r1] emissions in the EU

## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![CI/CD](https://github.com/rafoolin/made-template/actions/workflows/pipeline.yml/badge.svg)](https://github.com/rafoolin/made-template/actions/workflows/pipeline.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

## Introduction

![cars](./git_resources/pic.jpg)

Greenhouse gas emissions from transport account for 25% of the total EU greenhouse gas emissions. In order to achieve climate neutrality by 2050, as specified in the European Green Deal, there is a target to reduce greenhouse gas emissions from the transport sector by 90%. [^r2]

In this report, the primary objective is to explore the correlation between automobile choices and $CO_2$ emissions. This report aims to examine the impact of selecting one type of car over another on $CO_2$ emissions and its consequent effects on various aspects of life. The objective is to comprehend how individuals' choices of car fuel contribute to the quantity of $CO_2$ emissions.

## Documentation

There is a [Wiki](https://github.com/rafoolin/made-template/wiki) for some exercises and project's works.

## Jupyter notebook report

A Jupyter notebook report titled [report.ipynb](https://github.com/rafoolin/made-template/blob/main/project/report.ipynb) is available in the `project` directory. This report systematically details the data sources employed and outlines the Extract, Transform, Load (ETL) processes utilized to investigate the primary question. The objective is to identify any potential correlations between the carbon dioxide ($CO_2$) emissions and the motor engine types of recently registered cars in Europe.

There is also a pipeline in the `project` directory. This pipeline downloads data sources, performs cleaning and transformation tasks, and subsequently generates a new SQL dataset tailored to the specific requirements of the project. To run the pipeline locally and generate the SQL file, follow the next step.

## Run Pipeline Locally

Clone the project

```bash
  git clone git@github.com:rafoolin/made-template.git
```

Go to the project directory

```bash
  cd made-template
```

Run the bash script `project/pipeline.sh`

```bash
  bash project/pipeline.sh
```

This will start a virtual environment and finally create a SQL database in `\data` directory.

## Running Tests

To run tests, run the following command

```bash
  bash project/tests.sh
```

## Future work

It is recommended to explore data sources that provide in-depth details about cars, like open data from factories sharing their greenhouse gas (GHG) emissions during production. The impact on the environment goes beyond just using the car, and it's crucial to look at the whole life cycle. For example, if making electric cars produces a lot of GHG emissions, that's an important factor to think of. So, including data from the manufacturing phase is really important to get a complete picture of how different types of motors affect the environment.
A comparative analysis allows for understanding tradeoffs between different motor types. If one type of vehicle has higher manufacturing emissions but significantly lower operational emissions, it's important to weigh these factors when considering the overall environmental impact.

To gain a comprehensive understanding of how one type of motor energy impacts greenhouse gas (GHG) emissions compared to another, it is advisable to incorporate additional data sources. For instance, analyzing data on the age of newly registered cars could provide valuable insights into how emissions evolve over time.
Understanding how GHG emissions change as vehicles age can inform policy decisions. For example, it can help policymakers assess the effectiveness of emissions standards and regulations over the lifespan of a vehicle.

In Germany, there is available open data on the car market, providing access to information about new cars in the market that potential buyers may consider. Utilizing the data from these sources, models can be developed to train for $CO_2$ emissions. Users can then choose specific parameters for their preferred car, enabling them to compare and make informed decisions based on $CO_2$ emissions. This approach allows users to comprehend the environmental impact, illustrating how each selected car contributes a specific amount of $CO_2$ emissions per kilometer, empowering them to make environmentally conscious decisions.

## Limitations

Since 2021, the emissions are measured with a new test procedure (Worldwide harmonized Light vehicles Test Procedure WLTP), compared to the New European Driving Cycle (NEDC) procedure used until 2020. The WLTP aims to reflect better real driving conditions and WLTP values are systematically higher than NEDC values. This change leads to a break in time series between 2020 and 2021. $^5$

The $CO_2$ emission data lacks information for the year 2023, and significant fluctuations occurred from 2019 to 2021, primarily attributed to the COVID-19 situation.

There are some missing data for years prior to 2017 for some motor types.

## Contributing

Contributions are always welcome!
To explore potential areas for future work related to this project, please refer to the [future-work](#future-work) section.

## Feedback

If you have any feedback, please reach out to me at niloo.jv@gmail.com

## Licenses

Photo by <a href="https://unsplash.com/@so666max?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Max Zhang</a> on <a href="https://unsplash.com/photos/cars-on-road-near-city-buildings-during-daytime-jnmDblTq1uk?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
  
[^r1]: Only $CO2$ is considered among all the other greenhouse gases in this report.

[^r2]: EC, 2021, Communication from the Commission to the European Parliament, the Council, the European Economic and Social Committee and the Committee of the Regions ‘Fit for 55’: delivering the EU’s 2030 Climate Target on the way to climate neutrality, COM(2021) 550 final
