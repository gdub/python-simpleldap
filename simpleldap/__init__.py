"""
This module makes simple LDAP queries simple.
"""

import ldap

DEBUG = False
if DEBUG:
    # Log debug statements to standard error.
    import sys
    ldap.set_option(ldap.OPT_DEBUG_LEVEL, 255)
    ldapmodule_trace_level=1
    ldapmodule_trace_file=sys.stderr


class SimpleLDAPException(Exception):
    """Base class for all simpleldap exceptions."""

class ObjectNotFound(SimpleLDAPException):
    """
    Exception when no objects were returned, but was expecting a single item.
    """

class MultipleObjectsFound(SimpleLDAPException):
    """
    Exception for when multiple objects were returned, but was expecting only
    a single item.
    """


class LDAPItem(dict):
    """
    A convenience class for wrapping standard LDAPResult objects.
    """

    def __init__(self, LDAPResult):
        self.dn, self.attributes = LDAPResult
        # XXX: quick and dirty, should really proxy straight to the existing
        # self.attributes dict.
        for attribute, values in self.attributes.iteritems():
            # Make the entire list of values for each LDAP attribute
            # accessible through a dictionary mapping.
            self[attribute] = values

    def first(self, attribute):
        """
        Return the first value for the given LDAP attribute.
        """
        return self[attribute][0]

    def value_contains(self, value, attribute):
        """
        Determine if any of the items in the value list for the given
        attribute contain value.
        """
        for item in self[attribute]:
            if value in item:
                return True
        return False

    def __str__(self):
        """
        Print attribute names and values, one per line, in alphabetical order.

        Attribute names are displayed right-aligned to the length of the
        longest attribute name.
        """
        attributes = self.keys()
        longestKeyLength = max([len(attr) for attr in attributes])
        output = []
        for attr in sorted(attributes):
            values = ("\n%*s  " % (longestKeyLength, ' ')).join(self[attr])
            output.append("%*s: %s" % (longestKeyLength, attr, values))
        return "\n".join(output)


class Connection(object):
    """
    A connection to an LDAP server.
    """

    # The class to use for items returned in results.  Subclasses can change
    # this to a class of their liking.
    result_item_class = LDAPItem

    def __init__(self, hostname, port=None, dn='', password='',
                 encryption=None):
        """
        Bind using the passed DN and password.

        If no user and password is given, try to connect anonymously with a
        blank user DN and password.

        ``encryption`` should be one of 'tls', 'ssl', or ``None``.  If 'tls',
        then the standard port 389 is used by default and after binding, tls is
        started.  If 'ssl', then port 636 is used by default.
        """
        if not encryption or encryption == 'tls':
            protocol = 'ldap'
            if not port:
                port = 389
        elif encryption == 'ssl':
            protocol = 'ldaps'
            if not port:
                port = 636
        else:
            raise ValueError("Invalid encryption protocol."
                             " Must be one of: 'tls' or 'ssl'.")

        url='%s://%s:%s' % (protocol, hostname, port)
        self.connection = ldap.initialize(url)
        if encryption == 'tls':
            self.connection.start_tls_s()
        # It seems that python-ldap chokes when passed unicode objects with
        # non-ascii characters.  So if we have a unicode password, encode
        # it to utf-8.
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        self.connection.simple_bind_s(dn, password)

    def close(self):
        """
        Shutdown the connection.
        """
        self.connection.unbind_s()

    def search(self, filter, base_dn='', attrs=None, scope=ldap.SCOPE_SUBTREE,
               timeout=-1, limit=0):
        """
        Search the directory.
        """
        results=self.connection.search_ext_s(
            base_dn, scope, filter, attrs, timeout=timeout, sizelimit=limit)
        return self.to_items(results)

    def get(self, *args, **kwargs):
        """
        Get a single object.

        This is a convenience wrapper for the search method that checks that
        only one object was returned, and returns that single object instead
        of a list.  This method takes the exact same arguments as search.
        """
        results = self.search(*args, **kwargs)
        num_results = len(results)
        if num_results == 1:
            return results[0]
        if num_results > 1:
            raise MultipleObjectsFound()
        if num_results < 1:
            raise ObjectNotFound()

    def to_items(self, results):
        """
        Turn LDAPResult objects returned from the ldap library into more
        convenient objects.
        """
        return [self.result_item_class(item) for item in results]
