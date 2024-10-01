"""
app name:  GSI updater
summary: Extract and install the downloaded your_gsi_img_name.xz.img.
"""

import os
import sys
import glob
import pathlib
import subprocess
from typing import Literal


IMG: str = ".img"
DOT_XZ: str = ".xz"
IMG_XZ: list[str, str] = ["img", "xz"]
GSI_TYPE: list[str, str] = ["aosp", "arm64", "ab", "gapps"]
FILE_TYPE = Literal["xz", "img"]
DOWNLOADS_DIR: str = r"/downloads/"


def search_gsi_img(filetype: FILE_TYPE) -> tuple[bool, list[str, str]]:
    """search GSI(**.img.xz)

    Args:
        filetype (FILE_TYPE): file extention

    Returns:
        tuple[bool, list[str, str]]: results of the execution and found files.
    """
    try:
        gsi_img_xz = list(
            filter(
                lambda gsi: pathlib.Path(gsi).suffix == filetype,
                glob.glob(DOWNLOADS_DIR + "**", recursive=True)  # fmt: skip
            )
        )
        return True, gsi_img_xz
    except Exception:
        return False, None


def exec_flash():
    ret, gsi_img_xz_list = search_gsi_img(DOT_XZ)

    if ret and any(gsi_img_xz_list):
        reversed_gsi_img_xz_list = sorted(gsi_img_xz_list, reverse=True)
        gsi_img_xz = reversed_gsi_img_xz_list[0]

        if gsi_img_xz.split(".")[-2:] == IMG_XZ:
            subprocess.run("unxz %s" % gsi_img_xz, shell=True)

        _, gsi_imgs = search_gsi_img(IMG)
        if gsi_imgs[0].split(os.sep)[-1].split("-")[:4] == GSI_TYPE:
            subprocess.run("adb reboot bootloader", shell=True)
            subprocess.run("fastboot reboot fastboot", shell=True)
            subprocess.run("fastboot flash system  %s" % gsi_imgs[0], shell=True)  # fmt: skip
            subprocess.run("fastboot reboot", shell=True)
        return
    else:
        raise IndexError


if __name__ == "__main__":
    try:
        exec_flash()
    except Exception as exc:
        sys.stdout.writelines("%s" % exc)
        raise exc
    else:
        sys.stdout.writelines("%s" % "all done!!")
