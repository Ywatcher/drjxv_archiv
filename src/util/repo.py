from pathlib import Path

root = Path(__file__).parent.parent.parent.absolute()


if __name__ == "__main__":
    print(root)