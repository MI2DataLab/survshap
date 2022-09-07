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
