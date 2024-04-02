class InvalidSettingsException(Exception):
    def __init__(self, message="Input schema does not contain the 'SMILES' column"):
        self.message = message
        super().__init__(self.message)
