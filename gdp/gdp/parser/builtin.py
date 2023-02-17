import io
import re
import zipfile
import logging

from lxml import etree


class Parser:
    def __init__(
            self, input_path: str, style: str | None = "xml-markup", output_path: str | None = None,
            root_ns: str | None = None, root_ns_prefix: str | None = None, schema: str | None = None,
            logger: logging.Logger | None = None) -> None:
        """Init method of Parser class

        Args:
            input_path (str): path to .docx or .doc file
            style (str | None, optional): MS Word style name for xml. Defaults to "xml-markup".
            output_path (str | None, optional): path to output file with it's name. Defaults to None.
            root_ns (str | None, optional): root namespace tag. Defaults to None.
            root_ns_prefix (str | None, optional): root namespace tag prefix. Defaults to None.
            schema (str | None, optional): path to validation schema. Defaults to None.
        """
        self.input_path = input_path
        self.style = style
        self.output_path = output_path
        self.root_ns = root_ns
        self.root_ns_prefix = root_ns_prefix
        self.schema = schema
        self.logger = logger

    def parse(self):
        """Main parsing method. Extracts xml from MS Word file and parses it.

        Raises:
            Exception: _description_
        """
        if self.root_ns is not None and self.root_ns_prefix is None:
            # TODO: Exceptions
            raise Exception('Root namespace prefix must be specified.')

        with zipfile.ZipFile(self.input_path, 'r') as zip_file:
            document_str = zip_file.read('word/document.xml')
        root = etree.fromstring(document_str)  # type: ignore

        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        tokens = _parse(root, ns, self.style)
        output = io.StringIO()
        writer = SimpleXmlWriter(output, ns=self.root_ns,
                                 ns_prefix=self.root_ns_prefix)
        for tok in tokens:
            writer.write(tok)
        output = output.getvalue()

        if self.output_path is not None:
            if self.logger is not None:
                self.logger.info(f'[+] Output to {self.output_path}')
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(output)

        if self.schema is not None:
            print('[+] Validation with', self.schema)
            out_root = etree.fromstring(output.encode('utf-8'))  # type: ignore

            schema_root = etree.parse(self.schema)  # type: ignore
            schema = etree.XMLSchema(schema_root)
            if not schema.validate(out_root):
                if self.logger is not None:
                    self.logger.error(
                        f'- Document is invalid, errors: \n {schema.error_log}')
                raise Exception('Document is invalid.')
            else:
                if self.logger is not None:
                    self.logger.error('- Document is valid.')


class Token:
    class StartTag:
        __slots__ = ('name',)

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f'StartTag({self.name})'

    class EndTag:
        def __repr__(self):
            return 'EndTag'

    class Data:
        __slots__ = ('data',)

        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return f'Data({self.data})'


class XmlMarkupError(Exception):
    pass


def is_run_has_style(run, style, ns):
    props = run.find('w:rPr', ns)
    if props is None:
        return False

    style_prop = props.find('w:rStyle', ns)
    if style_prop is None:
        return False

    value = style_prop.attrib[f'{{{ns["w"]}}}val']
    if value and value == style:
        return True
    return False


def parse_markup_tag(tag):
    if tag[:2] == '{{' and tag[-1] == '|':
        return Token.StartTag(tag[2:-1])
    elif tag == '}}':
        return Token.EndTag()
    else:
        raise XmlMarkupError


def parse_markup_tags(tags_str):
    for tag in re.findall(r'{{[^|]+\||}}', tags_str):
        yield parse_markup_tag(tag)


def make_tokens(is_tag, text):
    if is_tag:
        yield from parse_markup_tags(text)
    else:
        yield Token.Data(text)


def literals(root, ns, style):
    paragraphs = root.iterfind('.//w:p', ns)
    for paragraph in paragraphs:
        runs = paragraph.iterfind('w:r', ns)
        for run in runs:
            has_style = is_run_has_style(run, style, ns)
            texts = run.iterfind('w:t', ns)
            for text in texts:
                yield has_style, text.text
        yield False, '\n'


def _parse(root, ns, style):
    is_tag_prev = None
    data = []
    for is_tag, text in literals(root, ns, style):
        if is_tag_prev is not None and is_tag_prev != is_tag:
            d = ''.join(data)
            data.clear()
            yield from make_tokens(is_tag_prev, d)
        data.append(text)
        is_tag_prev = is_tag

    if data:
        yield from make_tokens(is_tag_prev, ''.join(data))


class SimpleXmlWriter:
    def __init__(self, writer, ns=None, ns_prefix=None):
        self._writer = writer
        self._stack = []
        self._data = None
        self._is_first_write = True
        self._ns = ns
        self._ns_prefix = ns_prefix if ns_prefix else ''

    def write(self, tok):
        if self._is_first_write:
            self._writer.write('<?xml version="1.0" encoding="UTF-8"?>\n')

        ttok = type(tok)
        if ttok is Token.StartTag:
            self._data = None
            self._writer.write(self._make_tag(tok.name))
            self._stack.append(tok.name)
        elif ttok is Token.EndTag:
            if self._data is not None:
                self._writer.write(self._data)
                self._data = None
            name = self._stack.pop()
            self._writer.write(self._make_tag(name, is_open_tag=False))
        elif ttok is Token.Data:
            self._data = tok.data

        self._is_first_write = False

    def _make_tag(self, name, is_open_tag=True):
        if self._ns:
            name = f"{self._ns_prefix}:{name}"

        if self._is_first_write:
            attrs = f" xmlns:{self._ns_prefix}=\"{self._ns}\""
        else:
            attrs = ''

        if is_open_tag:
            return f"<{name}{attrs}>"
        else:
            return f"</{name}>"

    def close(self):
        self._writer.close()
