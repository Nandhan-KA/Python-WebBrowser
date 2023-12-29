import os
import sys


def run():
    try:
        modules = ["PyQt5", "PyQt5-tools", "PyQtWebEngine", "qt-widgets"]
        os.system(f"pip install {' '.join(modules)}")
    except Exception as e:
        print("Error Occured "+e)
        sys.exit(0)


if __name__ == '__main__':
    run()
