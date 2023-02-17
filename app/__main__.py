from gdp import parser

import logging
import logging.handlers


log_format = '%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d %(levelname)s %(message)s'


def get_stream_handler() -> logging.StreamHandler:
    '''Инициализирует обработчик вывода логов в stdout'''
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(log_format))
    return stream_handler


def get_logger(name: str) -> logging.Logger:
    '''Собирает логгер из компонентов'''
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_stream_handler())
    return logger


_parser = parser.Parser('./app/Student_1.docx',
                        output_path='./app/out.xml', logger=get_logger(__name__))

_parser.parse()
