import argparse
import os
import json
import netrc
from comparison_functions import fetch_binary_packages, compare_package_lists

def main():
    parser = argparse.ArgumentParser(description="Compare binary packages between two branches")
    parser.add_argument("branch1", help="First branch name")
    parser.add_argument("branch2", help="Second branch name")
    args = parser.parse_args()

    try:
        packages1 = fetch_binary_packages(args.branch1)
        packages2 = fetch_binary_packages(args.branch2)

        comparison_result = compare_package_lists(packages1, packages2)

         # Сохранение результатов в отдельные файлы в папке results
        os.makedirs("results", exist_ok=True)

        with open(os.path.join("results", "branch1_only.json"), "w") as f:
            json.dump(comparison_result["in_first_only"], f, indent=4)
        print(f"branch1_only saved to {os.path.join('results', 'branch1_only.json')}")

        with open(os.path.join("results", "branch2_only.json"), "w") as f:
            json.dump(comparison_result["in_second_only"], f, indent=4)
        print(f"branch2_only saved to {os.path.join('results', 'branch2_only.json')}")

        with open(os.path.join("results", "higher_version_in_branch1.json"), "w") as f:
            json.dump(comparison_result["greater_in_first"], f, indent=4)
        print(f"higher_version_in_branch1 saved to {os.path.join('results', 'higher_version_in_branch1.json')}")

        # Сохранение исходных JSON-файлов в папку results
        with open(os.path.join("results", f"{args.branch1}.json"), "w") as f:
            json.dump(packages1, f, indent=4)
        print(f"branch1 JSON saved to {os.path.join('results', f'{args.branch1}.json')}")

        with open(os.path.join("results", f"{args.branch2}.json"), "w") as f:
            json.dump(packages2, f, indent=4)
        print(f"branch2 JSON saved to {os.path.join('results', f'{args.branch2}.json')}")

        # Вывод количества строк
        print(f"branch1_only: {len(comparison_result['in_first_only'])}")
        print(f"branch2_only: {len(comparison_result['in_second_only'])}")
        print(f"higher_version_in_branch1: {len(comparison_result['greater_in_first'])}")
        print(f"Results saved to results")  # Вывод сообщения о сохранении

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
