from unittest import TestCase

from simpleldap.cidict import cidict


class cidictTests(TestCase):
    
    def test_init(self):
        pass
    
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
        pass
    
    def test_keys(self):
        pass
    
    def test_values(self):
        pass
    
    def test_case_insensitive(self):
        pass