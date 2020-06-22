"""
Generic configuration module.

|
| Start your application using:
|
| ``application.py --config CONFIGFILE.yml``
|
|
| You can also provide multiple configurations:
|
| ``application.py --config CONFIGFILE1.yml CONFIGFILE2.yml CONFIGFILE3.yml``
|
|
| When using multiple conf files, the latter files may override settings
| from the former files.
|
| In your application:
|
| ``import conf``
| ``my_setting = conf.get('my_setting', 'DEFAULT_SETTING')``
|
|
| If you don't need a default setting - make sure you always supply a conf
| file and that the setting exists:
|
| ``my_setting = conf.my_setting``
|
|
| Or simply:
|
| ``from conf import my_setting``
|
|
| If you use an ArgumentParser in your own application for other purposes, you
| must use the ``parse_known_args()`` method of the parser.
|
| Alternatively, you can load configuration files manually, using the load
| function. If you do this, make sure that the path is absolute. The syntax is:
|
| ``conf.load('complete/path/to/conf.yml')``
"""

from conf.reader import *
