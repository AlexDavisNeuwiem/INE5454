from enum import Enum

class URLs(Enum):
    PINCH_OF_YUM = "https://pinchofyum.com/recipes/all"
    POY_OUTPUT_DIR = "src/dados/pinch_of_yum/"

    RECIPE_TIN_EATS = "https://www.recipetineats.com/recipes/?fwp_paged=1"
    RTE_OUTPUT_DIR = "src/dados/recipe_tin_eats/"

    FOOD = "https://www.food.com/recipe?ref=nav" # Adicionar &pn=2 em diante
    FOOD_OUTPUT_DIR = "src/dados/food/"
