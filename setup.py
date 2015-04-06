from distutils.core import setup

setup(
    name="KegPi",
    version="0.1",

    author="Bradley Brockman",
    author_email="bradbrok@gmail.com",
    url="https://github.com/bradbrok/KegPi",

    license="MIT_License.txt",
    description="Keg control system built on a Raspberry Pi.",

    install_requires=[
        "flask",
        "FlaskWTF",
    ],
)