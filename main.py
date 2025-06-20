import sys
import threading

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from enums import URLs

from src.sites.food import Food
from src.sites.pinch_of_yum import PinchOfYum
from src.sites.recipe_tin_eats import RecipeTinEats

from src.interface.recipe_app import RecipeApp


if __name__ == '__main__':

    # Create scraper instances
    scraperRTE = RecipeTinEats(
        url=URLs.RECIPE_TIN_EATS.value,
        output_dir=URLs.RTE_OUTPUT_DIR.value
    )
    scraperPOY = PinchOfYum(
        url=URLs.PINCH_OF_YUM.value,
        output_dir=URLs.POY_OUTPUT_DIR.value
    )
    # scraperFOOD = Food(
    #     url=URLs.FOOD.value,
    #     output_dir=URLs.FOOD_OUTPUT_DIR.value
    # )

    # Create threads for each scraper
    thread_rte = threading.Thread(target=scraperRTE.run)
    thread_poy = threading.Thread(target=scraperPOY.run)
    # thread_food = threading.Thread(target=scraperFOOD.run)

    # Start all threads
    thread_rte.start()
    thread_poy.start()
    # thread_food.start()

    # Wait for all threads to complete
    thread_rte.join()
    thread_poy.join()
    # thread_food.join()

    app = QApplication(sys.argv)
    
    # Configurar fonte padrão da aplicação
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = RecipeApp()
    window.show()
    
    sys.exit(app.exec_())
