class Dimension:
    def __init__(self, name, value=None, tolerance=None):
        self.name = name
        self.value = value
        self.tolerance = tolerance

    def __repr__(self):
        return f"Dimension(name={self.name}, value={self.value}, tolerance={self.tolerance})"