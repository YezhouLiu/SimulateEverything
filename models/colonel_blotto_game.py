from .core import GameModel
import numpy as np

class ColonelBlottoGame(GameModel):
    name = "Colonel Blotto Game"
    description = "A classic game of strategic resource allocation across multiple battlefields. Players must distribute limited resources, with the player allocating more to a battlefield winning that field."

    def __init__(self, resources=10, battlefields=3):
        super().__init__({
            'resources': resources,
            'battlefields': battlefields
        })
    
    def play(self, allocation1, allocation2):
        """
        Play the Colonel Blotto game
        
        allocation1, allocation2: lists of resource allocations for each battlefield
        
        Returns the number of battlefields won by each player and a list of battlefield results
        """
        resources = self.params['resources']
        battlefields = self.params['battlefields']
        
        # Validate allocations
        if not isinstance(allocation1, list) or not isinstance(allocation2, list):
            raise ValueError("Allocations must be lists")
        
        if len(allocation1) != battlefields or len(allocation2) != battlefields:
            raise ValueError(f"Allocations must have exactly {battlefields} elements")
        
        if sum(allocation1) > resources or sum(allocation2) > resources:
            raise ValueError(f"Total resources cannot exceed {resources}")
        
        if any(x < 0 for x in allocation1) or any(x < 0 for x in allocation2):
            raise ValueError("Allocations cannot be negative")
        
        # Determine the winner of each battlefield
        battlefield_results = []
        wins1 = 0
        wins2 = 0
        
        for i in range(battlefields):
            if allocation1[i] > allocation2[i]:
                battlefield_results.append(1)  # Player 1 wins
                wins1 += 1
            elif allocation2[i] > allocation1[i]:
                battlefield_results.append(2)  # Player 2 wins
                wins2 += 1
            else:
                battlefield_results.append(0)  # Tie
        
        return wins1, wins2, battlefield_results
    
    def play_simple(self, strategy1, strategy2):
        """
        Simplified interface for playing the game with predefined strategies
        
        strategy1, strategy2: 
            0 = Equal allocation
            1 = Focus on first battlefield
            2 = Focus on last battlefield
            3 = Random allocation
        
        Returns the number of battlefields won by each player
        """
        resources = self.params['resources']
        battlefields = self.params['battlefields']
        
        # Generate allocations based on strategies
        allocation1 = self._generate_allocation(strategy1)
        allocation2 = self._generate_allocation(strategy2)
        
        wins1, wins2, _ = self.play(allocation1, allocation2)
        return wins1, wins2
    
    def _generate_allocation(self, strategy):
        """Generate resource allocation based on strategy"""
        resources = self.params['resources']
        battlefields = self.params['battlefields']
        
        if strategy == 0:  # Equal allocation
            base_alloc = resources // battlefields
            remainder = resources % battlefields
            allocation = [base_alloc] * battlefields
            
            # Distribute remainder
            for i in range(remainder):
                allocation[i] += 1
                
        elif strategy == 1:  # Focus on first battlefield
            allocation = [0] * battlefields
            allocation[0] = int(0.6 * resources)  # 60% to first battlefield
            
            # Distribute remaining evenly
            remaining = resources - allocation[0]
            base_alloc = remaining // (battlefields - 1) if battlefields > 1 else 0
            allocation[1:] = [base_alloc] * (battlefields - 1)
            
            # Distribute remainder
            remainder = remaining % (battlefields - 1) if battlefields > 1 else 0
            for i in range(1, 1 + remainder):
                allocation[i] += 1
                
        elif strategy == 2:  # Focus on last battlefield
            allocation = [0] * battlefields
            allocation[-1] = int(0.6 * resources)  # 60% to last battlefield
            
            # Distribute remaining evenly
            remaining = resources - allocation[-1]
            base_alloc = remaining // (battlefields - 1) if battlefields > 1 else 0
            allocation[:-1] = [base_alloc] * (battlefields - 1)
            
            # Distribute remainder
            remainder = remaining % (battlefields - 1) if battlefields > 1 else 0
            for i in range(remainder):
                allocation[i] += 1
                
        elif strategy == 3:  # Random allocation
            # Generate random distribution that sums to resources
            allocation = np.zeros(battlefields, dtype=int)
            for _ in range(resources):
                idx = np.random.randint(0, battlefields)
                allocation[idx] += 1
                
        else:
            raise ValueError("Invalid strategy")
        
        return allocation.tolist() if isinstance(allocation, np.ndarray) else allocation
    
    def get_strategy_name(self, strategy):
        """Return the name of a strategy"""
        strategy_names = {
            0: "Equal Distribution",
            1: "Front-Loaded",
            2: "Back-Loaded",
            3: "Random Distribution"
        }
        return strategy_names.get(strategy, "Unknown Strategy")
