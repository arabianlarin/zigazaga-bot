import pandas as pd
import duckdb
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from sklearn.preprocessing import MinMaxScaler
import fpl_api as fa
from datasets import get_dataset, get_player_data

def chart_player_comparison_att(player1, player2):
    global data
    data = get_player_data()
    metrics = ["Sh_per_90_Standard", 'SoT_per_90_Standard', 'G+A_Per', "xG_Expected", "xA_Expected", 'KP', 'creativity', 'threat']
    scaler = MinMaxScaler()
    df_scaled = data.copy()
    df_scaled[metrics] = scaler.fit_transform(data[metrics])
    p1 = df_scaled[df_scaled["Player"] == player1][metrics].values.flatten()
    p2 = df_scaled[df_scaled["Player"] == player2][metrics].values.flatten()

    ph1 = data.loc[data["Player"] == player1.strip(), "photo"].values[0]
    ph2 = data.loc[data["Player"] == player2.strip(), "photo"].values[0]
    
    metrics_closed = metrics + [metrics[0]]
    p1 = list(p1) + [p1[0]]
    p2 = list(p2) + [p2[0]]

    fig = make_subplots(
        rows=1, cols=3,
        column_widths=[0.25, 0.5, 0.25],
        specs=[[{"type": "xy"}, {"type": "polar"}, {"type": "xy"}]],
    )
    
    # --- Plotly radar chart ---
    # fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=p1,
        theta=['Shots/90', 'Shots on Target/90', 'G+A/90', 'xG/90', 'xA/90', 'Key Passes/90', 'Creativity', 'Threat'],
        fill='toself',
        name=player1,
        line=dict(color='#D62E0F', width=4),
        fillcolor='#DB5B42',
        opacity=0.5
    ), row=1, col=2)
    fig.add_trace(go.Scatterpolar(
        r=p2,
        theta=['Shots/90', 'Shots on Target/90', 'G+A/90', 'xG/90', 'xA/90', 'Key Passes/90', 'Creativity', 'Threat'],
        fill='toself',
        name=player2,
        line=dict(color='#120FD6', width=4),
        fillcolor='#4F4ED9',
        opacity=0.5
    ), row=1, col=2)
    
    fig.update_layout(
        polar=dict(radialaxis=dict(
            visible=True,
            range=[0, 1],
            color="black",          # ← makes the tick labels black
            tickfont=dict(color="rgba(0,0,0,0)")  # ← ensures tick text is black
        )),
        showlegend=True,
        legend=dict(
             orientation="h",      # horizontal layout
            x=0.5,                # center horizontally
            y=1.15,               # position above the chart
            xanchor="center",     # anchor at center
            yanchor="bottom",     # anchor at bottom of legend box
            bgcolor="rgba(0,0,0,0)"  # transparent background (optional) 
        ),
        #title=dict(text=f"{player1} vs {player2}", x=0.5, xanchor='center', font=dict(size=24)),
        width=500,  # 👈 increase size
        height=500, # 👈 increase size
        margin=dict(l=20, r=20, t=80, b=20)
    )

    return fig

def chart_player_comparison_def(player1, player2):
    #global data
    #data = get_player_data()
    metrics = ["TklW_Tackles", 'Blocks_Blocks', 'Int', "Clr", "defensive_contribution_per_90", 'CBIT/90', 'CS_percent', 'Err', 'expected_goals_conceded_per_90']
    scaler = MinMaxScaler()
    df_scaled = data.copy()
    df_scaled[metrics] = scaler.fit_transform(data[metrics])
    p1 = df_scaled[df_scaled["Player"] == player1][metrics].values.flatten()
    p2 = df_scaled[df_scaled["Player"] == player2][metrics].values.flatten()

    ph1 = data.loc[data["Player"] == player1, "photo"].values[0]
    ph2 = data.loc[data["Player"] == player2, "photo"].values[0]
    
    metrics_closed = metrics + [metrics[0]]
    p1 = list(p1) + [p1[0]]
    p2 = list(p2) + [p2[0]]

    fig = make_subplots(
        rows=1, cols=3,
        column_widths=[0.25, 0.5, 0.25],
        specs=[[{"type": "xy"}, {"type": "polar"}, {"type": "xy"}]],
    )

    fig.add_layout_image(
        dict(
            source=Image.open(f"photos/{ph1}"),
            xref="paper", yref="paper",
            x=0.13, y=0.6,
            sizex=0.72, sizey=0.85,
            xanchor="center", yanchor="middle",
            layer="below"
        )
    )

    fig.add_layout_image(
        dict(
            source=Image.open(f"photos/{ph2}"),
            xref="paper", yref="paper",
            x=0.87, y=0.6,
            sizex=0.72, sizey=0.85,
            xanchor="center", yanchor="middle",
            layer="below"
        )
    )
    
    # --- Plotly radar chart ---
    # fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=p1,
        theta=['Tackles Won/90', 'Blocks/90', 'Interceptions/90', 'Clearances/90', 'DefCon/90', 'CBIT/90', 'Clean Sheets %', 'Errors Lead to Shot/90', 'xGC'],
        fill='toself',
        name=player1,
        line=dict(color='#D62E0F', width=4),
        fillcolor='#DB5B42',
        opacity=0.5
    ), row=1, col=2)
    fig.add_trace(go.Scatterpolar(
        r=p2,
        theta=['Tackles won/90', 'Blocks/90', 'Interceptions/90', 'Clearances/90', 'DefCon/90', 'CBIT/90', 'Clean Sheets %', 'Errors lead to goal/90', 'xGC'],
        fill='toself',
        name=player2,
        line=dict(color='#120FD6', width=4),
        fillcolor='#4F4ED9',
        opacity=0.5
    ), row=1, col=2)
    
    fig.update_layout(
        polar=dict(radialaxis=dict(
            visible=True,
            range=[0, 1],
            color="black",          # ← makes the tick labels black
            tickfont=dict(color="rgba(0,0,0,0)")  # ← ensures tick text is black
        )),
        showlegend=True,
        legend=dict(
             orientation="h",      # horizontal layout
            x=0.5,                # center horizontally
            y=1.15,               # position above the chart
            xanchor="center",     # anchor at center
            yanchor="bottom",     # anchor at bottom of legend box
            bgcolor="rgba(0,0,0,0)"  # transparent background (optional) 
        ),
        #title=dict(text=f"{player1} vs {player2}", x=0.5, xanchor='center', font=dict(size=24)),
        width=500,  # 👈 increase size
        height=500, # 👈 increase size
        margin=dict(l=20, r=20, t=80, b=20)
    )

    return fig

def chart_player_comparison_gk(player1, player2):
    #global data
    #data = get_player_data()
    metrics = ["Save_percent", 'CS_percent', 'Save_percent_Penalty', "Err", 'expected_goals_conceded_per_90']
    scaler = MinMaxScaler()
    df_scaled = data.copy()
    df_scaled[metrics] = scaler.fit_transform(data[metrics])
    p1 = df_scaled[df_scaled["Player"] == player1][metrics].values.flatten()
    p2 = df_scaled[df_scaled["Player"] == player2][metrics].values.flatten()

    ph1 = data.loc[data["Player"] == player1, "photo"].values[0]
    ph2 = data.loc[data["Player"] == player2, "photo"].values[0]
    
    metrics_closed = metrics + [metrics[0]]
    p1 = list(p1) + [p1[0]]
    p2 = list(p2) + [p2[0]]

    fig = make_subplots(
        rows=1, cols=3,
        column_widths=[0.25, 0.5, 0.25],
        specs=[[{"type": "xy"}, {"type": "polar"}, {"type": "xy"}]],
    )

    fig.add_layout_image(
        dict(
            source=Image.open(f"photos/{ph1}"),
            xref="paper", yref="paper",
            x=0.13, y=0.6,
            sizex=0.72, sizey=0.85,
            xanchor="center", yanchor="middle",
            layer="below"
        )
    )

    fig.add_layout_image(
        dict(
            source=Image.open(f"photos/{ph2}"),
            xref="paper", yref="paper",
            x=0.87, y=0.6,
            sizex=0.72, sizey=0.85,
            xanchor="center", yanchor="middle",
            layer="below"
        )
    )
    
    # --- Plotly radar chart ---
    # fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=p1,
        theta=['Saves %/90', 'Clean Sheets %', 'Saved Penalties %', 'Errors Lead to Shot/90', 'xGC'],
        fill='toself',
        name=player1,
        line=dict(color='#D62E0F', width=4),
        fillcolor='#DB5B42',
        opacity=0.5
    ), row=1, col=2)
    fig.add_trace(go.Scatterpolar(
        r=p2,
        theta=['Saves %/90', 'Clean Sheets %', 'Saved Penalties %', 'Errors Lead to Shot/90', 'xGC'],
        fill='toself',
        name=player2,
        line=dict(color='#120FD6', width=4),
        fillcolor='#4F4ED9',
        opacity=0.5
    ), row=1, col=2)
    
    fig.update_layout(
        polar=dict(radialaxis=dict(
            visible=True,
            range=[0, 1],
            color="black",          # ← makes the tick labels black
            tickfont=dict(color="rgba(0,0,0,0)")  # ← ensures tick text is black
        )),
        showlegend=True,
        legend=dict(
             orientation="h",      # horizontal layout
            x=0.5,                # center horizontally
            y=1.15,               # position above the chart
            xanchor="center",     # anchor at center
            yanchor="bottom",     # anchor at bottom of legend box
            bgcolor="rgba(0,0,0,0)"  # transparent background (optional) 
        ),
        #title=dict(text=f"{player1} vs {player2}", x=0.5, xanchor='center', font=dict(size=24)),
        width=500,  # 👈 increase size
        height=500, # 👈 increase size
        margin=dict(l=20, r=20, t=80, b=20)
    )

    return fig
