# Random Name Generator

[![codecov](https://codecov.io/gh/diabolical-ninja/RandomNameGenerator/branch/main/graph/badge.svg?token=Q4zU40ENrt)](https://codecov.io/gh/diabolical-ninja/RandomNameGenerator)
[![Linting and Unit Tests](https://github.com/diabolical-ninja/RandomNameGenerator/actions/workflows/hygiene_checks.yml/badge.svg)](https://github.com/diabolical-ninja/RandomNameGenerator/actions/workflows/hygiene_checks.yml)

Simple tool to generate random project or business names using a basic [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain) approach.

## How to Run

Everything is controlled via the configuration file (`config.yml`)

To get started, rename the `config_sample.yml` to `config.yml` and remove the GoDaddy references. Then run the app:
```sh
python generate_names.py
```

### Parameters


| Parameter 	| Type 	| Description 	|
|---	|---	|---	|
| `number_of_names` 	| Integer 	| Number of names to attempt to create 	|
| `maximum_name_length` 	| Integer 	| Maximum name length. Note names can be up to length + largest n-gram in length 	|
| `n_grams` 	| List of integers 	| The word segment lengths to consider for learning and generating new words. 	|
| `extensions` 	| List of strings 	| Domain extensions to check for such as `.com`, `.ai`, etc 	|
| `training_words` 	| List of strings 	| Words to learn from and used to generate new, random, words 	|


### Domain Name Lookup
If you'd like to check if the domain name (eg `www.randomname.com`) is available for the generated names then you'll also need a GoDaddy API key. This can be generated at the following: https://developer.godaddy.com/keys



## Testing

[Nox](https://nox.thea.codes/en/stable/) is used handle test automation. To run the tests:

1. Register with GoDaddy and generate OTE & PROD keys
2. Set them as environment variables:
```sh
# GoDaddy OTE
GODADDY_OTE_KEY=<OTE Key>
GODADDY_OTE_SECRET=<OTE Secret>

# GoDaddy Prod
GODADDY_PROD_KEY=<Prod Key>
GODADDY_PROD_SECRET=<Prod Secret>
```
3. Install [nox](https://nox.thea.codes/en/stable/) if not already available 
4. Run the tests:
```sh
nox
```