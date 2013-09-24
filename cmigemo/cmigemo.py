# -*- coding: utf-8 -*-

from ctypes import *

charset_map = {
    0: "ascii",
    1: "cp932",
    2: "euc_jp",
    3: "utf_8",
}

class MigemoStruct(Structure):
    _fields_ = [
        ("enable", c_int),
        ("mtree", c_void_p),
        ("charset", c_int),
        ("roma2hira", c_void_p),
        ("hira2kata", c_void_p),
        ("han2zen", c_void_p),
        ("zen2han", c_void_p),
        ("rx", c_void_p),
        ("addword", c_void_p),
        ("char2int", c_void_p)
    ]

class Migemo(object):
    def __init__(self, dictionary_path):
        self.libmigemo = self.load_libmigemo()
        self.migemo_struct = self.open_migemo(dictionary_path)

    def open_migemo(self, dictionary_path):
        import os
        if not os.path.exists(dictionary_path):
            raise IOError("Specified dictionary not found: " + dictionary_path)
        return self.libmigemo.migemo_open(dictionary_path)

    def load_libmigemo(self, lib_name = "libmigemo.so"):
        libmigemo = cdll.LoadLibrary(lib_name)
        libmigemo.migemo_open.restype = POINTER(MigemoStruct)
        libmigemo.migemo_get_operator.restype = c_char_p
        libmigemo.migemo_query.restype = c_char_p
        return libmigemo

    def ensure_string_encoded(self, string):
        if isinstance(string, unicode):
            return string.encode(self.get_encoding())
        else:
            return string

    def get_encoding(self):
        return charset_map[self.migemo_struct.contents.charset]

    def get_operator(self, index):
        return self.libmigemo.migemo_get_operator(self.migemo_struct, index)

    def is_enable(self):
        pass

    def load(self):
        pass

    def query(self, query_string):
        query_bytes = self.ensure_string_encoded(query_string)
        regexp_bytes = self.libmigemo.migemo_query(self.migemo_struct, query_bytes)
        return regexp_bytes.decode(self.get_encoding())

    def set_operator(self):
        pass
