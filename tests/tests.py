from operator import itemgetter
from unittest import TestCase

import simpleldap


class LDAPItemTests(TestCase):

    mock_results = [
        ('uid=joe,ou=people,dc=directory,dc=example,dc=com',
            {'cn': ['Joseph Smith', 'Joseph Smith Jr.'],
             'givenName': ['Joseph'],
             'sn': ['Smith'],
             'displayName': ['Joe L. Smith', 'Joe Smith'],
            }),
        ('uid=bob,ou=people,dc=directory,dc=example,dc=com',
            {'cn': ['Robert West', 'Robert T. West'],
             'givenName': ['Robert'],
             'sn': ['West'],
             'displayName': ['Bob West'],
            }),
    ]

    def test_dn(self):
        item = simpleldap.LDAPItem(self.mock_results[0])
        self.assertEqual(item.dn,
                         'uid=joe,ou=people,dc=directory,dc=example,dc=com')

    def test_str(self):
        item = simpleldap.LDAPItem(self.mock_results[0])
        self.assertEqual(str(item), """\
         cn: Joseph Smith
             Joseph Smith Jr.
displayName: Joe L. Smith
             Joe Smith
  givenName: Joseph
         sn: Smith""")

    def test_item_lookup(self):
        item = simpleldap.LDAPItem(self.mock_results[0])
        self.assertEqual(item['cn'], ['Joseph Smith', 'Joseph Smith Jr.'])
        self.assertRaises(KeyError, itemgetter('foo'), item)

    def test_first_lookup(self):
        item = simpleldap.LDAPItem(self.mock_results[0])
        self.assertEqual(item.first('cn'), 'Joseph Smith')
        self.assertEqual(item.first('sn'), 'Smith')
        self.assertRaises(KeyError, item.first, 'foo')
