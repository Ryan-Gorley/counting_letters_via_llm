import argparse

from common import SAMPLES_DEFAULT, CONCURRENT_DEFAULT

def main():
    parser = argparse.ArgumentParser(description="Run tests or check results.")
    group = parser.add_argument_group()
    group.add_argument(
        "-T", "--test",
        action="store_true",
        help="Run test on GPT-5"
    )
    group.add_argument(
        "-C", "--check",
        action="store_true",
        help="Print total correct and incorrect"
    )
    group.add_argument(
        "-A", "--all",
        action="store_true",
        help="Print all of the organized data"
    )
    group.add_argument(
        "-c",
        "--concurrent",
        type=int,
        choices=range(1, 33),
        default=CONCURRENT_DEFAULT,
        metavar="[1-32]",
        help=f"Number of concurrent requests to make during testing \
            (1-32, default {CONCURRENT_DEFAULT})",
    )
    group.add_argument(
        "-s",
        "--samples",
        type=int,
        choices=range(1, 1001),
        default=SAMPLES_DEFAULT,
        metavar="[1-1000]",
        help=f"Number of samples to use during testing \
            (1-1000, default {SAMPLES_DEFAULT})",
    )
    
    args = parser.parse_args()

    if args.test:
        from llm_testing import run_test
        concurrent = int(args.concurrent or CONCURRENT_DEFAULT)
        sample_count = int(args.samples or SAMPLES_DEFAULT)
        run_test(sample_count, concurrent)
    if args.all:
        from process_and_measure_results import print_all
        print_all()
    if args.check:
        from process_and_measure_results import print_totals
        print_totals()
    

if __name__ == "__main__":
    raise SystemExit(main())
