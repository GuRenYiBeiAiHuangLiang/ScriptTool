# coding=utf-8


import types
import typing
import re


class TemplateParser:

    ParserState = typing.NamedTuple("ParserState", [("Remaining", list), ("Map", dict), ("Line", int)])

    single = re.compile("^(\S+)\s*$")
    multi = re.compile("^(\S+)\s+(\S.*)")

    comment = re.compile("^\s*#")

    indented = re.compile("^\s+(.*)")

    @classmethod
    def inner(cls, state: ParserState):
        pass
        
    @classmethod
    def parse(cls, contents: str):
        contents = contents.replace("\r\n", "\n").replace("\r", "\n")
        remaining = contents.split("\n")
        return cls.inner()
