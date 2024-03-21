import fluoriclogppka

def predict_pKa(SMILES: str) -> float:
    inference_pKa = fluoriclogppka.Inference(SMILES=SMILES,
                                            target_value=fluoriclogppka.Target.pKa)
    
    return inference_pKa.predict()

def predict_logP(SMILES: str) -> float:
    inference_logP = fluoriclogppka.Inference(SMILES=SMILES,
                                            target_value=fluoriclogppka.Target.logP)
    
    return inference_logP.predict()
