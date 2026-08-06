import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def render_user_card(user):
    if not user:
        st.markdown("### 👤\n**User data unavailable**")
        st.caption("Could not fetch profile.")
        return

    avatar_html = f'<img src="{user.avatar_url}" class="avatar" />' if user.avatar_url else '<div class="avatar-placeholder">👤</div>'
    card_html = f"""
    <div class="user-card">
        {avatar_html}
        <div class="username">
            <a href="https://github.com/{user.login}" target="_blank">{user.name or user.login}</a>
        </div>
        <div class="handle">@{user.login}</div>
        <div class="stats">
            <span>⭐ {user.followers}</span>
            <span>🔁 {user.following}</span>
            <span>📦 {user.public_repos}</span>
        </div>
        {f'<div class="bio">📝 {user.bio[:90]}{"..." if user.bio and len(user.bio) > 90 else ""}</div>' if user.bio else ''}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def draw_graph(search_graph, path_nodes, placeholder):
    """Draw a clean Matplotlib network graph highlighting the path."""
    G = nx.DiGraph()
    for node in search_graph.nodes:
        G.add_node(node.username)
    for edge in search_graph.edges:
        G.add_edge(edge.source, edge.target)

    pos = nx.kamada_kawai_layout(G)  # better spacing

    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_facecolor('none')
    fig.patch.set_facecolor('none')

    # All edges (light)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#4b5563', alpha=0.3, arrows=True, arrowsize=10)

    # Non-path nodes
    non_path = [n for n in G.nodes() if n not in path_nodes]
    nx.draw_networkx_nodes(G, pos, nodelist=non_path, ax=ax,
                           node_size=300, node_color='#2d3748', edgecolors='#4b5563')

    # Path nodes and edges
    if path_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, ax=ax,
                               node_size=500, node_color='#f97316', edgecolors='#fb923c')
        path_edges = list(zip(path_nodes, path_nodes[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax,
                               edge_color='#f97316', width=3, arrows=True, arrowsize=15)

    # Labels
    nx.draw_networkx_labels(G, pos, labels={n:n for n in G.nodes()}, ax=ax,
                            font_size=8, font_weight='bold', font_color='#f3f4f6',
                            bbox=dict(facecolor='#0d1117', edgecolor='none', pad=1))

    ax.axis('off')
    with placeholder.container():
        st.markdown("### 🗺️ Connection Network Graph")
        st.pyplot(fig, clear_figure=True)

def render_metrics(visited_count, api_calls, current_node, placeholder_dict):
    placeholder_dict['visited'].metric("Visited Nodes", visited_count)
    placeholder_dict['api'].metric("GitHub API Calls", api_calls)
    placeholder_dict['current'].metric("Inspecting Node", current_node)

def render_stats(result):
    st.divider()
    st.subheader("📊 Search Execution Statistics")
    stats_html = f"""
    <div class="stat-card-container">
        <div class="stat-card"><div class="stat-label">Visited Users</div><div class="stat-value">{result.visited_count}</div></div>
        <div class="stat-card"><div class="stat-label">Path Distance</div><div class="stat-value">{result.search_depth}</div></div>
        <div class="stat-card"><div class="stat-label">API Calls</div><div class="stat-value">{result.api_calls}</div></div>
        <div class="stat-card"><div class="stat-label">Speed</div><div class="stat-value">{result.elapsed_time}s</div></div>
        <div class="stat-card"><div class="stat-label">Network Nodes</div><div class="stat-value">{len(result.graph.nodes)}</div></div>
        <div class="stat-card"><div class="stat-label">Network Edges</div><div class="stat-value">{len(result.graph.edges)}</div></div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)