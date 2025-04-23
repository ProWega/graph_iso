# graph_iso_checker/main.py
import sys
import argparse
from graph_iso_checker.graph import Graph
from graph_iso_checker.builder import GraphIsoCheckerBuilder


def load_graph(path: str) -> Graph:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    return Graph.from_json(data)


def main():
    parser = argparse.ArgumentParser(
        description="Проверка изоморфизма двух графов в формате JSON"
    )
    parser.add_argument("graph1", help="Путь к первому файлу с графом (.json)")
    parser.add_argument("graph2", help="Путь ко второму файлу с графом (.json)")
    parser.add_argument(
        "--no-genetic",
        action="store_true",
        help="Пропустить этап генетического поиска"
    )
    parser.add_argument(
        "--pop", type=int, default=100,
        help="Размер популяции для GA (по умолчанию 100)"
    )
    parser.add_argument(
        "--gens", type=int, default=2000,
        help="Число поколений для GA (по умолчанию 200)"
    )
    parser.add_argument(
        "--stall", type=int, default=250,
        help="Поколений без улучшений до остановки GA (по умолчанию 20)"
    )
    args = parser.parse_args()


    g1 = load_graph(args.graph1)
    g2 = load_graph(args.graph2)


    # builder = (
    #     GraphIsoCheckerBuilder()
    #     .add_invariant_stage()
    #     .add_refinement_stage()
    # )
    # if not args.no_genetic:
    #     builder = builder.add_genetic_stage(
    #         population_size=args.pop,
    #         generations=args.gens,
    #         stall=args.stall
    #     )
    # builder = builder.add_exact_search_stage()
    # checker = builder.build()

    builder = GraphIsoCheckerBuilder().add_invariant_stage().add_genetic_stage(
             population_size=args.pop,
             generations=args.gens,
             stall=args.stall
         )
    checker = builder.build()



    is_iso, mapping = checker.check_isomorphism(g1, g2)
    if is_iso:
        print("Graphs are isomorphic.")
        print("Mapping (g1 -> g2):")
        for u in sorted(mapping):
            print(f"  {u} -> {mapping[u]}")
        sys.exit(0)
    else:
        print("Graphs are not isomorphic.")
        sys.exit(1)


if __name__ == "__main__":
    main()
