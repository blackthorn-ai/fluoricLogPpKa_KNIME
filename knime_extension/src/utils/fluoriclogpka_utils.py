import fluoriclogppka

def predict_pKa(SMILES: str,
                is_fast_mode: bool = False,
                execution_context=None,
                index: int = None,
                total_number_of_operations: int = None) -> float:
    """
    Predicts the pKa value for a given single SMILES string.

    Args:
        SMILES (str): The SMILES representation of the molecule.
        is_fast_mode (bool, optional): Whether to use fast mode for inference.
        execution_context (object, optional): Context object for tracking execution progress.
        index (int, optional): Index of the current operation.
        total_number_of_operations (int, optional): Total number of operations.

    Returns:
        float: Predicted pKa value.
    """
    if execution_context is not None:
        execution_context.set_progress(progress=(index + 1)/total_number_of_operations,
                                       message=f"Features generating for: {SMILES}")
    

    inference_pKa = fluoriclogppka.Inference(SMILES=SMILES,
                                             target_value=fluoriclogppka.Target.pKa,
                                             is_fast_mode=is_fast_mode)
    
    if execution_context is not None:
        execution_context.set_progress(progress=(index + 2)/total_number_of_operations,
                                       message=f"pKa prediction for: {SMILES}")
    return inference_pKa.predict()

def predict_logP(SMILES: str,
                 is_fast_mode: bool = False,
                 execution_context=None,
                 index: int = None,
                 total_number_of_operations: int = None) -> float:
    """
    Predicts the logP value for a given single SMILES string.

    Args:
        SMILES (str): The SMILES representation of the molecule.
        is_fast_mode (bool, optional): Whether to use fast mode for inference.
        execution_context (object, optional): Context object for tracking execution progress.
        index (int, optional): Index of the current operation.
        total_number_of_operations (int, optional): Total number of operations.

    Returns:
        float: Predicted logP value.
    """
    if execution_context is not None:
        execution_context.set_progress(progress=(index + 1)/total_number_of_operations,
                                       message=f"Features generating for: {SMILES}")

    inference_logP = fluoriclogppka.Inference(SMILES=SMILES,
                                              target_value=fluoriclogppka.Target.logP,
                                              is_fast_mode=is_fast_mode)
    
    if execution_context is not None:
        execution_context.set_progress(progress=(index + 2)/total_number_of_operations,
                                       message=f"pKa prediction for: {SMILES}")
    return inference_logP.predict()
