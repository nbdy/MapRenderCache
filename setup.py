from setuptools import setup, find_packages
from setuptools.command.install import install
from os import system, listdir
from subprocess import check_output
from shutil import copyfile
from os.path import join


def build_copy_so():
    system("./build.sh")
    dist_path = check_output(["python3", "-m", "site", "--user-site"]).decode("utf-8").strip()
    for so in [fp for fp in listdir("build/") if fp.endswith(".so")]:
        copyfile(join("build", so), join(dist_path, so))


class BuildExtension(install):
    def run(self):
        install.run(self)
        build_copy_so()


setup(
    long_description=open("README.md", "r").read(),
    name="MapRenderCache",
    version="0.1",
    description="mapnik render cache",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/MapRenderCache",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords="mapnik render cache",
    packages=find_packages(),
    cmdclass={"install": BuildExtension},
    long_description_content_type="text/markdown"
)
