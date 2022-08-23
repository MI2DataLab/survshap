# SurvSHAP(t)
This repository contains data and code for the article:

M. Krzyziński, M. Spytek, H. Baniecki, P. Biecek. ***SurvSHAP(t): Time-dependent explanations of machine learning survival models***


<hr/>

Python version: 3.10.5

### Methods 
- `SurvSHAP` directory contains the SurvSHAP(t) method implementation (NOTE: it can be installed as package - `setup.py`) 
- `survLIME.py` is the SurvLIME method implementation

### Data
- `data_generation.R` is the code for synthetic censored data generation (for Experiments 1 and 2)
- `data` directory contains the datasets used in experiments

### Experiments
- `*.ipynb` are notebooks with code of the conducted experiments 
- `results` directory contains results of the conducted experiments

### Plots
- `plots.R` is the code for creating Figures from the article
- `plots` directory contains Figures in `.pdf` format
