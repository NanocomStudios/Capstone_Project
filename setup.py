from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.read()
    required_packages = [
        line.strip() 
        for line in content.splitlines() 
        if line.strip() and not line.startswith("-e")
    ]

setup(
    name="swift-logistics",
    version="0.1.0",
    packages=find_packages(),
    install_requires=required_packages,
    python_requires=">=3.8",
)