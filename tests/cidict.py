from unittest import TestCase

from simpleldap.cidict import cidict


class cidictTests(TestCase):

    def test_setitem_getitem_get(self):
        d = cidict()
        d['foo'] = 'bar'
        self.assertEqual(d['foo'], 'bar')
        self.assertEqual(d['FOO'], 'bar')
        self.assertEqual(d.get('foo'), 'bar')
        self.assertEqual(d.get('FOO'), 'bar')
        d['FOO'] = 'baz'
        self.assertEqual(d['foo'], 'baz')
        self.assertEqual(d['FOO'], 'baz')
        self.assertEqual(d.get('foo'), 'baz')
        self.assertEqual(d.get('FOO'), 'baz')

    def test_update(self):
        d = cidict({'foo': 'bar', 'FOO': 'bar', 'bar': 'baz'})
        self.assertEqual(len(d), 2)

    def test_keys_has_key(self):
        d = cidict({'foo': 'bar', 'bar': 'baz'})
        self.assertEqual(sorted(list(d)), ['bar', 'foo'])
        self.assertEqual(sorted(d.keys()), ['bar', 'foo'])
        self.assertTrue(d.has_key('foo'))
        self.assertTrue(d.has_key('FOO'))
        self.assertTrue('foo' in d)
        self.assertTrue('FOO' in d)
        d['FOO'] = 'bar'
        del d['foo']
        self.assertFalse(d.has_key('foo'))
        self.assertFalse(d.has_key('FOO'))
        self.assertFalse('foo' in d)
        self.assertFalse('FOO' in d)

    def test_values_items(self):
        d = cidict({'foo': 'bar', 'FOO': 'bar', 'bar': 'baz'})
        self.assertEqual(sorted(d.values()), ['bar', 'baz'])
        d = cidict({'foo': 'bar', 'bar': 'baz'})
        self.assertEqual(sorted(d.items()), [('bar', 'baz'), ('foo', 'bar')])

if __name__ == "__main__":
    import unittest
    unittest.main()
