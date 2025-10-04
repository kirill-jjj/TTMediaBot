#!/usr/bin/env python3

import bs4
import patoolib
import requests

import os
import platform
import re
import shutil
import sys

path = os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(path)
sys.path.append(path)
import downloader


url = "https://api.github.com/repos/shinchiro/mpv-winbuild-cmake/releases/latest"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}

def download():
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    release_info = r.json()
    assets = release_info["assets"]
    
    arch = platform.architecture()[0][0:2]
    
    download_url = None
    for asset in assets:
        if arch == "64" and "x86_64" in asset["name"] and "mpv-dev" in asset["name"] and asset["name"].endswith(".7z"):
            download_url = asset["browser_download_url"]
            break
        elif arch == "32" and "i686" in asset["name"] and "mpv-dev" in asset["name"] and asset["name"].endswith(".7z"):
            download_url = asset["browser_download_url"]
            break
            
    if not download_url:
        sys.exit("Could not find a suitable libmpv download for your architecture.")
        
    downloader.download_file(download_url, os.path.join(path, "libmpv.7z"))

def extract():
    temp_path = os.path.join(path, "libmpv")
    try:
        os.mkdir(temp_path)
    except FileExistsError:
        shutil.rmtree(temp_path)
        os.mkdir(temp_path)
    patoolib.extract_archive(
        os.path.join(path, "libmpv.7z"),
        outdir=temp_path,
    )

def move_file():
    source = os.path.join(path, "libmpv", "libmpv-2.dll")
    dest = os.path.join(path, "libmpv-2.dll")
    if os.path.exists(dest):
        os.remove(dest)
    shutil.move(source, dest)

def clean():
    os.remove(os.path.join(os.getcwd(), "libmpv.7z"))
    shutil.rmtree(os.path.join(os.getcwd(), "libmpv"))

def install():
    if sys.platform != "win32":
        sys.exit("This script should be run only on Windows")
    print("Installing libmpv for Windows...")
    print("Downloading latest libmpv version...")
    download()
    print("Downloaded")
    print("extracting...")
    extract()
    print("extracted")
    print("moving...")
    move_file()
    print("moved")
    print("cleaning...")
    clean()
    print("cleaned.")
    print("Installed, exiting.")

if __name__ == "__main__":
    install()
