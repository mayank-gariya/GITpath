import sys
from pathlib import Path
import streamlit as st

# --------------------------------------------------
# Path setup – add the parent directory so "Backend" is a package
# --------------------------------------------------
project_root = Path(__file__).resolve().parent          # Backend/
parent_dir = project_root.parent                        # directory containing Backend/
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Now import from Backend.app...
from Backend.app.github.service import GitHubService
from Backend.app.graph.builder import GraphBuilder
from Backend.app.algorithms.bidirectional_bfs import BidirectionalBFS

from Backend.app.ui.styles import apply_custom_css
from Backend.app.ui.components import (
    render_user_card,
    draw_graph,
    render_metrics,
    render_stats
)
from Backend.app.ui.utils import fetch_user

# --------------------------------------------------
# Page config & CSS
# --------------------------------------------------
st.set_page_config(page_title="GitPath", page_icon="🕸️", layout="wide")
apply_custom_css()

# --------------------------------------------------
# Custom Header (enhanced)
# --------------------------------------------------
st.markdown(
    """
    <div class="centered-header" style="border-bottom: 3px solid #f97316; padding-bottom: 0.5rem; box-shadow: 0 4px 20px rgba(249,115,22,0.15);">
        <h1>🕸️ GitPath</h1>
        <p style="color: #d1d5db;">Find the shortest GitHub connection path between two users instantly.</p>
    </div>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def get_builder():
    service = GitHubService()
    return GraphBuilder(service)

builder = get_builder()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("Search Configuration")
    start_user = st.text_input("Start User", placeholder="octocat")
    target_user = st.text_input("Target User", placeholder="torvalds")
    st.markdown("---")
    st.caption("**Algorithm Selected:** Bidirectional BFS")
    search_button = st.button("Search Path", use_container_width=True, type="primary")

# --------------------------------------------------
# Placeholders
# --------------------------------------------------
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_placeholders = {
    'visited': metric_col1.empty(),
    'api': metric_col2.empty(),
    'current': metric_col3.empty()
}
status_placeholder = st.empty()          
path_placeholder = st.empty()
profile_placeholder = st.empty()
graph_placeholder = st.empty()
stats_placeholder = st.empty()

# Helper: show custom status box
def show_status(message, type_="info"):
    icons = {"info": "📡", "success": "✅", "error": "❌"}
    status_placeholder.markdown(
        f'<div class="custom-status {type_}">{icons.get(type_, "ℹ️")} {message}</div>',
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Search execution
# --------------------------------------------------
if search_button:
    if not start_user or not target_user:
        st.error("Please fill out both fields.")
        st.stop()

    builder.api_calls = 0
    engine = BidirectionalBFS()

    for ph in [graph_placeholder, path_placeholder, profile_placeholder, stats_placeholder, status_placeholder]:
        ph.empty()

    with st.spinner("Mapping paths across GitHub networks..."):
        for update in engine.get_shortest_path_stream(start_user, target_user, builder):
            render_metrics(
                visited_count=update.visited_count,
                api_calls=builder.api_calls,
                current_node=update.current_node,
                placeholder_dict=metric_placeholders
            )

            if update.type == "progress":
                show_status(f"Exploring adjacent nodes around user: **{update.current_node}**...", "info")
            else:
                result = update.result
                if result.found:
                    # --- Success Banner ---
                    status_placeholder.markdown(
                        """
                        <div class="success-banner">
                            <span class="big-icon">🎉</span>
                            <div class="title">Shortest Connection Discovered!</div>
                            <div class="sub">Path found between <strong>""" + start_user + """</strong> and <strong>""" + target_user + """</strong></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # --- Path as steps ---
                    steps_html = '<div class="path-steps">'
                    for idx, username in enumerate(result.path):
                        steps_html += f'<span class="path-step"><span class="step-num">{idx+1}.</span> {username}</span>'
                        if idx < len(result.path) - 1:
                            steps_html += '<span class="path-arrow">➔</span>'
                    steps_html += '</div>'
                    path_placeholder.markdown(
                        f"### 📍 Connection Route\n{steps_html}",
                        unsafe_allow_html=True
                    )

                    # --- User cards ---
                    with profile_placeholder.container():
                        st.markdown("### 👥 Path Profile Connections")
                        cols = st.columns(min(4, len(result.path)))
                        for idx, username in enumerate(result.path):
                            with cols[idx % len(cols)]:
                                user = fetch_user(username, builder)
                                render_user_card(user)

                    draw_graph(update.graph, result.path, graph_placeholder)
                else:
                    show_status(f"No connection found between **{start_user}** and **{target_user}**.", "error")
                    draw_graph(update.graph, [], graph_placeholder)

                with stats_placeholder.container():
                    render_stats(result)