# Architecture

This repository implements a BFS-based search approach to explore a social graph (e.g., GitHub follow graph) starting from one or more seed profiles.

High-level components

- src/gitpath/search.py: BFS traversal logic (core algorithm)
- examples/run_example.py: Toy example demonstrating traversal
- assets/: repository images and diagrams (logo, flowchart)
- docs/: design notes and architecture docs

Design notes

- The traversal separately accepts a get_neighbors() callable so it can be integrated with real network calls, cached graph stores, or synthetic graphs for testing.
- The implementation is intentionally small and well-documented to make extensions (ranking, filtering, parallelism) straightforward.
