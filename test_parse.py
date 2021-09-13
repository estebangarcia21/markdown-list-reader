import unittest
from argparse import Namespace
from io import BytesIO, TextIOWrapper

from parse import (MarkdownLineData, MarkdownListType, get_section_name,
                   indent_size, is_md_list, read_args)


class FlagParserTestCase(unittest.TestCase):
    def test_read_args_string(self):
        ns = Namespace()

        ns.string = 'Hi'
        ns.file = None

        res = read_args(ns)

        self.assertEqual(res, 'Hi')

    def test_read_args_file(self):
        ns = Namespace()

        file = TextIOWrapper(BytesIO(), encoding='utf-8')
        file.write('Hello world!')
        file.seek(0, 0)

        ns.string = None
        ns.file = file

        res = read_args(ns)

        self.assertEqual(res, 'Hello world!')


class MarkdownParserTestCase(unittest.TestCase):
    def test_is_list(self):
        md_numeral = '1. Hello world!'

        self.assertEqual(MarkdownLineData(
            is_list=True,
            list_type=MarkdownListType.ORDERED
        ), is_md_list(md_numeral))

        md_bullet = '- Hello world!'

        self.assertEqual(MarkdownLineData(
            is_list=True,
            list_type=MarkdownListType.UNORDERED
        ), is_md_list(md_bullet))

        md_none = 'Hello world!'

        self.assertEqual(MarkdownLineData(
            is_list=False,
            list_type=None
        ), is_md_list(md_none))

    def test_indent_size(self):
        md_line = '   1. Section start'

        self.assertEqual(indent_size(md_line), 3)

    def test_get_section_name(self):
        md_numeral = '1. Hello world!'

        self.assertEqual(
            'Hello world!',
            get_section_name(md_numeral)
        )

        md_bullet = '- Hello world!'

        self.assertEqual(
            'Hello world!',
            get_section_name(md_bullet)
        )


if __name__ == '__main__':
    unittest.main()
