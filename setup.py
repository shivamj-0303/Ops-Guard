from setuptools import setup, find_packages

setup(
    name="opsguard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "GitPython",
        "docker",
        "fastapi",
        "uvicorn",
        "pydantic"
    ],
    entry_points={
        "console_scripts": [
            "opsguard=opsguard.cli.main:main"
        ]
    }
)