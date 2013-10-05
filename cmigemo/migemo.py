# -*- coding: utf-8 -*-

from ctypes import *

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
    migemo_struct = None

    def __init__(self, dictionary_path):
        self.libmigemo = self._load_libmigemo()
        self.migemo_struct = self._open_migemo(dictionary_path)

    def __del__(self):
        if self.migemo_struct is not None:
            self.libmigemo.migemo_close(self.migemo_struct)

    def _assert_file_exist(self, file_path):
        import os
        if not os.path.exists(file_path):
            raise IOError("Fie not found: " + file_path)

    def _open_migemo(self, dictionary_path):
        self._assert_file_exist(dictionary_path)
        return self.libmigemo.migemo_open(dictionary_path)

    def _load_libmigemo(self, lib_name = "libmigemo.so"):
        libmigemo = cdll.LoadLibrary(lib_name)
        libmigemo.migemo_open.restype = POINTER(MigemoStruct)
        libmigemo.migemo_get_operator.restype = c_char_p
        libmigemo.migemo_set_operator.restype = c_bool
        libmigemo.migemo_query.restype = c_void_p
        libmigemo.migemo_is_enable.restype = c_bool
        libmigemo.migemo_load.restype = c_int
        return libmigemo

    def _ensure_string_encoded(self, string):
        if isinstance(string, unicode):
            return string.encode(self.get_encoding())
        else:
            return string

    def _char_ptr_to_string(self, char_ptr):
        return cast(char_ptr, c_char_p).value

    charset_map = {
        0: "ascii",
        1: "cp932",
        2: "euc_jp",
        3: "utf_8",
    }
    def get_encoding(self):
        return self.charset_map[self.migemo_struct.contents.charset]

    def is_enable(self):
        return self.libmigemo.migemo_is_enable(self.migemo_struct)

    def load(self, dict_id, dict_file):
        return self.libmigemo.migemo_load(self.migemo_struct, dict_id, dict_file)

    def query(self, query_string):
        query_bytes = self._ensure_string_encoded(query_string)
        regexp_ptr = self.libmigemo.migemo_query(self.migemo_struct, query_bytes)
        try:
            regexp_bytes = self._char_ptr_to_string(regexp_ptr)
            regexp_string = regexp_bytes.decode(self.get_encoding())
        finally:
            self.libmigemo.migemo_release(self.migemo_struct, regexp_ptr)
        return regexp_string

    def get_operator(self, index):
        operator_bytes = self.libmigemo.migemo_get_operator(self.migemo_struct, index)
        return operator_bytes.decode(self.get_encoding())

    def set_operator(self, index, operator):
        operator_bytes = self._ensure_string_encoded(operator)
        return self.libmigemo.migemo_set_operator(self.migemo_struct, index, operator_bytes)
