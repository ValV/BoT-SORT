#!/usr/bin/env python
# Copyright (c) Megvii, Inc. and its affiliates. All Rights Reserved

import re
import setuptools
import glob

from os import path

import torch

from torch.utils.cpp_extension import CppExtension
from setuptools.command.build_ext import build_ext as _build_ext


torch_ver = [int(x) for x in torch.__version__.split(".")[:2]]
assert torch_ver >= [1, 3], "Requires PyTorch >= 1.3"


class BuildVideoCameraCorrection(_build_ext):
    def run(self):
        print("Building VideoCameraCorrection...")
        super().run()


def get_extensions():
    this_dir = path.dirname(path.abspath(__file__))
    extensions_dir = path.join(
        this_dir, "VideoCameraCorrection", "VideoCameraCorrection"
    )

    main_source = path.join(extensions_dir, "main.cpp")
    sources = glob.glob(path.join(extensions_dir, "**", "*.cpp"))

    sources = list(set([main_source] + sources))
    extension = CppExtension

    extra_compile_args = {"cxx": ["-std=c++17", "-O0"]}
    define_macros = []

    include_dirs = [extensions_dir, "/usr/local/include/opencv4"]
    library_dirs = ["/usr/local/lib"]

    ext_modules = [
        extension(
            "VideoCameraCorrection._C",
            sources,
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            libraries=[
                "opencv_core",
                "opencv_imgcodecs",
                "opencv_calib3d",
                "opencv_highgui",
                "opencv_videostab",
                "opencv_imgproc",
                "opencv_features2d",
                "opencv_optflow",
                "opencv_tracking",
                "stdc++fs",
            ],
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
        )
    ]

    return ext_modules


with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="VideoCameraCorrection",
    version="0.1.0",
    author="basedet team",
    python_requires=">=3.6",
    long_description=long_description,
    ext_modules=get_extensions(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmdclass={"build_ext": BuildVideoCameraCorrection},
    packages=setuptools.find_namespace_packages(),
    install_requires=[
        "torch>=1.3",
        "numpy",
        "opencv-python",
        "scipy",
        "scikit-image",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": []},
)
