# -*- coding: utf-8 -*-

import six

from ctypes import *
from ctypes.util import find_library

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

    def __init__(self, dictionary_path, path_encoding="utf_8"):
        self.path_encoding = path_encoding
        self.libmigemo = self._load_libmigemo()
        self.migemo_struct = self._open_migemo(dictionary_path)

    def __del__(self):
        if self.migemo_struct is not None:
            self.libmigemo.migemo_close(self.migemo_struct)

    def _assert_file_exist(self, file_path):
        import os
        if not os.path.exists(file_path):
            raise IOError("File not found: " + file_path)

    def _open_migemo(self, dictionary_path):
        self._assert_file_exist(dictionary_path)
        dictionary_path_raw = self._ensure_string_encoded(dictionary_path,
                                                          self.path_encoding)
        return self.libmigemo.migemo_open(dictionary_path_raw)

    def _load_libmigemo(self, lib_name="migemo"):
        import platform
        if platform.system() == u"Windows":
            libmigemo = windll.migemo
        elif platform.system() == u"Darwin":
            libmigemo = CDLL("libmigemo.dylib")
        else:
            lib_path = find_library(lib_name)
            if lib_path is None:
                lib_path = "lib" + lib_name + ".so"
            libmigemo = cdll.LoadLibrary(lib_path)
        libmigemo.migemo_open.restype = POINTER(MigemoStruct)
        libmigemo.migemo_get_operator.restype = c_char_p
        libmigemo.migemo_set_operator.restype = c_bool
        # Note: Actually migemo_query's return type is char* (it
        # returns newly-allocated string, which have to be released by
        # us afterward). However if we do "restype = c_char_p", ctypes
        # converts returned pointer value to Python string, preventing
        # us from getting pointer value and freeing the memory pointed
        # by the value. We take a known workaround for this issue,
        # which do "restype = c_void_p" and cast it afterward.
        libmigemo.migemo_query.restype = c_void_p
        libmigemo.migemo_is_enable.restype = c_bool
        libmigemo.migemo_load.restype = c_int
        return libmigemo

    def _ensure_string_encoded(self, string, encoding=None):
        if isinstance(string, six.text_type):
            return string.encode(encoding or self.get_encoding())
        else:
            return string

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
        dict_file_raw = self._ensure_string_encoded(dict_file,
                                                    self.path_encoding)
        return self.libmigemo.migemo_load(self.migemo_struct,
                                          dict_id,
                                          dict_file_raw)

    def _migemo_query(self, query_string):
        query_bytes = self._ensure_string_encoded(query_string)
        regexp_ptr = self.libmigemo.migemo_query(self.migemo_struct, query_bytes)
        return regexp_ptr

    def _ptr_to_python_string(self, ptr):
        regexp_bytes = cast(ptr, c_char_p).value
        regexp_string = regexp_bytes.decode(self.get_encoding())
        return regexp_string

    def _migemo_release_memory(self, ptr):
        # To free char* correctly, we need casting
        self.libmigemo.migemo_release(self.migemo_struct, cast(ptr, c_char_p))

    def query(self, query_string):
        regexp_ptr = self._migemo_query(query_string)
        try:
            regexp_string = self._ptr_to_python_string(regexp_ptr)
        finally:
            self._migemo_release_memory(regexp_ptr)
        return regexp_string

    def get_operator(self, index):
        operator_bytes = self.libmigemo.migemo_get_operator(self.migemo_struct, index)
        return operator_bytes.decode(self.get_encoding())

    def set_operator(self, index, operator):
        operator_bytes = self._ensure_string_encoded(operator)
        return self.libmigemo.migemo_set_operator(self.migemo_struct, index, operator_bytes)
