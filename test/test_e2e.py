import unittest
import os
import time
import threading

from selenium import webdriver

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

from werkzeug.serving import make_server

class Ordering(unittest.TestCase):
    # Creamos la base de datos de test
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.baseURL = 'http://localhost:5000'

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.t = threading.Thread(target=self.app.run)
        self.t.start()

        time.sleep(1)

        self.driver = webdriver.Chrome()

    def test_title(self):
        driver = self.driver
        driver.get(self.baseURL)
        add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        add_product_button.click()
        modal = driver.find_element_by_id('modal')
        assert modal.is_displayed(), "El modal no esta visible"

    def test_productos_cantidad_negativa(self):
        driver = self.driver
        driver.get(self.baseURL)
        
        agregar = find_element_by_xpath("/html/body/main/div[1]/div/button").click()
        producto = driver.find_element_by_id("select-prod")
        producto.select_by_visible_text("Silla")
        cantidad = driver.find_element_by_id("quantity")
        cantidad.SendKeys('-1')
        send = driver.find_element_by_id("save-button").is_enabled()
        
        self.assertEqual(send, "FALSE", "Se puede ingresar productos negativos a la orden")

    def test_existe_notificacion(self):
        prod = Product(name = 'Silla', price = 500)
        order = Order()
        op = OrderProduct(product = prod, quantity = 1)

        db.session.add(prod)
        db.session.add(order)
        db.session.add(op)
        db.session.commit()


        driver = self.driver
        driver.get(self.baseURL)
        
        agregar = driver.find_element_by_xpath("/html/body/main/div[1]/div/button").click()
        producto = driver.find_element_by_id("select-prod")
        producto.select_by_visible_text("Silla")
        cantidad = driver.find_element_by_id("quantity")
        cantidad.SendKeys('1')
        send = driver.find_element_by_id("save-button").click()
        noti = driver.find_element_by_id("noti").is_displayed()
        
        self.assertEqual(noti, "TRUE", "No aparece la notificación")

    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()

