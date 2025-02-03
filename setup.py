from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import os
import subprocess

class CustomInstallCommand(install):
    """Customized setuptools install command - builds the Singularity container."""
    def run(self):
        # Call the standard install process first
        install.run(self)
        
        # Now build the Singularity container
        module_dir = os.path.dirname(os.path.realpath(__file__))
        def_file_path = os.path.join(module_dir, 'singularity/gtools.def')
        sif_file_path = os.path.join(module_dir, 'singularity/gtools.sif')

        command = ['singularity', 'build', '--fakeroot', '--force', sif_file_path, def_file_path]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(e)
            raise SystemExit(1)
        
class CustomDevelopCommand(develop):

    def run(self):
        # Call the standard install process first
        develop.run(self)
        
        # Now build the Singularity container
        module_dir = os.path.dirname(os.path.realpath(__file__))
        def_file_path = os.path.join(module_dir, 'singularity/gtools.def')
        sif_file_path = os.path.join(module_dir, 'singularity/gtools.sif')

        command = ['singularity', 'build', '--fakeroot', '--force', sif_file_path, def_file_path]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(e)
            raise SystemExit(1)
        

setup(
    name="GMRT_tools",
    version="0.1.0",
    author="Abhinav Narayan",
    author_email="abhinavnarayan7@gmail.com",
    description="A singularity container for GMRT tools",
    # long_description=open('README.md').read(),
    # long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/GMRT_tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # install_requires=[
    #     # List your project's dependencies here.
    #     # e.g., 'numpy', 'scipy', 'astropy'
    # ],
    entry_points={
        'console_scripts': [
            'gtools=gtools.main:main'
        ]
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand
    }
)