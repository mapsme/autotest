import setuptools

setuptools.setup(
    name='mapsme-appium',
    version='0.1',
    author="k.kravchuk",
    author_email="k.kravchuk@corp.mail.ru",
    description="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        '': ['*.ini'],
    },
)
