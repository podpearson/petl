from __future__ import absolute_import, print_function, division


__author__ = 'Alistair Miles <alimanfoo@googlemail.com>'


from tempfile import NamedTemporaryFile
import cPickle as pickle


from petl.testutils import ieq
from petl.io.pickle import frompickle, topickle, appendpickle


def test_frompickle():
    """Test the frompickle function."""

    f = NamedTemporaryFile(delete=False)
    table = (('foo', 'bar'),
             ('a', 1),
             ('b', 2),
             ('c', 2))
    for row in table:
        pickle.dump(row, f)
    f.close()

    actual = frompickle(f.name)
    ieq(table, actual)
    ieq(table, actual) # verify can iterate twice


def test_topickle_appendpickle():
    """Test the topickle and appendpickle functions."""

    # exercise function
    table = (('foo', 'bar'),
             ('a', 1),
             ('b', 2),
             ('c', 2))
    f = NamedTemporaryFile(delete=False)
    topickle(table, f.name)

    def picklereader(fl):
        try:
            while True:
                yield pickle.load(fl)
        except EOFError:
            pass

    # check what it did
    with open(f.name, 'rb') as o:
        actual = picklereader(o)
        ieq(table, actual)

    # check appending
    table2 = (('foo', 'bar'),
              ('d', 7),
              ('e', 9),
              ('f', 1))
    appendpickle(table2, f.name)

    # check what it did
    with open(f.name, 'rb') as o:
        actual = picklereader(o)
        expect = (('foo', 'bar'),
                  ('a', 1),
                  ('b', 2),
                  ('c', 2),
                  ('d', 7),
                  ('e', 9),
                  ('f', 1))
        ieq(expect, actual)

