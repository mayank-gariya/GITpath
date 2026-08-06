import streamlit as st
from fullapp.app.graph.builder import GraphBuilder

@st.cache_data(ttl=3600)
def fetch_user(username: str, _builder: GraphBuilder):
    """
    Fetch full GitHub user data with caching.
    The underscore before 'builder' tells Streamlit NOT to hash this argument.
    """
    return _builder.github_service.get_user(username)
