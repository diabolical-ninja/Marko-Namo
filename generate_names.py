"""Entry point to generate random names. All settings are controlled via config.yml"""

import yaml
from src.go_daddy import GoDaddy
from src.random_name_generator import RandomBusinessName

config = yaml.safe_load(open("config.yml"))

gd = GoDaddy(
    key=config["godaddy-prod"]["key"],
    secret=config["godaddy-prod"]["secret"],
    env="PROD",
)

if __name__ == "__main__":
    rbn = RandomBusinessName(
        name_length=config["parameters"]["maximum_name_length"],
        number_of_names=config["parameters"]["number_of_names"],
        domain_extensions=config["extensions"],
        training_words=config["training_words"],
        n_grams=config["parameters"]["n_grams"],
        godaddy=gd,
    )

    rbn.create_business_name()
