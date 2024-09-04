from setuptools import setup, find_packages

setup(
    name='slo_yaml_generator',
    version='0.0.7',
    author='Jack Fordyce',
    author_email='jackmitchellfordyce@gmail.com',
    description='Generate OpenSLO and Nobl9 yaml configuration',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jackmford/slo-yaml-generator',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "slo_yaml_generator": ["templates/*"],
    },
    entry_points={
            'console_scripts': [
                'slo_yaml_generator=slo_yaml_generator.main:main',
        ]
    },
    install_requires=[
        'Jinja2==3.1.4',
        'MarkupSafe==2.1.5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

