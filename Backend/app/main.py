import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from github.service import GitHubService
from graph.builder import GraphBuilder
from algorithms.bfs import BFS
from algorithms.bidirectional_bfs import BidirectionalBFS

st.set_page_config(
    page_title="GitPath",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ GitPath")
st.caption("Find the shortest GitHub connection path between two users.")


# --------------------------------------------------
# Resources
# --------------------------------------------------

@st.cache_resource
def get_builder():
    service = GitHubService()
    return GraphBuilder(service)

builder = get_builder()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

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

    algorithm = st.radio(
        "Algorithm",
        [
            "BFS",
            "Bidirectional BFS"
        ]
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

graph_placeholder = st.empty()

path_placeholder = st.empty()


# --------------------------------------------------
# Graph Drawing
# --------------------------------------------------

def draw_graph(search_graph):
    G = nx.DiGraph()

    for node in search_graph.nodes:
        G.add_node(node.username)

    for edge in search_graph.edges:
        G.add_edge(edge.source, edge.target)

    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G)

    nx.draw_networkx(
        G,
        pos=pos,
        ax=ax,
        node_size=900,
        font_size=9,
        arrows=True
    )

    ax.axis("off")
    graph_placeholder.pyplot(fig)


# --------------------------------------------------
# Search Execution
# --------------------------------------------------

if search_button:
    if not start_user or not target_user:
        st.error("Please enter both usernames.")
        st.stop()

    builder.api_calls = 0

    # Instantiate the correct algorithm module dynamically
    if algorithm == "BFS":
        engine = BFS()
    else:
        engine = BidirectionalBFS()

    with st.spinner("Searching..."):
        # Both engines now share the identical streaming interface
        for update in engine.get_shortest_path_stream(
            start_user,
            target_user,
            builder,
        ):
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

            draw_graph(update.graph)

            if update.type == "progress":
                status.info(
                    f"Searching frontier near **{update.current_node}**..."
                )
            else:
                # final update payload unpack
                result = update.result

                if result.found:
                    status.success("Path Found ✅")
                    path_placeholder.markdown(
                        "### Shortest Path\n\n"
                        + " → ".join(result.path)
                    )
                else:
                    status.error("No path found.")

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