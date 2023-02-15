#!/usr/bin/env python3

import argparse
import io
import zipfile
#import xml.etree.ElementTree as XMLTree
from lxml import etree

from xmlmarkupparser import parse, Token
from xmlwriter import SimpleXmlWriter

def make_argparser():
    parser = argparse.ArgumentParser(description="Extract xml-markup from docx into xml")
    parser.add_argument('input', help='input path for docx file')
    parser.add_argument('--style', help='style name of xml-markup in docx', default='xml-markup')
    parser.add_argument('--output', help='output path for xml file')
    parser.add_argument('--root-ns', help='namespace for root element')
    parser.add_argument('--root-ns-prefix', help='namespace prefix for root element')
    parser.add_argument('--schema', help='validate with xsd schema')
    return parser


def main():
    parser = make_argparser()
    args = parser.parse_args()
    if args.root_ns and not args.root_ns_prefix:
        print('Namespace prefix must be specified with --root-ns-prefix')
        return
    
    with zipfile.ZipFile(args.input, 'r') as zip_file:
        document_str = zip_file.read('word/document.xml')
        #zip_file.extract('word/document.xml')
    root = etree.fromstring(document_str)
    #root = etree.parse('word/document.xml')

    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    tokens = parse(root, ns, args.style)
    output = io.StringIO()
    writer = SimpleXmlWriter(output, ns=args.root_ns, ns_prefix=args.root_ns_prefix)
    for tok in tokens:
        writer.write(tok)
    output = output.getvalue()
    
    if args.output:
        print('[+] Output to ', args.output)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    
            
    
    if args.schema:
        print('[+] Validation with', args.schema)
        out_root = etree.fromstring(output.encode('utf-8'))
        
        schema_root = etree.parse(args.schema)
        schema = etree.XMLSchema(schema_root)
        if not schema.validate(out_root):
            print(f"- Document is invalid, errors:")
            print(schema.error_log)
        else:
            print(f"- Document is valid")



if __name__ == '__main__':
    main()