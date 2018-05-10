# coding=utf-8
import os

if __name__ == '__main__':
    os.environ['SIMPLE_SETTINGS'] = 'settings.' + os.sys.argv[1]
    from simple_settings import settings

    settings.setup()

    print(settings.as_dict())
    print(settings.UPDATE_INTERVAL)
