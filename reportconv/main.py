import argparse
from datetime import date, datetime
from jinja2 import BaseLoader, Environment, FileSystemLoader, Template
import json

argp = argparse.ArgumentParser()
argp.add_argument(
    "-i",
    "--input-file",
    help="Input JASEN report file in JSON format",
    required=True,
)
argp.add_argument(
    "-o",
    "--output-file",
    help="Output HTML report in the style of microSALT",
    required=True,
)
args = argp.parse_args()


def main():
    with open(args.input_file) as jasen_report_f:
        jasen_report = json.load(jasen_report_f)

    with open("templates/typing_page.html") as tpl_file:
        template_str = tpl_file.read()

    j2env = Environment(loader=FileSystemLoader("./templates"))
    tpl = j2env.get_template("typing_page.html")

    # Hack to make the template parsing happy.
    # This is a function that is typically available from Flask, but not here
    # since we don't run Flask
    tpl.globals["url_for"] = url_for

    # Initiate some dummy objects
    entry = Entry()
    samples = [Sample()]
    threshold = Threshold()
    reports = [Report()]

    # Set some dummy values
    version = "1.0"
    user = "ABC"
    verified_organisms = ["Homo Sapiens"]

    html_report = tpl.render(
        samples=samples,
        topsample=samples[0],
        date=date.today().isoformat(),
        version=version,
        user=user,
        threshold=threshold,
        verified_organisms=verified_organisms,
        reports=reports,
        build=version,
    )

    with open(args.output_file, "w") as out_file:
        out_file.write(html_report)
        print(f"Wrote HTML typing report to: {args.output_file}")


def url_for(filetype, filename=""):
    return filename


class Entry:
    def __init__(self):
        self.CG_ID_sample = None
        self.Customer_ID_sample = None
        self.organism = "Organism"
        self.projects = []
        self.pubmlst_ST = None
        self.ST = None


class Sample:
    def __init__(self):
        self.application_tag = ""
        self.average_coverage = ""

        self.CG_ID_sample = ""

        self.coverage_100x = ""
        self.coverage_10x = ""
        self.coverage_30x = ""
        self.coverage_50x = ""

        self.date_arrival = datetime.now()
        self.date_libprep = datetime.now()
        self.date_sequencing = datetime.now()
        self.date_analysis = datetime.now()

        self.duplication_rate = ""
        self.gc_percentage = 0.5

        self.genome_length = 0
        self.insert_size = ""

        self.mapped_rate = ""
        self.method_libprep = ""
        self.method_sequencing = ""

        self.n50 = 0

        self.organism = ""
        self.priority = ""
        self.projects = []

        self.reference_genome = ""
        self.reference_length = 0
        self.resistances = ""

        self.seq_types = ""
        self.ST = 0
        self.ST_status = ""

        self.threshold = 0
        self.total_reads = 0


class Threshold:
    def __init__(self):
        self.average_coverage_fail = ""
        self.average_coverage_warn = ""
        self.bp_100x_warn = ""
        self.bp_10x_fail = ""
        self.bp_10x_warn = ""
        self.bp_30x_warn = ""
        self.bp_50x_warn = ""
        self.duplication_rate_fail = ""
        self.duplication_rate_warn = ""
        self.insert_size_fail = ""
        self.insert_size_warn = ""
        self.mapped_rate_fail = ""
        self.mapped_rate_warn = ""
        self.NTC_total_reads_fail = ""
        self.NTC_total_reads_warn = ""
        self.total_reads_fail = ""
        self.total_reads_warn = ""
        self.application_tag = ""


class Report:
    def __init__(self):
        self.date = datetime.now()


if __name__ == "__main__":
    main()
