from argparse import Namespace
from enum import Enum
from dataclasses import dataclass
from io import TextIOWrapper
from typing import List


EXTRA_LIST_TOKENS = ['-']


@dataclass
class Section:
    """A section in a list. For example:

    1. This is a top level section
       2. A sub section
       3. Another sub section
       4. A top level section again
          1. A sub section

    Top level sections will have child Section objects.
    """
    title: str
    subsections: list


@dataclass
class ParseResult:
    top_section: Section


def read_args(args: Namespace) -> str:
    """Reads the arguments from an argparse argument set, returning the
    loaded markdown from a file or the markdown string passed from the -s
    flag. Throws an error if the file does not exist."""
    string_arg: str = args.string
    file_arg: TextIOWrapper = args.file

    if file_arg is not None:
        md = file_arg.read()
    elif string_arg is not None:
        md = string_arg
    else:
        print('No markdown specified. Read the help using the --help or -h flags')
        exit(1)

    return md


def parse_markdown(md: str) -> ParseResult:
    """Read a markdown string and return all sections of a the specified list."""
    lines = md.splitlines()

    depth = 0
    acc: list[Section] = []

    for i in range(len(lines)):
        l = lines[i]

        if is_md_list(l):
            acc.append(Section(title='SN', subsections=[]))


def is_md_list(s: str) -> bool:
    """Checks if a line is a markdown list."""
    s = s.strip()

    if len(s) == 0 or s[0] == '\n':
        return False
    else:
        fc = s[0]

    return _is_list_char(fc)


def get_title(s: str) -> str:
    """Get the title of a bullet point in a list."""
    if not is_md_list(s):
        return s


def indent_size(s: str) -> int:
    """Get the indentation size of a string."""
    indent = 0

    for c in s:
        if c == ' ':
            indent += 1
        else:
            break

    return indent


def _traverse_sections(md: str, pos: int) -> list[Section]:
    """Traverse a tree of subsections for a given top level section."""
    pass


class MarkdownListType(Enum):
    """The type of list a markdown list is."""
    ORDERED = 0
    UNORDERED = 1


@dataclass
class MarkdownLineData:
    """Result of checking if a markdown line is a list. Contains a boolean
    indicating if it is a line and an enum value on what kind of list
    it is."""
    is_list: bool
    list_type: MarkdownListType


def _is_list_char(c: str) -> MarkdownLineData:
    """Check if char is a list token."""
    fc = c[0]

    if EXTRA_LIST_TOKENS.count(fc) > 0:
        list_type = MarkdownListType.UNORDERED
    elif fc.isnumeric():
        list_type = MarkdownListType.ORDERED
    else:
        list_type = None

    return MarkdownLineData(
        is_list=list_type is not None,
        list_type=list_type
    )


def get_section_name(s: str) -> str:
    """Get the name of a list section."""
    line_data = _is_list_char(s)

    if not line_data.is_list:
        return s

    lt = line_data.list_type

    s = s.strip()

    if lt is MarkdownListType.ORDERED:
        return ''.join(s.split('.')[1:]).strip()

    if lt is MarkdownListType.UNORDERED:
        return ''.join(s[1:]).strip()
