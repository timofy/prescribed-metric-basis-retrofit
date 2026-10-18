"""Independent definition-level oracle. No pilot modules are imported.

Written before examining any pilot implementation or result contents.
"""
import itertools
from collections import deque


def distances(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        assert 0 <= a < n and 0 <= b < n and a != b
        assert b not in adj[a], 'duplicate edge'
        adj[a].add(b)
        adj[b].add(a)
    d = []
    for s in range(n):
        row = [None] * n
        row[s] = 0
        todo = deque([s])
        while todo:
            a = todo.popleft()
            for b in adj[a]:
                if row[b] is None:
                    row[b] = row[a] + 1
                    todo.append(b)
        assert None not in row, 'disconnected'
        d.append(row)
    return d, adj


def exact(n, edges):
    d, adj = distances(n, edges)
    subsets = [tuple(i for i in range(n) if m & (1 << i)) for m in range(1 << n)]
    # The graph and distances stay fixed when a sensor is erased.
    resolves = [len({tuple(d[v][s] for s in subset) for v in range(n)}) == n
                for subset in subsets]
    ft = [bool(subsets[m]) and all(resolves[m ^ (1 << s)] for s in subsets[m])
          for m in range(1 << n)]
    beta = min(len(subsets[m]) for m in range(1 << n) if resolves[m])
    bases = [m for m in range(1 << n) if resolves[m] and len(subsets[m]) == beta]
    ft_masks = [m for m in range(1 << n) if ft[m]]
    beta2 = min(m.bit_count() for m in ft_masks)
    rho = {b: min(m.bit_count() for m in ft_masks if m & b == b) for b in bases}
    return dict(beta=beta, beta2=beta2, bases=bases, rho=rho, ft_masks=ft_masks,
                resolving_masks=[m for m, ok in enumerate(resolves) if ok],
                subset_count=1 << n, erasure_checks=n * (1 << (n-1)))


def canonical(n, edges):
    """Exact isomorphism key: unique cycle with rooted tree attachments."""
    _, adj = distances(n, edges)
    degree = list(map(len, adj))
    leaves = deque(v for v in range(n) if degree[v] == 1)
    while leaves:
        v = leaves.popleft()
        degree[v] = 0
        for w in adj[v]:
            if degree[w] > 0:
                degree[w] -= 1
                if degree[w] == 1:
                    leaves.append(w)
    cycle = {v for v in range(n) if degree[v] > 0}
    assert len(cycle) >= 3 and all(degree[v] == 2 for v in cycle)
    def tree(v, parent):
        return '(' + ''.join(sorted(tree(w, v) for w in adj[v] if w != parent and w not in cycle)) + ')'
    start = min(cycle)
    order, prev, v = [], None, start
    while not order or v != start:
        order.append(tree(v, None))
        nxt = next(w for w in sorted(adj[v] & cycle) if w != prev)
        prev, v = v, nxt
    variants = []
    for seq in (order, list(reversed(order))):
        variants.extend(tuple(seq[i:] + seq[:i]) for i in range(len(seq)))
    return min(variants)


def independent_trees(limit):
    """Leaf extension with exact unrooted AHU-style keys; no library generator."""
    levels = {2: [[(0, 1)]]}
    for n in range(3, limit + 1):
        unique = {}
        for edges in levels[n-1]:
            _, adj = distances(n-1, edges)
            for v in range(n-1):
                if len(adj[v]) >= 3:
                    continue
                candidate = edges + [(v, n-1)]
                _, ca = distances(n, candidate)
                def rooted(v, p):
                    return '(' + ''.join(sorted(rooted(w, v) for w in ca[v] if w != p)) + ')'
                key = min(rooted(v, -1) for v in range(n))
                unique.setdefault(key, candidate)
        levels[n] = list(unique.values())
    return levels


def independent_graphs(n, trees):
    """Every unicyclic graph is a tree plus a missing edge.

    Enumerate unlabeled trees using independent leaf extension, add each
    allowable missing edge, and deduplicate by exact cycle/tree isomorphism.
    Removing any cycle edge proves this route covers the required class.
    """
    out = {}
    for tree_edges in trees:
        _, adj = distances(n, tree_edges)
        for a, b in itertools.combinations(range(n), 2):
            if b in adj[a] or len(adj[a]) >= 3 or len(adj[b]) >= 3:
                continue
            edges = tree_edges + [(a, b)]
            out.setdefault(canonical(n, edges), edges)
    return out
