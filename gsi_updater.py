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


def search_gsi_img(filetype: FILE_TYPE) -> tuple[bool, list[str, str]]:
    try:
        current_work_dir = os.getcwd()
        gsi_img_xz = list(
            filter(
                lambda gsi: pathlib.Path(gsi).suffix == filetype,
                glob.glob(current_work_dir + "/**", recursive=True)  # fmt: skip
            )
        )
        return True, gsi_img_xz
    except Exception:
        return False, None


def main():
    ret, gsi_img_xz_list = search_gsi_img(DOT_XZ)
    if ret and gsi_img_xz_list is not None:
        reversed_gsi_img_xz_list = sorted(gsi_img_xz_list, reverse=True)
        gsi_img_xz = reversed_gsi_img_xz_list[0]

        if gsi_img_xz.split(".")[-2:] == IMG_XZ:
            subprocess.run("unxz %s" % gsi_img_xz, shell=True)

        _, gsi_imgs = search_gsi_img(IMG)
        if gsi_imgs[0].split("/")[-1].split("-")[:4] == GSI_TYPE:
            subprocess.run("adb reboot bootloader", shell=True)
            subprocess.run("fastboot reboot fastboot", shell=True)
            subprocess.run("fastboot flash system  %s" % gsi_imgs[0], shell=True)  # fmt: skip
            subprocess.run("fastboot reboot", shell=True)
        # break
        return


if __name__ == "__main__":
    try:
        main()
        sys.stdout.writelines("%s" % "all done!!")

    except Exception as exc:
        sys.stdout.writelines("%s" % exc)
        raise exc
