from __future__ import with_statement  # Python 2.5 compatibility.
from operator import itemgetter
from unittest import TestCase

import ldap

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
                                             encryption=method,
                                             require_cert=cert)
            except Exception, e:
                self.fail("Got error connecting to %s %s %s %s: %s"
                          % (host, port, method, cert, e))
            else:
                conn.close()

    def test_initialize_kwargs(self):
        from StringIO import StringIO
        output = StringIO()
        initialize_kwargs = {'trace_file': output, 'trace_level': 0}
        conn = simpleldap.Connection('ldap.utexas.edu',
                                     initialize_kwargs=initialize_kwargs)
        conn.close()
        self.assertFalse(output.getvalue())
        initialize_kwargs = {'trace_file': output, 'trace_level': 1}
        conn = simpleldap.Connection('ldap.utexas.edu',
                                     initialize_kwargs=initialize_kwargs)
        conn.close()
        self.assertTrue(output.getvalue())

    def test_context_manager(self):
        host, port, method, cert = self.hosts[0]
        with simpleldap.Connection(hostname=host, port=port, encryption=method,
                                   require_cert=cert) as conn:
            conn.connection.whoami_s()

    def test_invalid_encryption(self):
        self.assertRaises(simpleldap.InvalidEncryptionProtocol,
                          simpleldap.Connection,
                          hostname='ldap.ucdavis.edu', encryption='foo')

    def test_connection_options(self):
        opt = 'OPT_TIMELIMIT'
        value = 1000
        conn = simpleldap.Connection(hostname='ldap.utexas.edu',
                                     options={opt: value},
                                     # No way to really test debug output, but
                                     # thrown in for coverage.
                                     debug=True)
        self.assertEqual(conn.connection.get_option(getattr(ldap, opt)), value)

    def test_search(self):
        conn = simpleldap.Connection('ldap.ucdavis.edu')
        objs = conn.search('cn=*', base_dn='ou=Groups,dc=ucdavis,dc=edu')
        self.assertTrue(len(objs) > 3)
        for obj in objs:
            self.assertTrue(isinstance(obj, conn.result_item_class))

    def test_search_params(self):
        conn = simpleldap.Connection('ldap.ucdavis.edu')
        self.assertRaises(ldap.SIZELIMIT_EXCEEDED, conn.search, 'cn=*',
                          base_dn='ou=Groups,dc=ucdavis,dc=edu', limit=1)
        kwargs = {'filter': 'cn=External Anonymous',
                  'base_dn': 'ou=Groups,dc=ucdavis,dc=edu'}
        # Should return all attrs.
        self.assertTrue(len(conn.search(**kwargs)[0]) > 2)
        # Should return just cn attr.
        obj = conn.search(attrs=['cn'], **kwargs)[0]
        self.assertEqual(len(obj), 1)
        self.assertTrue('cn' in obj)

    def test_search_defaults(self):
        conn = simpleldap.Connection('ldap.ucdavis.edu', search_defaults={'limit': 1})
        conn.set_search_defaults(base_dn='ou=Groups,dc=ucdavis,dc=edu')
        self.assertRaises(ldap.SIZELIMIT_EXCEEDED, conn.search, 'cn=*')
        kwargs = {'filter': 'cn=External Anonymous', }
        conn.clear_search_defaults(['limit'])
        # Should return all attrs.
        self.assertTrue(len(conn.search(**kwargs)[0]) > 2)
        # Should return just cn attr.
        conn.set_search_defaults(attrs=['cn'])
        obj = conn.search(**kwargs)[0]
        self.assertEqual(len(obj), 1)
        self.assertTrue('cn' in obj)
        conn.clear_search_defaults()
        self.assertEqual(conn._search_defaults, {})

    def test_get(self):
        conn = simpleldap.Connection('ldap.ucdavis.edu')
        obj = conn.get('cn=External Anonymous',
                       base_dn='ou=Groups,dc=ucdavis,dc=edu')
        self.assertTrue(isinstance(obj, conn.result_item_class))
        self.assertEqual(obj['cn'], ['External Anonymous'])

        self.assertRaises(simpleldap.ObjectNotFound, conn.get,
                          'cn=Does not exist',
                          base_dn='ou=Groups,dc=ucdavis,dc=edu')
        self.assertRaises(simpleldap.MultipleObjectsFound, conn.get, 'cn=*',
                          base_dn='ou=Groups,dc=ucdavis,dc=edu')

    def test_compare(self):
        conn = simpleldap.Connection('ldap.ucdavis.edu')
        obj = conn.get('cn=External Anonymous',
                       base_dn='ou=Groups,dc=ucdavis,dc=edu')
        self.assertTrue(conn.compare(obj.dn, 'cn', 'External Anonymous'))
        self.assertFalse(conn.compare(obj.dn, 'cn', 'foo'))


class AuthenticateTests(TestCase):

    def test_success(self):
        conn = simpleldap.Connection('ldap.ucdavis.edu')
        self.assertTrue(conn.authenticate('cn=External Anonymous,ou=Groups,dc=ucdavis,dc=edu', ''))

    def test_fail_no_such_object(self):
        conn = simpleldap.Connection('ldap.ucdavis.edu')
        self.assertFalse(conn.authenticate('uid=foobar', 'baz'))

    def test_fail_unwilling_to_perform(self):
        conn = simpleldap.Connection('ldap.utexas.edu')
        self.assertFalse(conn.authenticate('cn=Anonymous', ''))

    def test_fail_invalid_credentials(self):
        conn = simpleldap.Connection('ldap.utexas.edu')
        self.assertFalse(conn.authenticate('uid=foobar', 'baz'))


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

    def test_case_insensitive(self):
        item = simpleldap.LDAPItem(self.mock_results[0])
        self.assertEqual(item['cn'], ['Joseph Smith', 'Joseph Smith Jr.'])
        self.assertEqual(item['cn'], item['CN'])
        self.assertEqual(item.first('cn'), item.first('CN'))
        self.assertTrue('cn' in item)
        self.assertTrue('CN' in item)

    def test_value_contains(self):
        item = simpleldap.LDAPItem(self.mock_results[0])
        self.assertTrue(item.value_contains('Joseph', 'cn'))
        self.assertFalse(item.value_contains('Bob', 'cn'))

    def test_equals(self):
        self.assertEqual(simpleldap.LDAPItem(self.mock_results[0]),
                         simpleldap.LDAPItem(self.mock_results[0]))
        self.assertNotEqual(simpleldap.LDAPItem(self.mock_results[0]),
                            simpleldap.LDAPItem(self.mock_results[1]))


if __name__ == "__main__":
    import unittest
    unittest.main()
