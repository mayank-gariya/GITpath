"""
Reusable UI components: user cards, interactive Plotly graph drawing, metrics, etc.
"""
import streamlit as st
import networkx as nx
import plotly.graph_objects as go

def render_user_card(user):
    """
    Display a single user profile card with full details.
    Expects a GitHubUser object (or None).
    """
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
    """
    Draw an interactive Plotly network graph tailored to the orange theme.
    """
    G = nx.DiGraph()
    for node in search_graph.nodes:
        G.add_node(node.username)
    for edge in search_graph.edges:
        G.add_edge(edge.source, edge.target)

    # Compute graph layout coordinates
    pos = nx.spring_layout(G, k=0.35, seed=42)

    # Edges trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.2, color='#fed7aa'),
        hoverinfo='none',
        mode='lines'
    )

    # Highlight Path Edges with Orange/Amber Accent
    path_edge_trace = None
    if path_nodes and len(path_nodes) > 1:
        path_edges = list(zip(path_nodes, path_nodes[1:]))
        p_edge_x = []
        p_edge_y = []
        for edge in path_edges:
            if edge[0] in pos and edge[1] in pos:
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                p_edge_x.extend([x0, x1, None])
                p_edge_y.extend([y0, y1, None])
        
        path_edge_trace = go.Scatter(
            x=p_edge_x, y=p_edge_y,
            line=dict(width=3.5, color='#f97316'),
            hoverinfo='none',
            mode='lines'
        )

    # Nodes trace styled for the orange theme
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        if path_nodes and node in path_nodes:
            node_color.append('#ea580c')  # Deep vibrant orange for path nodes
            node_size.append(30)
        else:
            node_color.append('#431407')  # Dark warm brown/charcoal for standard network nodes
            node_size.append(18)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line=dict(width=2, color='#ffedd5')
        ),
        textfont=dict(family="Inter", size=10, color="#7c2d12")
    )

    # Plot layout configuration
    fig_data = [edge_trace, node_trace]
    if path_edge_trace:
        fig_data.insert(1, path_edge_trace)

    fig = go.Figure(
        data=fig_data,
        layout=go.Layout(
            title=dict(text="", font=dict(size=14)),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=20),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=550
        )
    )

    with placeholder.container():
        st.markdown("### 🗺️ Interactive Connection Network Graph")
        col_left, col_center, col_right = st.columns([0.05, 0.9, 0.05])
        with col_center:
            st.plotly_chart(fig, use_container_width=True)

def render_metrics(visited_count, api_calls, current_node, placeholder_dict):
    """
    Update the three metric placeholders.
    """
    placeholder_dict['visited'].metric("Visited Nodes", visited_count)
    placeholder_dict['api'].metric("GitHub API Calls", api_calls)
    placeholder_dict['current'].metric("Inspecting Node", current_node)

def render_stats(result):
    """
    Display search statistics nicely using clean orange-themed stat cards.
    """
    st.divider()
    st.subheader("📊 Search Execution Statistics")
    
    stats_html = f"""
    <div class="stat-card-container">
        <div class="stat-card">
            <div class="stat-label">Visited Users</div>
            <div class="stat-value">{result.visited_count}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Path Distance</div>
            <div class="stat-value">{result.search_depth}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">API Calls</div>
            <div class="stat-value">{result.api_calls}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Speed</div>
            <div class="stat-value">{result.elapsed_time}s</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Network Nodes</div>
            <div class="stat-value">{len(result.graph.nodes)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Network Edges</div>
            <div class="stat-value">{len(result.graph.edges)}</div>
        </div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)