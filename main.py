import argparse


def main():
    parser = argparse.ArgumentParser(description="Run tests or check results.")
    group = parser.add_argument_group()
    group.add_argument("-t", "--test", action="store_true", help="Run test on GPT-5")
    group.add_argument("-c", "--check", action="store_true", help="Print total correct and incorrect")
    group.add_argument("-a", "--all", action="store_true", help="Print all of the organized data")

    args = parser.parse_args()

    if args.test:
        from llm_testing import run_test
        run_test()
    if args.all:
        from process_and_measure_results import print_all
        print_all()
    if args.check:
        from process_and_measure_results import print_totals
        print_totals()
    

if __name__ == "__main__":
    raise SystemExit(main())
