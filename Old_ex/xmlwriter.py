from xmlmarkupparser import Token


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
