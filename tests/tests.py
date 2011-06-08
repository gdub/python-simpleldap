from operator import itemgetter
from unittest import TestCase

import simpleldap


class ConnectionTests(TestCase):

    hosts = (
        # host, port, encryption type, require_cert.
        ('ldap.utexas.edu', None, None, None),
        ('ldap.utexas.edu', 389, None, None),
        ('ldap.ucdavis.edu', None, 'tls', False),
        ('ldap.ucdavis.edu', 389, 'tls', False),
        ('ldap.ucdavis.edu', None, 'ssl', False),
        ('ldap.ucdavis.edu', 636, 'ssl', False),
    )

    def test_connect(self):
        for host, port, method, cert in self.hosts:
            try:
                conn = simpleldap.Connection(hostname=host, port=port,
                                             encryption=method, require_cert=cert)
            except Exception, e:
                self.fail("Got error connecting to %s %s %s %s: %s"
                          % (host, port, method, cert, e))
            else:
                conn.close()

    def test_context_manager(self):
        host, port, method, cert = self.hosts[0]
        with simpleldap.Connection(hostname=host, port=port, encryption=method,
                                   require_cert=cert) as conn:
            conn.connection.whoami_s()


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
