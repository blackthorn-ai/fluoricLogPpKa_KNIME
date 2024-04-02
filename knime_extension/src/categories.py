import knime_extension as knext

main_category = knext.category(
    path="/community",
    level_id="chem-ai",
    name="Chem AI Extension",
    description="Nodes using artificial intelligence methods for prediction.",
    icon="icons/chem_ai_icon.png",
)

fluoric_category = knext.category(
    path=main_category,
    level_id="fluoric_logp_pka_predictors",
    name="Fluorine Predictor",
    description="Nodes for predicting chemical properties in fluorine molecules.",
    icon="icons/fluorine_icon.png",
)
