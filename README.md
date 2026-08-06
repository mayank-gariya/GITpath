🌐 GITpath

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An intelligent graph-based search application designed to discover connections and shortest paths between any two GitHub users through their network of followers, followings, and shared connections.

---

## 📌 Problem Statement

With millions of active developers on GitHub, mapping social connections and finding how two engineers are linked can be computationally expensive. Standard search algorithms like traditional Breadth-First Search (BFS) suffer from exponential node expansion when navigating deeply nested social graphs, leading to high latency and API rate-limiting issues.

**GITpath** addresses this challenge by combining graph theory with optimized pathfinding algorithms to map network connections between users efficiently and dynamically.

---

## 🚀 Demo & Walkthrough

Below is a demonstration of the application in action:

https://github.com/user-attachments/assets/GitPath%20-%20Profile%201%20-%20Microsoft_%20Edge%202026-08-01%2021-30-20.mp4

> *Note: If the inline video preview does not load, you can view the raw video file directly in the repository.*

---

## ⚡ Algorithm & Core Approach

To achieve fast pathfinding across large GitHub networks, GITpath utilizes **Bidirectional Breadth-First Search (BFS)**.

### Why Bidirectional BFS?
* **Standard BFS Complexity:** $O(b^d)$, where $b$ is the branching factor (average connections per user) and $d$ is the connection distance.
* **Bidirectional BFS Complexity:** $O(b^{d/2})$, running two simultaneous searches—one forward from the **Source User** and one backward from the **Target User**—until both search frontiers intersect.
* **Performance Gain:** Significantly reduces the total number of API queries and graph nodes traversed to find the shortest path.

[Source User] ---> (Frontier A)(Intersection Point) ---> Shortest Path Found![Target User] ---> (Frontier B) /
---

## ⚙️ Architecture & Data Flow

                  +-------------------------+
                  |      Streamlit UI       |
                  |   (ui/components.py)    |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |       Core Logic        |
                  |   (core/SearchConfig)   |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  | Bidirectional BFS Engine|
                  | (algorithms/bd_bfs.py)  |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |   GitHub API Client     |
                  |  (github/client.py)     |
                  +-------------------------+

---

## 📂 Folder Structure

```text
app/
├── algorithms/
│   ├── bidirectional_bfs.py  # Bidirectional BFS pathfinding logic
│   ├── metric.py             # Path evaluation and performance metrics
│   └── schemas.py            # Data schemas for search algorithms
├── core/
│   ├── SearchConfig.py       # Configuration parameters for search execution
│   ├── constants.py          # Application-wide constants
│   ├── logger.py             # Logging utilities
│   └── settings.py           # Environment and app configuration settings
├── github/
│   ├── client.py             # GitHub REST API client handler
│   ├── schemas.py            # API request/response data models
│   └── service.py            # High-level GitHub network operations
├── graph/
│   ├── builder.py            # Graph construction routines
│   └── node.py               # Node and Edge representation models
├── ui/
│   ├── components.py         # Reusable UI component definitions
│   ├── styles.py             # Custom styling and CSS
│   └── utils.py              # UI helper functions
├── .env.example              # Example environment variable file
├── main.py                   # Streamlit app entrypoint
└── requirements.txt          # Python dependencies
```

##🛠️ Getting StartedPrerequisitesPython 3.10 or higherGitHub Personal Access Token (PAT) to prevent API rate limitingInstallationClone the repository:Bashgit clone [https://github.com/mayank-gariya/GITpath.git](https://github.com/mayank-gariya/GITpath.git)

```
cd GITpath/fullapp/app
Set up a virtual environment:Bashpython -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
```
Install dependencies:Bashpip install -r requirements.txt
```

Configure Environment Variables:
```
Copy .env.example to .env and add your GitHub token:Bashcp .env.example .env
Edit .env:Code snippetGITHUB_TOKEN=your_github_personal_access_token_here
Run the Application:Bashstreamlit run main.py
```

## 🔮 Future Improvements🔀 Multi-Algorithm Support: 
Incorporate additional graph pathfinding algorithms such as $A^*$, Dijkstra's algorithm (weighted by interaction/collaboration frequency), 
and Depth-First Search (DFS) for comparison.

## 📊 Algorithm Benchmarking:

Add a side-by-side performance comparison dashboard to measure execution time, API calls, and memory consumption across different algorithms.

🕸️ Interactive Graph Visualizations: 

Integrate interactive 3D/2D visualizers (e.g., PyVis, D3.js, or NetworkX) to render user network trees dynamically.

⚡ Caching Layer: Implement Redis or disk-backed caching for GitHub API responses to optimize response times and bypass rate limits for popular profiles.



🤝 Shared Repository Connections: Extend connection logic beyond followers/followings to include co-contributors, starred repositories, and shared organizations.
