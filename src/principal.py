import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaz.aplicacion import Aplicacion


def main():
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()
