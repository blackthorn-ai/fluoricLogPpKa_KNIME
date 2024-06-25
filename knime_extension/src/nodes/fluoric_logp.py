import logging

import pandas as pd
import knime.extension as knext

from categories import fluoric_category
from utils.fluoriclogpka_utils import predict_logP
from exceptions.fluoriclogppka_exceptions import InvalidSettingsException

LOGGER = logging.getLogger(__name__)

@knext.node(name="Fluoric logP", node_type=knext.NodeType.LEARNER, icon_path="icons/chem_icon.png", category=fluoric_category)
@knext.input_port(name="Input SMILES Data", description="Table with SMILES in 'string' of 'SMI' format", port_type=knext.PortType.TABLE)
@knext.output_table(name="Output Data", description="Table with predicted logP values")
class Fluoriclogp:
    """Node for predicting logP using molecules SMILES.
    
    For predicting are used a lot of generated molecule features using the most important and not correlated features from mordred (partial positive surface area, 
    partial negative surface area, number of fluorine or carbon atoms etc.), rdkit (number of cycles, chiral centers etc) and 
    custom calculation (dihedral angle, molecular weight and volume, dipole moment, sasa, functional group freedom etc).
    All this molecule features used for predicting logP values using ML models.
    """
    class ExecutionTimeOptions(knext.EnumParameterOptions):
        FAST = ("Fast/Inaccurate", "Generates less conformers for feature generation. Results in faster prediction, but with less accurate results.")
        SLOW = ("Slow/Accurate", "Generates 3^(number of double bonds) conformers for feature generation. Results in slower prediction, but better accurate results.")
        EXPERIMENTAL = ("Experimental - Fast/Accurate", "Graph neural network with features that are generated very quickly is used for prediction. The results are even better than other modes.")
    
    execution_mode = knext.EnumParameter(
        "Execution time",
        "How to execute feature generation.",
        ExecutionTimeOptions.EXPERIMENTAL.name,
        ExecutionTimeOptions,
    )

    selected_SMILES_col = knext.ColumnParameter(
        "SMILES column:",
        "Select the column containing SMILES.",
        column_filter= lambda col: True,
        include_row_key=False,
        include_none_column=False,
    )

    def __init__(self) -> None:
        
        self.smiles_column_name = None

    def configure(self, configure_context, input_schema_1):
        
        input_schema_1 = input_schema_1.append(knext.Column(knext.double(), "logP"))

        return input_schema_1

    def execute(self, exec_context, input_1):
        input_pandas = input_1.to_pandas()

        self.smiles_column_name = self.selected_SMILES_col
        if self.smiles_column_name is None:
            LOGGER.error(f"No column is selected.")
            raise InvalidSettingsException(f"Please specify a column.")

        selected_column_type = str(input_pandas.dtypes[self.selected_SMILES_col])
        is_smiles_column = "smiles" in selected_column_type.lower()
        if not is_smiles_column:
            LOGGER.error(f"Invalid SMILES column.")
            raise ValueError(f"The input data type is {selected_column_type} instead of SMILES. Please type cast.")

        LOGGER.info(f"Execution mode: {self.execution_mode}.")

        is_fast_mode = False
        model_name = "h2o"
        if self.ExecutionTimeOptions.FAST.name == self.execution_mode:
            LOGGER.info(f"FAST mode lauched.")
            is_fast_mode = True
        if self.ExecutionTimeOptions.EXPERIMENTAL.name == self.execution_mode:
            model_name = "gnn"

        LOGGER.info(f"SMILES column name: {self.smiles_column_name}, selected column name: {self.selected_SMILES_col}")

        SMILES_array = input_pandas[self.smiles_column_name]
        
        total_number_of_operations = len(SMILES_array) * 2
        
        predicted_logPs = []
        for index, SMILES in enumerate(SMILES_array):
            predicted_logP = None
            if pd.isnull(SMILES):
                LOGGER.warning(f"Empty cell.")
            else:
                try:
                    predicted_logP = predict_logP(
                        SMILES=SMILES,
                        is_fast_mode=is_fast_mode,
                        model_name=model_name,
                        execution_context=exec_context,
                        index=index * 2,
                        total_number_of_operations=total_number_of_operations
                    )
                except Exception as e:
                    LOGGER.error(f"Error predicting logP for SMILES '{SMILES}'")
                    raise ValueError(f"Couldn't parse, invalid SMILES: {SMILES}")
            
            predicted_logPs.append(predicted_logP)

        output_df = input_pandas.copy()
        output_df['logP'] = predicted_logPs
        
        return knext.Table.from_pandas(output_df)
