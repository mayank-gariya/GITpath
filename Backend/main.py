import sys
from pathlib import Path
import streamlit as st 
import networkx as nx                                                           
import matplotlib.pyplot as plt   

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent 

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

backend_app_dir = project_root / "Backend" / "app"
if str(backend_app_dir) not in sys.path:
    sys.path.insert(0, str(backend_app_dir))

from Backend.app.github.service import GitHubService
from Backend.app.graph.builder import GraphBuilder
from Backend.app.algorithms.bidirectional_bfs import BidirectionalBFS

st.set_page_config(
    page_title="GitPath",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ GitPath")
st.caption("Find the shortest GitHub connection path between two users.")

@st.cache_resource
def get_builder():
    service = GitHubService()
    return GraphBuilder(service)

builder = get_builder()


with st.sidebar:
    st.header("Search")
    start_user = st.text_input(
        "Start User",
        placeholder="octocat"
    )

    target_user = st.text_input(
        "Target User",
        placeholder="torvalds"
    )

    algorithm = st.subheader(
        'algorithm : Birdectional BFS'
    )

    search_button = st.button(
        "Search",
        use_container_width=True
    )

# --------------------------------------------------
# Metrics
# --------------------------------------------------

metric_col1, metric_col2, metric_col3 = st.columns(3)

visited_metric = metric_col1.empty()
api_metric = metric_col2.empty()
current_metric = metric_col3.empty()

status = st.empty()

# Placeholders for graph and path info
graph_placeholder = st.empty()
path_placeholder = st.empty()
profile_placeholder = st.empty()


# --------------------------------------------------
# Graph Drawing (final version with path highlight)
# --------------------------------------------------

def draw_graph_with_path(search_graph, path_nodes):
    """Draw the full search graph and highlight the shortest path."""
    G = nx.DiGraph()

    # Add all nodes and edges
    for node in search_graph.nodes:
        G.add_node(node.username)
    for edge in search_graph.edges:
        G.add_edge(edge.source, edge.target)

    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # deterministic layout

    # Draw all nodes and edges
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=600, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", arrows=True, arrowsize=15)

    # Highlight path nodes
    path_edges = list(zip(path_nodes, path_nodes[1:]))
    if path_edges:
        nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, ax=ax,
                               node_size=800, node_color="red")
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax,
                               edge_color="red", width=3, arrows=True, arrowsize=20)

    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

    ax.axis("off")
    graph_placeholder.pyplot(fig)

def get_user_from_graph(graph, username):
    """Return the node object with the given username from the search graph."""
    for node in graph.nodes:
        if node.username == username:
            return node
    return None

# --------------------------------------------------
# Search Execution
# --------------------------------------------------

if search_button:
    if not start_user or not target_user:
        st.error("Please enter both usernames.")
        st.stop()

    builder.api_calls = 0

    engine = BidirectionalBFS()

    # Clear previous results
    graph_placeholder.empty()
    path_placeholder.empty()
    profile_placeholder.empty()

    with st.spinner("Searching..."):
        # Both engines now share the identical streaming interface
        for update in engine.get_shortest_path_stream(
            start_user,
            target_user,
            builder,
        ):
            # Always update metrics
            visited_metric.metric(
                "Visited",
                update.visited_count
            )

            api_metric.metric(
                "API Calls",
                builder.api_calls
            )

            current_metric.metric(
                "Current List Node",
                update.current_node
            )

            if update.type == "progress":
                status.info(
                    f"Searching frontier near **{update.current_node}**..."
                )
            else:
                # Final update: draw graph and show user profiles
                result = update.result

                if result.found:
                    status.success("Path Found ✅")
                    path_placeholder.markdown(
                        "### Shortest Path\n\n"
                        + " → ".join(result.path)
                    )
                    
                    with profile_placeholder.container():
                        st.markdown("### 👥 User Profiles on the Path")
                        
                        # Set up a clean grid layout (max 4 cards per row)
                        max_cols = 4
                        path_len = len(result.path)
                        
                        for idx, username in enumerate(result.path):
                            # Create a new row of columns when needed
                            if idx % max_cols == 0:
                                cols = st.columns(min(max_cols, path_len - idx))
                            
                            col = cols[idx % max_cols]
                            user_node = get_user_from_graph(update.graph, username)
                            
                            with col:
                                # Wrap each profile in a clean bordered card
                                with st.container(border=True):
                                    if user_node:
                                        # Avatar image layout
                                        if getattr(user_node, 'avatar_url', None):
                                            st.image(user_node.avatar_url, width=80)
                                        else:
                                            st.markdown("### 👤")
                                            
                                        # Name & Handle (safely using username)
                                        display_name = getattr(user_node, 'name', None) or user_node.username
                                        st.markdown(f"**{display_name}**")
                                        st.caption(f"@{user_node.username}")
                                        
                                        # Metrics Grid
                                        m_col1, m_col2, m_col3 = st.columns(3)
                                        m_col1.metric("Repos", getattr(user_node, 'public_repos', '?'))
                                        m_col2.metric("Followers", getattr(user_node, 'followers', '?'))
                                        m_col3.metric("Following", getattr(user_node, 'following', '?'))
                                        
                                        # Bio Section
                                        bio = getattr(user_node, 'bio', None)
                                        if bio:
                                            st.caption(f"📝 {bio[:75]}..." if len(bio) > 75 else f"📝 {bio}")
                                    else:
                                        # Fallback placeholder if profile payload isn't fully loaded yet
                                        st.markdown(f"### 👤\n**{username}**")
                                        st.caption("Profile data loading...")
                                        
                    # Draw the final graph with path highlighted
                    draw_graph_with_path(update.graph, result.path)

                else:
                    status.error("No path found.")
                    # Optionally draw the full graph anyway
                    draw_graph_with_path(update.graph, [])

                st.divider()
                st.subheader("Statistics")
                st.json(
                    {
                        "Visited Users": result.visited_count,
                        "Depth": result.search_depth,
                        "API Calls": result.api_calls,
                        "Execution Time": f"{result.elapsed_time}s",
                        "Edges": len(result.graph.edges),
                        "Nodes": len(result.graph.nodes),
                    }
                )