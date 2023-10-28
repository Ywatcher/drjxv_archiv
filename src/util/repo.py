import os
from pathlib import Path

root = Path(__file__).parent.parent.parent.absolute()
driver_root = os.path.join(root, "driver")
database_root = os.path.join(root, "archiv_db")
drivers = {  # FIXME: put it into config
    "chrome": os.path.join(
        driver_root,
        "chromedriver-linux64",
        # "/home/ywatcher/.cache/selenium/chromedriver/linux64/118.0.5993.70",
        "chromedriver"),

    "firefox": os.path.join(
        driver_root, "geckodriver-v0.33.0-linux64", "geckodriver"),
    "edge": os.path.join(
        driver_root, "edgedriver_linux64", "msedgedriver")
}
git_repo = "/media/ywatcher/ExtDisk1/Files/web_archiv_/git_repo"
git_repo_test = "/media/ywatcher/ExtDisk1/Files/web_archiv_/git_repo_test"


if __name__ == "__main__":
    print(root)
