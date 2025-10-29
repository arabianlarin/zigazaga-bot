import pandas as pd
import duckdb
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from sklearn.preprocessing import MinMaxScaler
import fpl_api as fa
from datasets import get_player_data
import matplotlib.pyplot as plt
import numpy as np

def chart_player_comparison_att(player1, player2):
    global data
    data = get_player_data()
    metrics = ["Sh_per_90_Standard", 'SoT_per_90_Standard', 'G+A_Per', 
               "xG_Expected", "xA_Expected", 'KP', 'creativity', 'threat']
    
    scaler = MinMaxScaler()
    df_scaled = data.copy()
    df_scaled[metrics] = scaler.fit_transform(data[metrics])
    
    p1 = df_scaled[df_scaled["name_norm"] == player1.lower()][metrics].values.flatten()
    p2 = df_scaled[df_scaled["name_norm"] == player2.lower()][metrics].values.flatten()
    
    # Labels for the radar chart
    labels = ['Shots/90', 'Shots on Target/90', 'G+A/90', 'xG/90', 
              'xA/90', 'Key Passes/90', 'Creativity', 'Threat']
    
    # Number of variables
    num_vars = len(labels)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Close the plot by appending the first value
    p1 = list(p1) + [p1[0]]
    p2 = list(p2) + [p2[0]]
    angles += angles[:1]
    labels_closed = labels + [labels[0]]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot player 1
    ax.plot(angles, p1, 'o-', linewidth=3, label=player1, color='#D62E0F')
    ax.fill(angles, p1, alpha=0.3, color='#DB5B42')
    
    # Plot player 2
    ax.plot(angles, p2, 'o-', linewidth=3, label=player2, color='#120FD6')
    ax.fill(angles, p2, alpha=0.3, color='#4F4ED9')
    
    # Fix axis to go from 0 to 1
    ax.set_ylim(0, 1)
    
    # Set the labels for each axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=10)
    
    # Remove radial labels (0.2, 0.4, etc.) or make them less visible
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([])  # Hide the radial tick labels
    
    # Add grid
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=False, fontsize=12)
    
    # Title
    # plt.title(f"{player1} vs {player2}", size=16, y=1.08)
    
    plt.tight_layout()
    
    # Save file
    file_path = f"comparison_{player1}_{player2}.png"
    plt.savefig(file_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return file_path

def chart_player_comparison_def(player1, player2):
    #global data
    #data = get_player_data()
    metrics = ["TklW_Tackles", 'Blocks_Blocks', 'Int', "Clr", "defensive_contribution_per_90", 'CBIT/90', 'CS_percent', 'Err', 'expected_goals_conceded_per_90']
    
    scaler = MinMaxScaler()
    
    df_scaled = data.copy()
    df_scaled[metrics] = scaler.fit_transform(data[metrics])
    
    p1 = df_scaled[df_scaled["name_norm"] == player1.lower()][metrics].values.flatten()
    p2 = df_scaled[df_scaled["name_norm"] == player2.lower()][metrics].values.flatten()

    labels = ['Tackles Won/90', 'Blocks/90', 'Interceptions/90', 'Clearances/90', 'DefCon/90', 'CBIT/90', 'Clean Sheets %', 'Errors Lead to Shot/90', 'xGC']
    
    num_vars = len(labels)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Close the plot by appending the first value
    p1 = list(p1) + [p1[0]]
    p2 = list(p2) + [p2[0]]
    angles += angles[:1]
    labels_closed = labels + [labels[0]]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot player 1
    ax.plot(angles, p1, 'o-', linewidth=3, label=player1, color='#D62E0F')
    ax.fill(angles, p1, alpha=0.3, color='#DB5B42')
    
    # Plot player 2
    ax.plot(angles, p2, 'o-', linewidth=3, label=player2, color='#120FD6')
    ax.fill(angles, p2, alpha=0.3, color='#4F4ED9')
    
    # Fix axis to go from 0 to 1
    ax.set_ylim(0, 1)
    
    # Set the labels for each axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=10)
    
    # Remove radial labels (0.2, 0.4, etc.) or make them less visible
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([])  # Hide the radial tick labels
    
    # Add grid
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=False, fontsize=12)
    
    # Title
    # plt.title(f"{player1} vs {player2}", size=16, y=1.08)
    
    plt.tight_layout()
    
    # Save file
    file_path = f"comparison_{player1}_{player2}.png"
    plt.savefig(file_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return file_path

def chart_player_comparison_gk(player1, player2):
    #global data
    #data = get_player_data()
    metrics = ["Save_percent", 'CS_percent', 'Save_percent_Penalty', "Err", 'expected_goals_conceded_per_90']
    
    scaler = MinMaxScaler()
    
    df_scaled = data.copy()
    df_scaled[metrics] = scaler.fit_transform(data[metrics])
    
    p1 = df_scaled[df_scaled["name_norm"] == player1.lower()][metrics].values.flatten()
    p2 = df_scaled[df_scaled["name_norm"] == player2.lower()][metrics].values.flatten()

    labels = ['Saves %/90', 'Clean Sheets %', 'Saved Penalties %', 'Errors Lead to Shot/90', 'xGC']
    
    num_vars = len(labels)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Close the plot by appending the first value
    p1 = list(p1) + [p1[0]]
    p2 = list(p2) + [p2[0]]
    angles += angles[:1]
    labels_closed = labels + [labels[0]]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot player 1
    ax.plot(angles, p1, 'o-', linewidth=3, label=player1, color='#D62E0F')
    ax.fill(angles, p1, alpha=0.3, color='#DB5B42')
    
    # Plot player 2
    ax.plot(angles, p2, 'o-', linewidth=3, label=player2, color='#120FD6')
    ax.fill(angles, p2, alpha=0.3, color='#4F4ED9')
    
    # Fix axis to go from 0 to 1
    ax.set_ylim(0, 1)
    
    # Set the labels for each axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=10)
    
    # Remove radial labels (0.2, 0.4, etc.) or make them less visible
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([])  # Hide the radial tick labels
    
    # Add grid
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=False, fontsize=12)
    
    # Title
    # plt.title(f"{player1} vs {player2}", size=16, y=1.08)
    
    plt.tight_layout()
    
    # Save file
    file_path = f"comparison_{player1}_{player2}.png"
    plt.savefig(file_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return file_path
