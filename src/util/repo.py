import os
from pathlib import Path

root = Path(__file__).parent.parent.parent.absolute()
driver_root = os.path.join(root, "driver")
database_root = os.path.join(root, "archiv_db")


if __name__ == "__main__":
    print(root)
