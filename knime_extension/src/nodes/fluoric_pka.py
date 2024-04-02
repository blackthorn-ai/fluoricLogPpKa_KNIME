import logging

import pandas as pd
import knime.extension as knext

from categories import fluoric_category
from utils.fluoriclogpka_utils import predict_pKa
from exceptions.fluoriclogppka_exceptions import InvalidSettingsException

LOGGER = logging.getLogger(__name__)

@knext.node(name="Fluorine pKa", node_type=knext.NodeType.LEARNER, icon_path="icons/chem_icon.png", category=fluoric_category)
@knext.input_port(name="Input SMILES Data", description="Table with SMILES in 'string' of 'SMI' format", port_type=knext.PortType.TABLE)
@knext.output_table(name="Output Data", description="Table with predicted pKa values")
class Fluoricpka:
    """Node for predicting pKa using molecules SMILES.
    
    For predicting are used a lot of generated molecule features using the most important and not correlated features from mordred (partial positive surface area, partial negative surface area, number of fluorine or carbon atoms etc.), 
    rdkit (number of cycles, chiral centers etc) and custom calculation (dihedral angle, molecular weight and volume, dipole moment, sasa, functional group freedom etc).
    All this molecule features used for predicting pKa values using ML models.
    """
    class ExecutionTimeOptions(knext.EnumParameterOptions):
        FAST = ("Fast/Inaccurate", "Generates less conformers for feature generation. Results in faster prediction, but with less accurate results.")
        SLOW = ("Slow/Accurate", "Generates 3^(number of double bonds) conformers for feature generation. Results in slower prediction, but better accurate results.")
    
    execution_mode = knext.EnumParameter(
        "Execution time",
        "How to execute feature generation.",
        ExecutionTimeOptions.SLOW.name,
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
        
        self.smiles_column_name = 'SMILES'

    def configure(self, configure_context, input_schema_1):
        
        input_schema_1 = input_schema_1.append(knext.Column(knext.double(), "pKa"))

        return input_schema_1
 
    def execute(self, exec_context, input_1):
        input_pandas = input_1.to_pandas()

        LOGGER.info(f"Execution mode: {self.execution_mode}.")

        is_fast_mode = False
        if self.ExecutionTimeOptions.FAST.name == self.execution_mode:
            LOGGER.info(f"FAST mode lauched.")
            is_fast_mode = True

        if self.selected_SMILES_col != None:
            self.smiles_column_name = self.selected_SMILES_col

        LOGGER.info(f"SMILES column name: {self.smiles_column_name}, selected column name: {self.selected_SMILES_col}")

        has_smiles_column = any(column == self.smiles_column_name for column in input_1.column_names)
        if not has_smiles_column:
            LOGGER.error(f"{self.smiles_column_name} column is not represented in the input table.")
            raise InvalidSettingsException(f"Input schema does not contain the '{self.smiles_column_name}' column. Please specify the column that contains SMILES.")

        SMILES_array = input_pandas[self.smiles_column_name]
        
        total_number_of_operations = len(SMILES_array) * 2
        
        predicted_pKas = []
        for index, SMILES in enumerate(SMILES_array):
            if pd.isnull(SMILES):
                LOGGER.error(f"SMILES value cannot be NaN.")
                raise ValueError("SMILES cannot be NaN.")

            try:
                predicted_pKa = predict_pKa(SMILES=SMILES,
                                            is_fast_mode=is_fast_mode,
                                            execution_context=exec_context,
                                            index=index * 2,
                                            total_number_of_operations=total_number_of_operations)
                
            except Exception as e:
                LOGGER.error(f"Error predicting pKa for SMILES '{SMILES}': {str(e)}")
                raise ValueError(f"Inappropriate SMILES format: {SMILES}")

            predicted_pKas.append(predicted_pKa)

        output_df = input_pandas.copy()
        output_df['pKa'] = predicted_pKas
        
        return knext.Table.from_pandas(output_df)
