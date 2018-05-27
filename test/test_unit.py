import os
import unittest

from flask import json
from flask_testing import TestCase

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class OrderingTestCase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        return app

    # Creamos la base de datos de test
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    # Destruimos la base de datos de test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"

    def test_crear_producto(self):
        data = {
            'name': 'Tenedor',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Falló el POST")
        p = Product.query.all()

        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")

    def test_crear_producto_cantidad_no_negativa_(self):
        prod = Product(id = 5, name = 'sillon', price = 8000)
        order = Order(id = 1)
        op = OrderProduct(order_id = 1, product_id = 5, product = prod, quantity = -2)    

        db.session.add(prod)
        db.session.add(order)
        db.session.add(op)
        db.session.commit()

        self.assertNotIn(op,db.session,"Se crea instancia de OrderProduct con producto de cantidad negativa") 

    def test_GET_method_in_orderProduct(self):
        prod = Product(id = 5, name = 'sillon', price = 8000)
        order = Order(id = 1)
        op = OrderProduct(order_id = 1, product_id = 5, product = prod, quantity = 1)

        db.session.add(prod)
        db.session.add(order)
        db.session.add(op)
        db.session.commit()

        result_GET = self.client.get('/order/1/product/5', content_type='aplication/json')

        self.assertEqual(result_GET.status, "200 OK", "Falló el GET")

    def test_GET_method_in_order(self):
        order = Order(id = 2)

        db.session.add(order)
        db.session.commit()

        result_GET = self.client.get('/order/2', content_type='aplication/json')

        self.assertEqual(result_GET.status, "200 OK", "Falló el GET")


if __name__ == '__main__':
    unittest.main()

