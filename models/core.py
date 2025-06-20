import numpy as np

class GameModel:
    """
    Base class for game models. All specific models should inherit from this class.
    """
    name = "Base Game"
    description = "Base class for game models"
    row_labels = ["Action 0", "Action 1"]
    col_labels = ["Action 0", "Action 1"]

    def __init__(self, params=None):
        self.params = params or {}

    def play(self):
        """Run a game and return the result."""
        raise NotImplementedError

    def summary(self):
        """Return a brief description of the model."""
        return self.description
      
    def get_payoff_matrix(self):
        """
        Return the payoff matrix for the game.
        Should be overridden by subclasses for custom implementations.
        """
        try:
            # Default implementation for 2x2 games
            results = []
            for a1 in [0, 1]:
                row = []
                for a2 in [0, 1]:
                    payoffs = self.play(a1, a2)
                    row.append(f"{payoffs[0]}, {payoffs[1]}")
                results.append(row)
            
            # Ensure we return a 2D array
            matrix = np.array(results)
            if matrix.shape != (2, 2):
                # If we don't have a 2x2 matrix, create a default one
                matrix = np.array([["0, 0", "0, 0"], ["0, 0", "0, 0"]])
            
            return matrix
            
        except Exception as e:
            # Return a default 2x2 matrix in case of any error
            return np.array([["0, 0", "0, 0"], ["0, 0", "0, 0"]])
