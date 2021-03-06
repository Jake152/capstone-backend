import unittest

from neomodel import db, config, DoesNotExist

from backend import settings
from routing.models.location import Address


class MyTestCase(unittest.TestCase):
    config.DATABASE_URL = settings.NEOMODEL_NEO4J_BOLT_URL
    db.set_connection(url=config.DATABASE_URL)

    def test_constructor(self):
        street = '9029 Burt St'
        city = 'Omaha'
        state = 'NE'
        zipcode = 68114
        address = Address(address=street, city=city, state=state, zipcode=zipcode).save()
        self.assertEqual(address.address, street)
        self.assertEqual(address.city, city)
        self.assertEqual(address.state, state)
        self.assertEqual(address.zipcode, zipcode)
        self.assertIsNone(address.latitude)
        self.assertIsNone(address.longitude)
        with self.assertRaises(DoesNotExist):
            address.neighbor.get()
        address.delete()

    def test_str(self):
        street = '9029 Burt St'
        city = 'Omaha'
        state = 'NE'
        zipcode = 68114
        address = Address(address=street, city=city, state=state, zipcode=zipcode).save()
        expected = '{address}, {city}, {state} {zipcode}'.format(address=street, city=city, state=state,
                                                                 zipcode=zipcode)
        self.assertEqual(str(address), expected)
        address.delete()

    def test_distance_value_error(self):
        address = Address(address='6001 Dodge St', city='Omaha', state='NE', zipcode=68182).save()
        with self.assertRaises(TypeError):
            address.distance(object)
        address.delete()

    def test_duration_value_error(self):
        address = Address(address='6001 Dodge St', city='Omaha', state='NE', zipcode=68182).save()
        with self.assertRaises(TypeError):
            address.duration(object)
        address.delete()

    def test_distance_same_address(self):
        address = Address(address='6001 Dodge St', city='Omaha', state='NE', zipcode=68182).save()
        self.assertEqual(address.distance(address), 0)
        address.delete()

    def test_duration_same_address(self):
        address = Address(address='6001 Dodge St', city='Omaha', state='NE', zipcode=68182).save()
        self.assertEqual(address.duration(address), 0)
        address.delete()

    def test_distance_different_addresses(self):
        uno = Address(address='6001 Dodge St', city='Omaha', state='NE', zipcode=68182).save()
        creighton = Address(address='602 N. 20th St', city='Omaha', state='NE', zipcode=68178).save()
        expected_distance = 7.27
        expected_duration = 14.1

        self.assertEqual(uno.distance(creighton), expected_distance)
        self.assertEqual(uno.duration(creighton), expected_duration)
        uno.delete()
        creighton.delete()


if __name__ == '__main__':
    unittest.main()
