# survshap

<!-- badges: start -->
<!-- badges: end -->

## Overview 
The `survshap` package contains an implementation of the **SurvSHAP(t)** method, the first time-dependent explanation method for interpreting survival black-box models. It is based on SHapley Additive exPlanations (SHAP) but extends it to the time-dependent setting of survival analysis. SurvSHAP(t) is able to detect time-dependent variable effects and its aggregation determines the local variable importance.

Read more about SurvSHAP(t) in [our paper](https://doi.org/10.1016/j.knosys.2022.110234).

## Installation
**You can install the package from [PyPI](https://pypi.org/project/survshap/):**
```
pip install survshap
```

**NOTE:** SurvSHAP(t) is also implemented in the [*survex*](https://github.com/ModelOriented/survex) R package, along with many more explanation methods for survival models. *survex* offers explanations for *scikit-survival* models loaded into R via the *reticulate* package.

## Citation
If you use this package, please cite our paper:
    
```bib
@article{survshap,
    title = {SurvSHAP(t): Time-dependent explanations of machine learning survival models},
    journal = {Knowledge-Based Systems},
    volume = {262},
    pages = {110234},
    year = {2023},
    issn = {0950-7051}
    }
```

## Basic usage
```python
# import packages and load data
from survshap import SurvivalModelExplainer, PredictSurvSHAP, ModelSurvSHAP
from sksurv.ensemble import RandomSurvivalForest # or any other survival model
# X, y - data

# prepare survival model
model = RandomSurvivalForest()
model.fit(X, y)

# create explainer
explainer = SurvivalModelExplainer(model = model, data = X, y = y)

# compute SHAP values for a single instance
observation_A = X.iloc[[0]]
survshap_A = PredictSurvSHAP()
survshap_A.fit(explainer = explainer, new_observation = observation_A)

survshap_A.result 
survshap_A.plot()

# compute SHAP values for a group of instances
model_survshap = ModelSurvSHAP(calculation_method="treeshap") # fast implementation for tree-based models
model_survshap.fit(explainer = explainer, new_observations = X)

model_survshap.result
model_survshap.plot_mean_abs_shap_values()
model_survshap.plot_shap_lines_for_all_individuals(variable = "variable1")
extracted_survshap = model_survshap.individual_explanations[0] # PredictSurvSHAP object
```



