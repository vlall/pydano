try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name="cardano_wrapper",
    version="0.1",
    description="A quick Python wrapper for Cardano executables to test integration matrices.",
    author="vlall",
    author_email="",
    install_requires=["nose2", "mnemonic", "requests", "pyyaml", "asyncio"],
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    test_suite="nose.collector",
)
