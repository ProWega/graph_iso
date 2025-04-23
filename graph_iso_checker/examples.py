# graph_iso_checker/examples.py
import os
from graph_iso_checker.graph import Graph, generate_random_graph


def generate_examples(output_dir='examples'):
    """
    Создаёт папку output_dir и в ней JSON-файлы с примерами графов:
      - Структурированные изоморфные пары: empty, complete, path, cycle (n=5,10)
      - Структурированные не-изоморфные пары: empty vs complete (n=5,10)
      - Случайные графы G(n, p) и их перестановки (n=20,50,100; p=0.1,0.5)
    Возвращает список кортежей (path1, path2).
    """
    os.makedirs(output_dir, exist_ok=True)
    pairs = []


    for n in (5, 10):
        # empty: isomorphic pair
        g_empty = Graph(n)
        p_empty = os.path.join(output_dir, f'empty_{n}.json')
        with open(p_empty, 'w', encoding='utf-8') as f:
            f.write(g_empty.to_json())
        g_empty_perm, _ = g_empty.random_permutation()
        p_empty_perm = os.path.join(output_dir, f'empty_{n}_perm.json')
        with open(p_empty_perm, 'w', encoding='utf-8') as f:
            f.write(g_empty_perm.to_json())
        pairs.append((p_empty, p_empty_perm))


        # complete: isomorphic pair
        g_complete = Graph(n)
        for u in range(n):
            for v in range(u+1, n):
                g_complete.add_edge(u, v)
        p_complete = os.path.join(output_dir, f'complete_{n}.json')
        with open(p_complete, 'w', encoding='utf-8') as f:
            f.write(g_complete.to_json())
        g_complete_perm, _ = g_complete.random_permutation()
        p_complete_perm = os.path.join(output_dir, f'complete_{n}_perm.json')
        with open(p_complete_perm, 'w', encoding='utf-8') as f:
            f.write(g_complete_perm.to_json())
        pairs.append((p_complete, p_complete_perm))


        # non-isomorphic: empty vs complete
        pairs.append((p_empty, p_complete))


        # path: isomorphic pair
        g_path = Graph(n)
        for u in range(n-1):
            g_path.add_edge(u, u+1)
        p_path = os.path.join(output_dir, f'path_{n}.json')
        with open(p_path, 'w', encoding='utf-8') as f:
            f.write(g_path.to_json())
        g_path_perm, _ = g_path.random_permutation()
        p_path_perm = os.path.join(output_dir, f'path_{n}_perm.json')
        with open(p_path_perm, 'w', encoding='utf-8') as f:
            f.write(g_path_perm.to_json())
        pairs.append((p_path, p_path_perm))


        # cycle: isomorphic pair
        g_cycle = Graph(n)
        for u in range(n-1):
            g_cycle.add_edge(u, u+1)
        if n > 2:
            g_cycle.add_edge(n-1, 0)
        p_cycle = os.path.join(output_dir, f'cycle_{n}.json')
        with open(p_cycle, 'w', encoding='utf-8') as f:
            f.write(g_cycle.to_json())
        g_cycle_perm, _ = g_cycle.random_permutation()
        p_cycle_perm = os.path.join(output_dir, f'cycle_{n}_perm.json')
        with open(p_cycle_perm, 'w', encoding='utf-8') as f:
            f.write(g_cycle_perm.to_json())
        pairs.append((p_cycle, p_cycle_perm))


    # random graphs
    for n in (20, 50, 100):
        for p in (0.1, 0.5):
            g_rand = generate_random_graph(n, p)
            fname = os.path.join(output_dir, f'rand_n{n}_p{p:.2f}.json')
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(g_rand.to_json())
            g_rand_perm, _ = g_rand.random_permutation()
            fname_perm = os.path.join(output_dir, f'rand_n{n}_p{p:.2f}_perm.json')
            with open(fname_perm, 'w', encoding='utf-8') as f:
                f.write(g_rand_perm.to_json())
            pairs.append((fname, fname_perm))


    return pairs


if __name__ == "__main__":
    pairs = generate_examples()
    print("Generated examples in 'examples' directory:")
    for f1, f2 in pairs:
        print(f"  python -m graph_iso_checker.main {f1} {f2}")




