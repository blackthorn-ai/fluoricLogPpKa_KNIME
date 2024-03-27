import fluoriclogppka

def predict_pKa(SMILES: str,
                is_fast_mode: bool = False,
                execution_context=None,
                index: int = None,
                total_number_of_operations: int = None) -> float:
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
                 is_fast_mode: bool = False) -> float:
    inference_logP = fluoriclogppka.Inference(SMILES=SMILES,
                                              target_value=fluoriclogppka.Target.logP)
    
    return inference_logP.predict()
