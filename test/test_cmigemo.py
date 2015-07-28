# -*- coding: utf-8 -*-

import unittest
import cmigemo

class TestCMigemo(unittest.TestCase):
    def setUp(self):
        pass

    dict_path_base = "/usr/share/cmigemo"
    def dict_path_for_encoding(self, encoding):
        return self.dict_path_base + "/" + encoding + "/" + "migemo-dict"

    def get_migemo_instance(self, encoding = "utf-8"):
        return cmigemo.Migemo(self.dict_path_for_encoding(encoding))

    def test_migemo_open(self):
        migemo = self.get_migemo_instance()
        self.assertTrue(isinstance(migemo, cmigemo.Migemo))
        self.assertTrue(migemo.is_enable())
        self.assertRaises(IOError, self.get_migemo_instance, "not-existing-dictionary")

    def test_migemo_load(self):
        migemo = self.get_migemo_instance("utf-8")
        loaded_dict_id = migemo.load(cmigemo.DICTID_MIGEMO, self.dict_path_for_encoding("utf-8"))
        self.assertEqual(cmigemo.DICTID_MIGEMO, loaded_dict_id)

    def test_migemo_load_not_found(self):
        migemo = self.get_migemo_instance("utf-8")
        loaded_dict_id = migemo.load(cmigemo.DICTID_MIGEMO, "not-existing-dictionary")
        self.assertEqual(cmigemo.DICTID_INVALID, loaded_dict_id)

    def test_migemo_get_encoding(self):
        migemo_utf8 = self.get_migemo_instance("utf-8")
        self.assertEqual("utf_8", migemo_utf8.get_encoding())

        migemo_eucjp = self.get_migemo_instance("euc-jp")
        self.assertEqual("euc_jp", migemo_eucjp.get_encoding())

    def test_migemo_query(self):
        expected_result_unicode = u"ホゲ"
        query_string_unicode = u"ほげ"

        migemo_utf8 = self.get_migemo_instance("utf-8")
        self.assertTrue(expected_result_unicode in migemo_utf8.query(query_string_unicode.encode("utf-8")))
        self.assertTrue(expected_result_unicode in migemo_utf8.query(query_string_unicode))

        migemo_eucjp = self.get_migemo_instance("euc-jp")
        self.assertTrue(expected_result_unicode in migemo_eucjp.query(query_string_unicode.encode("euc-jp")))
        self.assertTrue(expected_result_unicode in migemo_eucjp.query(query_string_unicode))

    def test_migemo_get_operator(self):
        migemo_utf8 = self.get_migemo_instance("utf-8")
        self.assertEqual("|", migemo_utf8.get_operator(0))
        self.assertEqual("(", migemo_utf8.get_operator(1))
        self.assertEqual(")", migemo_utf8.get_operator(2))

    def test_migemo_set_operator(self):
        migemo_utf8 = self.get_migemo_instance("utf-8")

        self.assertEqual("|", migemo_utf8.get_operator(0))
        self.assertTrue(migemo_utf8.set_operator(0, ")"))
        self.assertEqual(")", migemo_utf8.get_operator(0))

        self.assertEqual("(", migemo_utf8.get_operator(1))
        self.assertTrue(migemo_utf8.set_operator(1, "!"))
        self.assertEqual("!", migemo_utf8.get_operator(1))

if __name__ == "__main__":
    unittest.main()
