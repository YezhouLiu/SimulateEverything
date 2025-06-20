import streamlit as st
import numpy as np
from models.prisoners_dilemma import PrisonersDilemma
from models.stag_hunt import StagHunt
from models.coordination_game import CoordinationGame
from models.hawk_dove_game import HawkDoveGame
from models.public_goods_game import PublicGoodsGame
from models.trust_game import TrustGame
from models.battle_of_sexes import BattleOfSexes
from models.dictator_game import DictatorGame
from visualize import plot_payoff_matrix, get_game_labels

st.set_page_config(page_title="Game Theory Simulator", layout="centered")
st.title("🎲 Game Theory Simulator")

MODEL_MAP = {
    PrisonersDilemma.name: PrisonersDilemma,
    StagHunt.name: StagHunt,
    CoordinationGame.name: CoordinationGame,
    HawkDoveGame.name: HawkDoveGame,
    PublicGoodsGame.name: PublicGoodsGame,
    TrustGame.name: TrustGame,
    BattleOfSexes.name: BattleOfSexes,
    DictatorGame.name: DictatorGame
}

model_name = st.sidebar.selectbox("Select Game Model", list(MODEL_MAP.keys()))
ModelClass = MODEL_MAP[model_name]
st.sidebar.markdown(ModelClass.description)

if model_name == "Prisoner's Dilemma":
    R = st.sidebar.slider("Reward for Cooperation (R)", 0, 10, 3)
    T = st.sidebar.slider("Temptation to Betray (T)", 0, 10, 5)
    S = st.sidebar.slider("Sucker's Payoff (S)", 0, 10, 0)
    P = st.sidebar.slider("Punishment for Mutual Betrayal (P)", 0, 10, 1)
    model = ModelClass(R, T, S, P)
    st.write("#### Player Choices")
    action1 = st.radio("Player 1", ["Cooperate", "Betray"], horizontal=True)
    action2 = st.radio("Player 2", ["Cooperate", "Betray"], horizontal=True)
    if st.button("Run Game"):
        res = model.play(0 if action1=="Cooperate" else 1, 0 if action2=="Cooperate" else 1)
        st.success(f"Result: Player 1 Score {res[0]}, Player 2 Score {res[1]}")
        
elif model_name == "Stag Hunt":
    stag = st.sidebar.slider("Stag Score", 0, 10, 4)
    hare = st.sidebar.slider("Hare Score", 0, 10, 2)
    fail = st.sidebar.slider("Fail to Hunt Stag Score", 0, 10, 0)
    model = ModelClass(stag, hare, fail)
    st.write("#### Player Choices")
    action1 = st.radio("Player 1", ["Hunt Stag", "Hunt Hare"], horizontal=True)
    action2 = st.radio("Player 2", ["Hunt Stag", "Hunt Hare"], horizontal=True)
    if st.button("Run Game"):
        res = model.play(0 if action1=="Hunt Stag" else 1, 0 if action2=="Hunt Stag" else 1)
        st.success(f"Result: Player 1 Score {res[0]}, Player 2 Score {res[1]}")
        
elif model_name == "Coordination Game":
    coord_a = st.sidebar.slider("Coordination A Payoff", 0, 10, 3)
    coord_b = st.sidebar.slider("Coordination B Payoff", 0, 10, 3)
    mismatch = st.sidebar.slider("Mismatch Payoff", 0, 10, 0)
    model = ModelClass(coord_a, coord_b, mismatch)
    st.write("#### Player Choices")
    action1 = st.radio("Player 1", ["Option A", "Option B"], horizontal=True)
    action2 = st.radio("Player 2", ["Option A", "Option B"], horizontal=True)
    if st.button("Run Game"):
        res = model.play(0 if action1=="Option A" else 1, 0 if action2=="Option A" else 1)
        st.success(f"Result: Player 1 Score {res[0]}, Player 2 Score {res[1]}")
        
elif model_name == "Hawk-Dove Game":
    value = st.sidebar.slider("Resource Value", 0, 10, 4)
    cost = st.sidebar.slider("Cost of Conflict", 0, 10, 6)
    model = ModelClass(value, cost)
    st.write("#### Player Choices")
    action1 = st.radio("Player 1", ["Hawk (Aggressive)", "Dove (Passive)"], horizontal=True)
    action2 = st.radio("Player 2", ["Hawk (Aggressive)", "Dove (Passive)"], horizontal=True)
    if st.button("Run Game"):
        res = model.play(0 if action1=="Hawk (Aggressive)" else 1, 0 if action2=="Hawk (Aggressive)" else 1)
        st.success(f"Result: Player 1 Score {res[0]}, Player 2 Score {res[1]}")
        
elif model_name == "Public Goods Game":
    endowment = st.sidebar.slider("Player Endowment", 1, 20, 10)
    multiplier = st.sidebar.slider("Multiplier", 1.0, 3.0, 1.6, 0.1)
    st.write("#### Player Contributions")
    contrib1 = st.slider("Player 1 Contribution", 0, endowment, endowment // 2)
    contrib2 = st.slider("Player 2 Contribution", 0, endowment, endowment // 2)
    model = ModelClass(endowment, multiplier)
    if st.button("Run Game"):
        res = model.play_two_player(contrib1, contrib2)
        st.success(f"Result: Player 1 Payoff {res[0]:.2f}, Player 2 Payoff {res[1]:.2f}")
        
elif model_name == "Trust Game":
    initial_amount = st.sidebar.slider("Initial Amount", 1, 20, 10)
    multiplier = st.sidebar.slider("Multiplier", 1.0, 5.0, 3.0, 0.5)
    model = ModelClass(initial_amount, multiplier)
    st.write("#### Player Choices")
    send_choice = st.radio("Player 1 (Sender): Trust Level", ["Low Trust", "Medium Trust", "High Trust"], horizontal=True)
    return_choice = st.radio("Player 2 (Receiver): Return Level", ["Low Return", "Medium Return", "High Return"], horizontal=True)
    send_mapping = {"Low Trust": 0, "Medium Trust": 1, "High Trust": 2}
    return_mapping = {"Low Return": 0, "Medium Return": 1, "High Return": 2}
    if st.button("Run Game"):
        res = model.play_simple(send_mapping[send_choice], return_mapping[return_choice])
        st.success(f"Result: Sender Payoff {res[0]:.2f}, Receiver Payoff {res[1]:.2f}")
        
elif model_name == "Battle of Sexes":
    opera_man = st.sidebar.slider("Man's Opera Payoff", 0, 10, 2)
    opera_woman = st.sidebar.slider("Woman's Opera Payoff", 0, 10, 1)
    football_man = st.sidebar.slider("Man's Football Payoff", 0, 10, 1)
    football_woman = st.sidebar.slider("Woman's Football Payoff", 0, 10, 2)
    model = ModelClass(opera_man, opera_woman, football_man, football_woman)
    st.write("#### Player Choices")
    action1 = st.radio("Man", ["Opera", "Football"], horizontal=True)
    action2 = st.radio("Woman", ["Opera", "Football"], horizontal=True)
    if st.button("Run Game"):
        res = model.play(0 if action1=="Opera" else 1, 0 if action2=="Opera" else 1)
        st.success(f"Result: Man Score {res[0]}, Woman Score {res[1]}")
        
elif model_name == "Dictator Game":
    total_amount = st.sidebar.slider("Total Amount", 1, 20, 10)
    model = ModelClass(total_amount)
    st.write("#### Dictator's Choice")
    amount_given = st.slider("Amount to Give", 0, total_amount, total_amount // 2)
    if st.button("Run Game"):
        res = model.play(amount_given)
        st.success(f"Result: Dictator Keeps {res[0]}, Recipient Gets {res[1]}")

st.markdown("---")
st.markdown("**Model Introduction:**")
st.info(ModelClass.description)

# Add visualization for games that have a payoff matrix
if model_name in ["Prisoner's Dilemma", "Stag Hunt", "Coordination Game", "Hawk-Dove Game", "Battle of Sexes"]:
    st.markdown("---")
    st.markdown("**Payoff Matrix Visualization:**")
    st.markdown("Each cell shows: (Player 1 payoff, Player 2 payoff)")
    
    # Get the figure from the visualization module
    try:
        fig = plot_payoff_matrix(model, f"{model_name} Payoff Matrix")
        if fig:
            st.pyplot(fig)
    except Exception as e:
        st.warning(f"Could not display payoff matrix visualization: {str(e)}")
