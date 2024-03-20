import logging
import math

import pandas as pd
import knime.extension as knext

from utils import predict_logP, predict_pKa

LOGGER = logging.getLogger(__name__)

@knext.node(name="Fluoric logP", node_type=knext.NodeType.LEARNER, icon_path="icons\chem_icon.png", category="/")
@knext.input_table(name="Input SMILES Data", description="Table with SMILES in 'string' of 'SMI' format")
@knext.output_table(name="Output Data", description="Table with predicted logP values")
class Fluoriclogp:
    """Node for predicting logP using molecules SMILES.
    For predicting are used a lot of generated molecule features, such as dihedral angle, molecular weight and volume, amount of Carbon atoms etc.
    All this molecule features used for predicting logP values using H2O models.
    """

    def configure(self, configure_context, input_schema_1):
        
        input_schema_1 = input_schema_1.append(knext.Column(knext.double(), "logP"))

        return input_schema_1

 
    def execute(self, exec_context, input_1):
        input_pandas = input_1.to_pandas()

        predicted_logPs = []
        for _, row in input_pandas.iterrows():
            if pd.isnull(row['SMILES']):
                raise ValueError("SMILES cannot be NaN")

            SMILES = row['SMILES']
            
            predicted_logP = predict_logP(SMILES=SMILES)
            predicted_logPs.append(predicted_logP)

        output_df = pd.DataFrame({
            'SMILES': input_pandas['SMILES'],
            'logP': predicted_logPs,
        })
        
        return knext.Table.from_pandas(output_df)


@knext.node(name="Fluoric pKa", node_type=knext.NodeType.LEARNER, icon_path="icons\chem_icon.png", category="/")
@knext.input_table(name="Input SMILES Data", description="Table with SMILES in 'string' of 'SMI' format")
@knext.output_table(name="Output Data", description="Table with predicted pKa values")
class Fluoricpka:
    """Node for predicting pKa using molecules SMILES.
    For predicting are used a lot of generated molecule features, such as dihedral angle, molecular weight and volume, amount of Carbon atoms etc.
    All this molecule features used for predicting pKa values using H2O models.
    """

    def configure(self, configure_context, input_schema_1):
        
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

            predicted_pKa = predict_pKa(SMILES=SMILES)
            predicted_pKas.append(predicted_pKa)


        output_df = pd.DataFrame({
            'SMILES': input_pandas['SMILES'],
            'pKa': predicted_pKas,
        })
        
        return knext.Table.from_pandas(output_df)
