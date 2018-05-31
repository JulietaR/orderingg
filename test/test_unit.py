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

    def test_crear_producto_cantidad_no_negativa(self):
        prod = Product(id = 5, name = 'sillon', price = 8000)
        order = Order(id = 1)
        op = OrderProduct(order_id = 1, product_id = 5, product = prod, quantity = -2)    

        db.session.add(prod)
        db.session.add(order)
        db.session.add(op)
        db.session.commit()

        ops = db.session.query(OrderProduct).all()

        self.assertNotIn(op, ops, "Se crea instancia de OrderProduct con producto de cantidad negativa") 

    def test_GET_method_in_orderProduct(self):
        prod = Product(id = 5, name = 'sillon', price = 8000)
        order = Order(id = 1)
        op = OrderProduct(order_id = 1, product_id = 5, product = prod, quantity = 1)

        db.session.add(prod)
        db.session.add(order)
        db.session.add(op)
        db.session.commit()

        result_GET = self.client.get('/order/1/product/5', content_type='aplication/json')
        data = json.loads(result_GET.data)

        self.assertEqual(result_GET.status, "200 OK", "Falló el GET")
        self.assertEqual(data['id'], prod.id, "Falló el GET")

    def test_GET_method_in_order(self):
        order = Order(id = 2)

        db.session.add(order)
        db.session.commit()

        result_GET = self.client.get('/order/2', content_type='aplication/json')
        data = json.loads(result_GET.data)

        self.assertEqual(result_GET.status, "200 OK", "Falló el GET")
        self.assertEqual(data['id'], order.id, "Falló el GET")        

    def test_DELETE_method_in_orderProduct(self):
        prod = Product(id = 6, name = 'Escritorio', price = 15000)
        order = Order(id = 3)
        op = OrderProduct(order_id = 3, product_id = 6, product = prod, quantity = 1)

        db.session.add(prod)
        db.session.add(order)
        db.session.add(op)
        db.session.commit()

        result_DELETE = self.client.delete('/order/3/product/6', content_type='aplication/json')
        result_GET = self.client.get('/order/3', content_type='aplication/json')
        data = json.loads(result_GET.data)

        self.assertEqual(result_DELETE.status, "200 OK", "Falló el DELETE")    
        self.assertEqual(data['products'], [], "Falló el DELETE")        

    def test_modificar_producto(self):
        pk_order = 1
        pk_product = 1

        data = {
            'quantity': 5,
            'product': {
                'id': 1,
                'name': 'Tenedor',
                'price': 50
            }
        }

        db.session.add(Order(id=pk_order))
        np = Product(id=data['product']['id'], name=data['product']['name'], price=data['product']['price'])
        db.session.add(np)
        db.session.add(OrderProduct(order_id= pk_order, product_id= pk_product, quantity= data['quantity'], product= np))
        db.session.commit()

        self.client.put('order/' + str(pk_order) + '/product/' + str(pk_product), data=json.dumps(data), content_type='application/json')
        
        ordprod = pk_order, pk_product
        p = OrderProduct.query.get(ordprod)
        self.assertEqual(p.quantity, data['quantity'], 'Quantity should be equal')

    def test_totalPrice(self):
        pk_order = 1

        o = Order(id=pk_order)
        db.session.add(o)
        p1 = Product(id=1, name="tenedor", price="5")
        p2 = Product(id=2, name="notebook", price="100")
        q1 = 2
        q2 = 1
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(OrderProduct(order_id= pk_order, product_id= 1, quantity= q1, product= p1))
        db.session.add(OrderProduct(order_id= pk_order, product_id= 2, quantity= q2, product= p2))
        db.session.commit()

        total = p1.price*q1 + p2.price*q2

        self.assertEqual(total, o.orderPrice, "Price should be equal")

    def test_crear_producto_string_no_vacio(self):
        prod = Product(id=1, name='l', price=10)
        db.session.add(prod)
        db.session.commit()

        p = Product.query.all()[0]

        self.assertFalse(p.name=="", "El nombre no debe estar vacío")


if __name__ == '__main__':
    unittest.main()

