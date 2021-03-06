from unittest import TestCase
from textwrap import dedent
from io import StringIO
import memestra

class TestBasic(TestCase):

    def checkDeprecatedUses(self, code, expected_output):
        sio = StringIO(dedent(code))
        output = memestra.memestra(sio, ('decoratortest', 'deprecated'))
        self.assertEqual(output, expected_output)


    def test_import(self):
        code = '''
            import decoratortest

            @decoratortest.deprecated
            def foo(): pass

            def bar():
                foo()

            foo()'''

        self.checkDeprecatedUses(
            code,
            [('foo', '<>', 8, 4), ('foo', '<>', 10, 0)])

    def test_import_alias(self):
        code = '''
            import decoratortest as dec

            @dec.deprecated
            def foo(): pass

            def bar():
                foo()

            foo()'''

        self.checkDeprecatedUses(
            code,
            [('foo', '<>', 8, 4), ('foo', '<>', 10, 0)])

    def test_import_from(self):
        code = '''
            from decoratortest import deprecated

            @deprecated
            def foo(): pass

            def bar():
                foo()

            foo()'''

        self.checkDeprecatedUses(
            code,
            [('foo', '<>', 8, 4), ('foo', '<>', 10, 0)])

    def test_import_from_alias(self):
        code = '''
            from decoratortest import deprecated as dp

            @dp
            def foo(): pass

            def bar():
                foo()

            foo()'''

        self.checkDeprecatedUses(
            code,
            [('foo', '<>', 8, 4), ('foo', '<>', 10, 0)])

    def test_call_from_deprecated(self):
        code = '''
            from decoratortest import deprecated as dp

            @dp
            def foo(): pass

            @dp
            def bar():
                foo()

            foo()'''

        self.checkDeprecatedUses(
            code,
            [('foo', '<>', 11, 0),])
