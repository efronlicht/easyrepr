# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:03:11 2017
@author: efron
Python 3.6.0
"""

from itertools import chain

def easyrepr(cls):
    """class decorator. tries to create self-documenting __repr__. 
    such that, where possible for immutable objects with 
    implemented __equals__, 
    eval(repr(x)) == x 
    
    """
    _cls_new = cls.__new__
    def _repr(self):
        return self._easyrepr
    def _new(cls, *args, **kwargs):
        instance = _cls_new(cls)
        argstr = (f'{arg!r}' for arg in args)
        kwargstr = (f'{arg} = {kwargs[arg]!r}' for arg in kwargs)
        args = ', '.join(chain(argstr, kwargstr))
        instance._easyrepr = f'{cls.__name__}({args})'
        return instance
    cls.__new__ = _new
    cls.__repr__ = _repr
    return cls


if __name__ == '__main__':
    @easyrepr
    class TestClass():
        def __init__(self, foo, *, bar):
            self.foo, self.bar = foo, bar
        def __eq__(self, other):
            return self.foo, self.bar == other.foo, other.bar
    class OtherTestClass(TestClass):
        pass
    class OverRiddenRepr(TestClass):
        def __repr__(self):
            return 'override'
    
    def test_simple_repr():
        a = TestClass('foo', bar = 'bar')
        assert repr(a) == "TestClass('foo', bar = 'bar')"
    def test_subclass_repr():
        assert repr(OtherTestClass('foo', bar = 'bar')) == "OtherTestClass('foo', bar = 'bar')"
    def test_recursive_repr():
        a = TestClass('foo', bar = 'bar')
        b = TestClass('spam', bar = 'eggs')
        c = TestClass(a, bar = b)
        assert repr(c) == "TestClass(TestClass('foo', bar = 'bar'), bar = TestClass('spam', bar = 'eggs'))"
        assert c == eval(repr(c))
    def test_repr_override():
        assert repr(OverRiddenRepr('foo', bar = 'bar')) == 'override'
            
    tests = [test_recursive_repr, test_simple_repr, test_subclass_repr, test_repr_override]
    passed = True
    for test in tests:
        try:
            test()
        except AssertionError:
            print(f'{test.__name__} failed!')
            passed = False
        else:
            print(f'{test.__name__} passed!')
    if passed:
        print('all tests passed!')