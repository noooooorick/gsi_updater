import os
import sys
import glob
import pathlib
import subprocess


IMG: str = ".img"
DOT_XZ: str = ".xz"
IMG_XZ: list[str, str] = ["img", "xz"]
GSI_TYPE: list[str, str] = ["aosp", "arm64", "ab", "gapps"]


def search_gsi_img() -> tuple[bool, list[str, str]]:
    try:
        current_work_dir = os.getcwd()
        gsi_img_xz = list(
            filter(
                lambda gsi: pathlib.Path(gsi).suffix == DOT_XZ,
                glob.glob(current_work_dir + "/**", recursive=True)  # fmt: skip
            )
        )
        return True, gsi_img_xz
    except Exception:
        return False, None


def main():
    ret, gsi_imgs = search_gsi_img()
    if ret and gsi_imgs is not None:
        for gsi_img in reversed(gsi_imgs):

            if gsi_img.split(".")[-2:] == IMG_XZ:
                subprocess.run(["unxz", f"{gsi_img}"], shell=True)

            # if gsi_img.split("/")[-1].split("-")[:4] == GSI_TYPE:
            #     subprocess.run(["adb", "reboot", "bootloader"], shell=True)
            #     subprocess.run(["fastboot", "reboot", "fastboot"], shell=True)
            #     subprocess.run(["fastboot flash", "system", f"{gsi_img}"])
            #     subprocess.run(["fastboot", "reboot"], shell=True)


if __name__ == "__main__":
    try:
        main()
        sys.stdout.writelines("%s" % "all done!!")

    except Exception as exc:
        sys.stdout.writelines("%s" % exc)
        raise exc
