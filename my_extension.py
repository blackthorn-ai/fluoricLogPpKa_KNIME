import logging
import math

import pandas as pd
import knime.extension as knext

from utils import predict_logP, predict_pKa

LOGGER = logging.getLogger(__name__)

@knext.node(name="Fluoriclogppka Node", node_type=knext.NodeType.LEARNER, icon_path="icon.png", category="/")
@knext.input_table(name="Input SMILES Data", description="Table with SMILES in 'string' of 'SMI' format")
@knext.output_table(name="Output Data", description="Table with predicted pKa and logP values")
class FluoriclogppkaNode:
    """Tool for predicting logP, pKa using molecules SMILES.
    For predicting are used a lot of generated molecule features, such as dihedral angle, molecular weight and volume, amount of Carbon atoms etc.
    All this molecule features used for predicting two values - pKa, logP using H2O models.
    """
    
    boolean_pka_param = knext.BoolParameter("Predict pKa", "Checkbox parameter in case you want to predict the pKa value or not", True)
    boolean_logp_param = knext.BoolParameter("Predict logP", "Checkbox parameter in case you want to predict the logP value or not", True)


    def configure(self, configure_context, input_schema_1):
        
        input_schema_1 = input_schema_1.append(knext.Column(knext.double(), "logP"))
        input_schema_1 = input_schema_1.append(knext.Column(knext.double(), "pKa"))

        return input_schema_1

 
    def execute(self, exec_context, input_1):
        input_pandas = input_1.to_pandas()

        predicted_logPs = []
        predicted_pKas = []
        for _, row in input_pandas.iterrows():
            if pd.isnull(row['SMILES']):
                raise ValueError("SMILES cannot be NaN")

            SMILES = row['SMILES']

            if self.boolean_pka_param is True:
                predicted_pKa = predict_pKa(SMILES=SMILES)
                predicted_pKas.append(predicted_pKa)
            
            if self.boolean_logp_param is True:
                predicted_logP = predict_logP(SMILES=SMILES)
                predicted_logPs.append(predicted_logP)

        output_df = pd.DataFrame({
            'SMILES': input_pandas['SMILES'],
            'logP': predicted_logPs if self.boolean_logp_param else [math.nan for i in range(len(input_pandas['SMILES']))],
            'pKa': predicted_pKas if self.boolean_pka_param else [math.nan for i in range(len(input_pandas['SMILES']))]
        })
        
        return knext.Table.from_pandas(output_df)
