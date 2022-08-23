def run_setup():
    from setuptools import setup

    setup(
        name="SurvSHAP",
        maintainer="Mateusz Krzyziński",
        author="Mateusz Krzyziński",
        author_email="mateusz.krzyzinski.stud@pw.edu.pl",
        version="0.1.0",
        description="SurvSHAP(t): Time-Dependent Explanations Of Machine Learning Survival Models",
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
        packages=["SurvSHAP"],
        python_requires=">=3.7",
        include_package_data=True,
    )


if __name__ == "__main__":
    run_setup()
