# Marko-Namo


![PyPi Version](https://img.shields.io/pypi/v/marko-namo)
![Python Versions](https://img.shields.io/pypi/pyversions/marko-namo)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
<br/>

[![Code Hygiene](https://github.com/diabolical-ninja/Marko-Namo/actions/workflows/code_hygiene.yml/badge.svg)](https://github.com/diabolical-ninja/Marko-Namo/actions/workflows/code_hygiene.yml)
[![codecov](https://codecov.io/gh/diabolical-ninja/Marko-Namo/branch/main/graph/badge.svg?token=Q4zU40ENrt)](https://codecov.io/gh/diabolical-ninja/Marko-Namo)
![black codestyle](https://img.shields.io/badge/Code%20Style-Black-black)
<br/>

[![Documentation Status](https://readthedocs.org/projects/marko-namo/badge/?version=latest)](https://marko-namo.readthedocs.io/en/latest/?badge=latest)

<br/>


Simple tool to generate random project or business names using a basic [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain) approach.


## Installation

Install `marko-namo` from the Python Package Index:

```console
$ pip install marko-namo
```

## Requirements

- Python 3.8+


## How It Words

The generator starts by creating a frequency table based on the training words supplied and the n-grams listed. Eg if our training word is `hello` and our n-grams are 1 and 2, we'd get a frequency table of:
```json
{
    "h": ["e", "el"],
    "he": ["l", "ll"],
    "e": ["l", "ll"],
    "el": ["l", "lo"],
    "l": ["l", "lo", "o", null],
    "ll": ["o", null],
    "lo": [null, null],
    "o": [null, null]
}
```

It then randomly selects an n-gram from the frequency table as the first letter, randomly selects a following letter and repeats until the word either ends (selects a `None`) or reaches the maximum word length.

Eg if the first selected letter was `e` we might go:
- `e` -> `l` -> `lo` -> None
- Which gives `ello`


## How To Run

You can either create a config file and pass that in or specifiy your parameters in code. To get started, you can utilse the `config_sample.yml`.

```python
from marko_namo import MarkoNamo

random_name_generator = MarkoNamo("config_sample.yml")
created_names, available_domains = random_name_generator.create_random_names()
```

If you'd rather not use a config file then you can run:
```python
from marko_namo import MarkoNamo

random_name_generator = MarkoNamo(
    name_length = 5,
    number_of_names = 10,
    training_words = ["hello", "pineapple", "planet"]
)
created_names, available_domains = random_name_generator.create_random_names()

```

### Parameters

| Parameter 	| Type 	| Description 	|
|---	|---	|---	|
| `number_of_names` 	| Integer 	| Number of names to attempt to create 	|
| `maximum_name_length` 	| Integer 	| Maximum name length. Note names can be up to length + largest n-gram in length 	|
| `n_grams` 	| List of integers 	| The word segment lengths to consider for learning and generating new words. 	|
| `extensions` 	| List of strings 	| Domain extensions to check for such as `.com`, `.ai`, etc 	|
| `training_words` 	| List of strings 	| Words to learn from and used to generate new, random, words.  There's no limit to the number of words to learn from but too many will slow the program down significantly. 	|


### Domain Name Lookup
If you'd like to check if the domain name (eg `www.randomname.com`) is available for the generated names then you'll also need a GoDaddy API key. This can be generated at the following: https://developer.godaddy.com/keys

You'll need to provide:
- API Key
- API Secret
- Whether you'd like to use their OTE (test) or PROD (production) environment


## Building the Project

This package uses `poetry` and `nox` for package management and building. 

If nox is not already installed, install it:
```console
$ pip install nox
$ pip install nox_poetry
```

Run everything including tests and documentation building
```console
$ nox

# Or to run a specific stage:
$ nox -s <stage name>, eg
$ nox -s tests
```

## Testing

Nox also handles the tests but you'll require OTE & PROD keys to run the GoDaddy tests.

1. Register with GoDaddy and generate OTE & PROD keys
2. Set them as environment variables:
```sh
# GoDaddy OTE
GODADDY_OTE_KEY=<OTE Key>
GODADDY_OTE_SECRET=<OTE Secret>
GODADDY_OTE_ENV=OTE

# GoDaddy Prod
GODADDY_PROD_KEY=<Prod Key>
GODADDY_PROD_SECRET=<Prod Secret>
GODADDY_PROD_ENV=PROD
```

3. Run the tests:
```console
$ nox -s tests
```

## Issues

If you encounter any problems, please [file an issue](https://github.com/diabolical-ninja/Marko-Namo/issues) along with a detailed description.
