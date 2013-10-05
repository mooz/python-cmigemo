# python-cmigemo

python-cmigemo is a pure python binding for C/Migemo (http://www.kaoriya.net/software/cmigemo/).

## Installation

    $ pip install cmigemo

And of cource, you need C/Migemo.

    $ apt-get install cmigemo

## Usage

python-cmigemo can be used as an alternative to PyMigemo (http://www.atzm.org/etc/pymigemo/).

```python
import cmigemo

migemo = cmigemo.Migemo("/usr/share/cmigemo/utf-8/migemo-dict")

print(migemo.query("hoge"))
# (ホゲ|補元|保元|帆桁|捕鯨|ほげ|ｈｏｇｅ|hoge)
```
