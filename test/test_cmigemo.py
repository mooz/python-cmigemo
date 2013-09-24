# -*- coding:utf-8 -*-

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

    def test_migemo_load(self):
        migemo = self.get_migemo_instance()
        self.assertTrue(isinstance(migemo, cmigemo.Migemo))
        self.assertRaises(IOError, self.get_migemo_instance, "not-existing-dictionary")

    def test_migemo_get_encoding(self):
        migemo_utf8 = self.get_migemo_instance("utf-8")
        self.assertEqual("utf_8", migemo_utf8.get_encoding())

        migemo_eucjp = self.get_migemo_instance("euc-jp")
        self.assertEqual("euc_jp", migemo_eucjp.get_encoding())

    def test_migemo_query(self):
        migemo = cmigemo.Migemo(self.dict_path_for_encoding("utf-8"))
        self.assertEqual(u"(フガ|府[金外]|腑甲斐|不学|富嶽|ふが|ｈｕｇａ|huga)",
                         migemo.query("huga"))

if __name__ == "__main__":
    unittest.main()
