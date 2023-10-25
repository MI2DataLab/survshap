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
