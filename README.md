# Markdown List Reader

A simple tool for reading lists in markdown.

## Usage

Begin by running the `mdr.py` file and input either a markdown string with the `--string` flag or a file with the `--file` flag.

```shell
python3 mdr.py --file example.py
```

If successful, it will execute the main function in `main.py` with all of the parsed sections. Example `main.py`:

```python
from parse import Section


def main(sections: list[Section]):
    for s in sections:
        print(s.title)


if __name__ == '__main__':
    print('Run mdr.py to parse your markdown list!')
    exit(1)
```

Output:

```
Section one
Introduction
Section two
Thats it
```
