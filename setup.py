def run_setup():
    from setuptools import setup, find_packages

    setup(
        name="survshap",
        maintainer="Mateusz Krzyziński",
        author="Mateusz Krzyziński",
        author_email="mateusz.krzyzinski.stud@pw.edu.pl",
        version="0.2.0",
        description="SurvSHAP(t): Time-dependent explanations of machine learning survival models",
        url="#",
        install_requires=[
            "setuptools",
            "scikit-survival>=0.17.2",
            "pandas>=1.2.5",
            "numpy>=1.20.3",
            "scipy>=1.6.3",
            "plotly>=5.1.0",
            "tqdm>=4.61.2",
            "statsmodels>=0.13.2",
        ],
        packages=find_packages(include=["survshap", "survshap.*"]),
        python_requires=">=3.7",
        include_package_data=True,
    )


if __name__ == "__main__":
    run_setup()
