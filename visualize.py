import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_payoff_matrix(model, title="Payoff Matrix"):
    """
    Create a visualization of the payoff matrix without using seaborn
    """
    # Create the payoff matrix
    try:
        # For 2x2 games (most common)
        p1_matrix = np.zeros((2, 2))
        p2_matrix = np.zeros((2, 2))
        text_matrix = []
        
        # Get the payoffs for each combination
        for i, a1 in enumerate([0, 1]):
            text_row = []
            for j, a2 in enumerate([0, 1]):
                p1, p2 = model.play(a1, a2)
                p1_matrix[i, j] = p1
                p2_matrix[i, j] = p2
                text_row.append(f"{p1}, {p2}")
            text_matrix.append(text_row)
        
        # Get action labels (if they exist)
        row_labels = getattr(model, 'row_labels', ['Action 0', 'Action 1'])
        col_labels = getattr(model, 'col_labels', ['Action 0', 'Action 1'])
        
        # Create a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Hide axes
        ax.axis('tight')
        ax.axis('off')
        
        # Create a table
        table = ax.table(
            cellText=text_matrix,
            rowLabels=row_labels,
            colLabels=col_labels,
            cellLoc='center',
            loc='center',
            bbox=[0.2, 0.2, 0.6, 0.6]  # [left, bottom, width, height]
        )
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        
        # Color cells based on Player 1's payoff
        min_payoff = np.min(p1_matrix)
        max_payoff = np.max(p1_matrix)
        payoff_range = max_payoff - min_payoff if max_payoff > min_payoff else 1
        
        # Add color to cells
        for i in range(2):
            for j in range(2):
                # Normalize payoff to [0, 1] for color scaling
                normalized_payoff = (p1_matrix[i, j] - min_payoff) / payoff_range
                # Create a blue color with intensity based on the payoff
                cell_color = (0.9 - 0.5 * normalized_payoff, 0.9 - 0.2 * normalized_payoff, 1.0)
                table[(i+1, j)].set_facecolor(cell_color)
        
        plt.title(title, fontsize=14)
        
        return fig
    
    except Exception as e:
        st.warning(f"Could not generate payoff matrix: {str(e)}")
        return None

def get_game_labels(model_name):
    """
    Return appropriate action labels for different games
    """
    if model_name == "Prisoner's Dilemma":
        return ["Cooperate", "Betray"], ["Cooperate", "Betray"]
    elif model_name == "Stag Hunt":
        return ["Hunt Stag", "Hunt Hare"], ["Hunt Stag", "Hunt Hare"]
    elif model_name == "Coordination Game":
        return ["Option A", "Option B"], ["Option A", "Option B"]
    elif model_name == "Hawk-Dove Game":
        return ["Hawk", "Dove"], ["Hawk", "Dove"]
    elif model_name == "Battle of Sexes":
        return ["Opera", "Football"], ["Opera", "Football"]
    else:
        return ["Action 0", "Action 1"], ["Action 0", "Action 1"]
    
    return fig

def get_game_labels(model_name):
    """
    Return appropriate action labels for different games
    """
    if model_name == "Prisoner's Dilemma":
        return ["Cooperate", "Betray"], ["Cooperate", "Betray"]
    elif model_name == "Stag Hunt":
        return ["Hunt Stag", "Hunt Hare"], ["Hunt Stag", "Hunt Hare"]
    elif model_name == "Coordination Game":
        return ["Option A", "Option B"], ["Option A", "Option B"]
    elif model_name == "Hawk-Dove Game":
        return ["Hawk", "Dove"], ["Hawk", "Dove"]
    elif model_name == "Battle of Sexes":
        return ["Opera", "Football"], ["Opera", "Football"]
    else:
        return ["Action 0", "Action 1"], ["Action 0", "Action 1"]
