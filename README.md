# GITpath

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

A tool to discover connection paths between GitHub users — i.e., how one user is connected to another through follower/following relationships. GITpath models users as graph nodes and follower/following relations as undirected edges, and finds short paths between two users efficiently.

Table of contents
- About
- Key features
- Architecture — how components connect
- Why bidirectional BFS (not plain BFS)
- Future improvements
- Example
- Quickstart (install & run)
- Configuration & rate limits
- Tech stack & badges
- Contributing
- License

About
-----
GITpath explores GitHub's social graph to answer questions like "How is user A connected to user B?". The project favors efficiency: instead of using a naive single-source BFS (which can blow up in time and requests), GITpath implements bidirectional breadth-first search to reduce the number of nodes explored and the number of GitHub API calls.

Key features
------------
- Finds connection paths between two GitHub users (via followers / following links).
- Uses bidirectional BFS to dramatically reduce search time and API usage compared to single-source BFS.
- Modular design: separate components for fetching neighbors, search orchestration, caching, and presentation (CLI/API/UI).
- Simple caching/persistence hooks so repeated queries for popular users cost less.

Architecture — how components connect
------------------------------------
1. CLI / API / UI
   - Accepts source & target usernames and optional parameters (token, max depth, cache settings).
2. Coordinator / Runner
   - Validates input, reads configuration, sets up logging and rate-limit handling.
3. Graph Fetcher (GitHub API client)
   - Fetches followers/following for a given username, handles pagination, authentication, errors, and rate-limit backoff.
   - Optionally persists neighbor lists to the Cache layer.
4. Cache / Persistence (optional)
   - Local file cache, SQLite, or Redis store for neighbor lists and previously computed paths.
5. Search Engine (Bidirectional BFS)
   - Maintains two frontiers (from source and target). Always expands the smaller frontier to keep exploration minimal.
   - After each expansion checks for intersection between visited sets; when found, it reconstructs the full path.
6. Output / Result
   - Returns the path (sequence of GitHub usernames), and optionally stores it in cache.

Interaction flow (concise):
- User requests path A -> B → Coordinator initializes Search Engine → Search Engine asks Graph Fetcher for neighbors on-demand → Cache used when available → When frontiers intersect, the full path is reconstructed and returned.

Why bidirectional BFS (not plain BFS)
-------------------------------------
Single-source BFS expands outward from one side and can explore O(b^d) nodes (b = branching factor, d = distance). Bidirectional BFS starts from both source and target and expands until the two searches meet. In typical undirected graphs this reduces explored nodes roughly to O(b^(d/2) + b^(d/2)), which is exponentially smaller for larger d. Practically this means far fewer GitHub API requests and much lower latency.

Future improvements (planned)
----------------------------
- Heuristic-guided searches (e.g., A* with heuristics based on mutual languages, repo overlap, or follower overlap).
- Weighted graph searches where relationships have different costs (mutual follows < one-way follows).
- Precomputed clusters / community detection to route searches across community boundaries faster.
- Parallel or distributed search for very large queries (multi-worker system with a message queue and shared cache).

Example (conceptual)
--------------------
Find a connection between `alice` and `bob`.
- Start: frontierA = {alice}, frontierB = {bob}
- Expand the smaller frontier (fetch neighbors as needed), alternate; on finding intersection user `x` reconstruct path: path(alice→x) + reversed(path(bob→x)).

Quickstart (install & run)
--------------------------
Prerequisites
- Python 3.8+
- A GitHub personal access token (recommended) in environment variable GITHUB_TOKEN for higher rate limits.

Install
1. Clone the repo:
   git clone https://github.com/mayank-gariya/GITpath.git
2. Create and activate a virtual environment, then install dependencies (if requirements.txt exists):
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # or pip install requests aiohttp networkx fastapi uvicorn

Run (example CLI)
- Example usage (pseudo):
  python run_search.py --source mayank-gariya --target torvalds --token $GITHUB_TOKEN

Run as a service (if an API exists)
- Example (FastAPI / uvicorn):
  uvicorn app.main:app --reload
- POST /search {"source": "alice", "target": "bob"}

Configuration & rate limits
---------------------------
- Use a token (GITHUB_TOKEN) to increase rate limits.
- Graph Fetcher honors rate-limit headers (X-RateLimit-Remaining, X-RateLimit-Reset) and backoff when needed.
- Caching neighbor lists reduces repeated API calls for popular users — consider using Redis for production.

Demo video (live proof)
-----------------------
A demo video showing the project working live is included in the `fullapp` folder of this repository. See the folder here:
https://github.com/mayank-gariya/GITpath/tree/main/fullapp

Tech stack & badges
-------------------
- Language: Python (100%)
  ![Python](https://img.shields.io/badge/python-3.8%2B-blue)
- Libraries commonly used:
  - requests / aiohttp — GitHub API client
  - networkx — graph utilities (optional)
  - cachetools / redis — caching
  - FastAPI / Flask — web API
  - pytest — tests

Contributing
------------
Contributions are welcome. Suggested workflow:
- Fork the repo
- Create a feature branch (feature/xyz or fix/issue-#)
- Add tests for new functionality
- Submit a pull request with a clear description

License
-------
This project is released under the MIT License. See LICENSE for details.


---

If you'd like I can also:
- Add CI badges (GitHub Actions) if you want a sample workflow file committed.
- Add a requirements.txt or example Dockerfile.

