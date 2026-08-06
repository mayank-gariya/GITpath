# GITpath

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  [![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

A small, practical tool to find connection paths between GitHub users using breadth-first search techniques (optimized with bidirectional BFS).

Demo
----

<video controls width="720">
  <source src="fullapp/GitPath - Profile 1 - Microsoft_ Edge 2026-08-01 21-30-20.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

If the embedded player does not appear on GitHub, open the demo directly:

https://github.com/mayank-gariya/GITpath/blob/main/fullapp/GitPath%20-%20Profile%201%20-%20Microsoft_%20Edge%202026-08-01%2021-30-20.mp4

What this project does (short)
-----------------------------

- Models GitHub users as nodes and follower/following relationships as edges.
- Uses bidirectional BFS (searching from source and target) to find a short connection path quickly while using fewer API calls.
- Designed to be modular: fetcher (GitHub API), cache, search engine, and output layer (CLI/API/UI).

Quick start
-----------

1. Clone:

   git clone https://github.com/mayank-gariya/GITpath.git

2. (Optional) Create & activate virtualenv:

   python -m venv .venv
   source .venv/bin/activate

3. Install dependencies if present:

   pip install -r requirements.txt

4. Example run (replace script name if different):

   python run_search.py --source alice --target bob --token $GITHUB_TOKEN

Notes
-----

- A GitHub personal access token (GITHUB_TOKEN) is recommended to avoid strict rate limits.
- Caching neighbor lists (local files, SQLite or Redis) reduces repeated API calls for popular users.

Why bidirectional BFS?
-----------------------

Bidirectional BFS expands from both source and target and meets in the middle — this reduces the number of explored nodes from O(b^d) to roughly O(b^(d/2)), so searches are much faster and cheaper (fewer API calls).

Contributing
------------

Contributions welcome: fork, branch, add tests, and open a pull request with a clear description.

License
-------

MIT
