import argparse
import json

argp = argparse.ArgumentParser()
argp.add_argument(
    "-i", "--input-file", help="Input JASEN report file in JSON format", required=True
)
args = argp.parse_args()


def main():
    with open(args.input_file) as jasen_report_f:
        jasen_report = json.load(jasen_report_f)
    jasen_report_str = json.dumps(jasen_report, indent=8)
    print(jasen_report_str)


if __name__ == "__main__":
    main()
