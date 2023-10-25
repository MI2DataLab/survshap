class SurvivalModelExplainer:
    def __init__(
        self,
        model,
        data=None,
        y=None,
        predict_survival_function=None,
        predict_cumulative_hazard_function=None,
    ):
        self.model = model
        self.data = data
        self.y = y
        self.predict_survival_function = predict_survival_function
        self.predict_cumulative_hazard_function = predict_cumulative_hazard_function

    def predict(self, data, function_type):
        if function_type == "sf":
            if self.predict_survival_function is not None:
                return self.predict_survival_function(self.model, data)
            elif hasattr(self.model, "predict_survival_function"):
                return self.model.predict_survival_function(data)
            else:
                raise ValueError("Pass a predict survival function to `SurvivalModelExplainer`,\
                    e.g. `predict_survival_function=lambda m, d: m.predict_survival_function(d)`.")
        elif function_type == "chf":
            if self.predict_cumulative_hazard_function is not None:
                return self.predict_cumulative_hazard_function(self.model, data)
            elif hasattr(self.model, "predict_cumulative_hazard_function"):
                return self.model.predict_cumulative_hazard_function(data)
            else:
                raise ValueError("Pass a predict cumulative hazard function to `SurvivalModelExplainer`,\
                    e.g. `predict_cumulative_hazard_function=lambda m, d: m.predict_cumulative_hazard_function(d)`.")         
        else:
            raise ValueError("function type needs to be one of `sf` or `chf`")
