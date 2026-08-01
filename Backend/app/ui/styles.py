import streamlit as st

def apply_custom_css():
    """Inject the orange/black theme CSS directly."""
    css = """
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Base Styles & Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Center Header & Description Layout */
    .centered-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .centered-header h1 {
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #ffffff;
        margin-bottom: 0.25rem;
    }
    .centered-header p {
        color: #9ca3af;
        font-size: 1.05rem;
    }

    /* Sidebar Customization (Dark Orange Theme) */
    [data-testid="stSidebar"] {
        background-color: #0f1117;
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
        box-shadow: 0 6px 16px rgba(249, 115, 22, 0.5);
    }

    /* User Card Component (High-Contrast Dark Mode & Orange Accents) */
    .user-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 1.25rem 1rem 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .user-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #f97316, #fb923c);
    }

    .user-card:hover {
        transform: translateY(-4px);
        border-color: #f97316;
        box-shadow: 0 12px 32px rgba(249, 115, 22, 0.2);
    }

    .user-card .avatar {
        border-radius: 50%;
        border: 3px solid #30363d;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        width: 90px;
        height: 90px;
        object-fit: cover;
        margin: 0 auto 0.75rem;
        display: block;
    }

    .user-card .username {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }

    .user-card .username a {
        color: #f3f4f6;
        text-decoration: none;
        transition: color 0.2s;
    }

    .user-card .username a:hover {
        color: #f97316;
    }

    .user-card .handle {
        color: #9ca3af;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.75rem;
    }

    .user-card .stats {
        display: flex;
        justify-content: space-around;
        font-size: 0.78rem;
        font-weight: 600;
        background: #0d1117;
        border: 1px solid #30363d;
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: #fb923c;
        flex-wrap: wrap;
        gap: 4px;
    }

    .user-card .stats span {
        white-space: nowrap;
    }

    .user-card .bio {
        font-size: 0.82rem;
        color: #d1d5db;
        border-top: 1px solid #30363d;
        padding-top: 0.6rem;
        margin-top: 0.6rem;
        text-align: left;
        line-height: 1.4;
    }

    /* Path Display Component */
    .path-route {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid #f97316;
        padding: 0.85rem 1.25rem;
        border-radius: 8px;
        font-family: 'Inter', monospace;
        font-size: 1.05rem;
        font-weight: 600;
        color: #f3f4f6;
        display: block;
        margin-top: 0.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        word-break: break-all;
    }

    /* Stats Grid Layout */
    .stat-card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        border-color: #f97316;
    }

    .stat-card .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }

    .stat-card .stat-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f97316;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)