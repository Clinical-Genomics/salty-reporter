import argparse
import glob
from datetime import date, datetime
from jinja2 import BaseLoader, Environment, FileSystemLoader, Template
import json
import sys


def main():
    args = parse_args(sys.argv[1:])

    jasen_report_paths = []
    if args.jasen_report_dir:
        jasen_report_paths = glob.glob(f"{args.jasen_report_dir}/*")
    else:
        jasen_report_paths = [args.jasen_report]

    with open(args.sample_info) as sample_info_f:
        sample_infos = json.load(sample_info_f)

    for jasen_report_path in jasen_report_paths:
        process_jasen_report(jasen_report_path, sample_infos)


def parse_args(argv):
    argp = argparse.ArgumentParser()
    argp.add_argument(
        "-d",
        "--jasen-report-dir",
        help="A folder with JASEN report files in JSON format to be parsed",
    )
    argp.add_argument(
        "-j",
        "--jasen-report",
        help="Input JASEN report file in JSON format to be parsed",
    )
    argp.add_argument(
        "-s",
        "--sample-info",
        help="Input sample info file in JSON from CG",
        required=True,
    )
    argp.add_argument(
        "-o",
        "--output-directory",
        help="Path to the output directory where to store generated reports",
        required=True,
    )
    args = argp.parse_args(argv)
    if (not args.jasen_report_dir and not args.jasen_report) or (
        args.jasen_report and args.jasen_report_dir
    ):
        print(
            f"ERROR: One (and only one) of --jasen-report-dir or --jasen-report is required"
        )
        sys.exit(1)

    return args


def process_jasen_report(jasen_report_path, sample_infos):
    with open(jasen_report_path) as jasen_report_f:
        jasen_report = json.load(jasen_report_f)

    # Initiate some dummy objects
    MISSING_IN_JASEN_REPORT = "MISSING IN JASEN REPORT!"
    entry = Entry()

    # ----------------------------------------------------------------------------
    # Populate fields with data from CG metadata and JASEN report as far as possible
    # ----------------------------------------------------------------------------
    jasen_sample_id = jasen_report["sample_id"]

    samples = []
    for sample_info in sample_infos:
        sample = models.Sample(CG_ID_sample=sample_info["CG_ID_sample"])

        sample.CG_ID_project = sample_info["CG_ID_project"]
        sample.Customer_ID = sample_info["Customer_ID"]
        sample.Customer_ID_project = sample_info["Customer_ID_project"]
        sample.Customer_ID_sample = sample_info["Customer_ID_sample"]
        sample.application_tag = sample_info["application_tag"]
        sample.date_arrival = datetime.fromisoformat(sample_info["date_arrival"])
        sample.date_libprep = datetime.fromisoformat(sample_info["date_libprep"])
        sample.date_sequencing = datetime.fromisoformat(sample_info["date_sequencing"])
        sample.method_libprep = sample_info["method_libprep"]
        sample.method_sequencing = sample_info["method_sequencing"]
        sample.priority = sample_info["priority"]
        sample.organism = sample_info["organism"]
        sample.reference = sample_info["reference"]
        sample.sequencing_qc_passed = sample_info["sequencing_qc_passed"]

        mlst_result = [
            tr for tr in jasen_report["typing_result"] if tr["type"] == "mlst"
        ][0]
        sample.ST = mlst_result.get("sequence_type", -1)
        sample.pubmlst_ST = mlst_result.get("sequence_type", -1)
        sample.date_analysis = datetime.fromisoformat(
            jasen_report["run_metadata"]["run"]["date"]
        )

        quast_qc = [qc for qc in jasen_report["qc"] if qc["software"] == "quast"][0]
        quast_res = quast_qc["result"]
        sample.genome_length = (
            -1
        )  # TODO: total_length? target_length? reference_length?
        sample.gc_percentage = quast_res["assembly_gc"]
        sample.n50 = quast_res["n50"]
        sample.contigs = quast_res["n_contigs"]

        postalign_qc = [
            qc for qc in jasen_report["qc"] if qc["software"] == "postalignqc"
        ][0]
        postalign_res = postalign_qc["result"]

        sample.total_reads = postalign_res["tot_reads"]
        sample.insert_size = postalign_res[
            "ins_size"
        ]  # TODO: What is "ins_size_dev" in postalignqc?
        sample.duplication_rate = postalign_res["dup_pct"]
        sample.mapped_rate = float(
            postalign_res["mapped_reads"] / postalign_res["tot_reads"]
        )  # TODO: Verify
        sample.coverage_10x = postalign_res["pct_above_x"]["10"]  # TODO: Verify
        sample.coverage_30x = postalign_res["pct_above_x"]["30"]  # TODO: Verify
        sample.coverage_50x = 0.0  # FIXME: MISSING IN JASEN DATA
        sample.coverage_100x = postalign_res["pct_above_x"]["100"]  # TODO: Verify
        sample.average_coverage = postalign_res["mean_cov"]
        sample.reference_genome = MISSING_IN_JASEN_REPORT  # FIXME: MISSING
        sample.reference_length = quast_res["reference_length"]

        jasen_run = jasen_report["run_metadata"]["run"]
        sample.date_analysis = datetime.fromisoformat(jasen_run["date"])
        sample.method_sequencing = (
            f"() / {jasen_run['sequencing_type']}"  # TODO: Verify
        )

        samples.append(sample)

    # ----------------------------------------------------------------------------
    # End: populate with JASEN data
    # ----------------------------------------------------------------------------

    # Set some dummy values
    version = "1.0"
    user = "ABC"
    verified_organisms = ["Homo Sapiens"]
    todays_date = date.today().isoformat()

    threshold = Threshold()
    reports = [Report()]

    j2env = Environment(loader=FileSystemLoader("./templates"))

    with open("templates/typing_page.html") as tpl_file:
        template_str = tpl_file.read()

    typing_tpl = j2env.get_template("typing_page.html")
    qc_tpl = j2env.get_template("alignment_page.html")
    st_tpl = j2env.get_template("STtracker_page.html")

    # Hack to make the template parsing happy.
    # This is a function that is typically available from Flask, but not here
    # since we don't run Flask
    typing_tpl.globals["url_for"] = url_for
    typing_html = typing_tpl.render(
        samples=samples,
        topsample=samples[0],
        date=todays_date,
        version=version,
        user=user,
        threshold=threshold,
        verified_organisms=verified_organisms,
        reports=reports,
        build=version,
    )
    typing_path = f"{args.output_basename}_typing.html"
    with open(typing_path, "w") as typing_file:
        typing_file.write(typing_html)
        print(f"Wrote typing report to: {typing_path}")

    qc_tpl.globals["url_for"] = url_for
    qc_html = qc_tpl.render(
        samples=samples,
        topsample=samples[0],
        date=todays_date,
        version=version,
        user=user,
        threshold=threshold,
        reports=reports,
    )
    qc_path = f"{args.output_basename}_qc.html"
    with open(qc_path, "w") as qc_file:
        qc_file.write(qc_html)
        print(f"Wrote QC report to: {qc_path}")

    st_tpl.globals["url_for"] = url_for
    st_html = st_tpl.render()  # TODO: Implement
    st_path = f"{args.output_basename}_sttracker.html"
    with open(st_path, "w") as st_file:
        st_file.write(st_html)
        print(f"Wrote ST tracker report to: {st_path}")


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


class Threshold:
    def __init__(self):
        self.average_coverage_fail = -1
        self.average_coverage_warn = -1
        self.bp_100x_warn = 0.0
        self.bp_10x_fail = 0.0
        self.bp_10x_warn = 0.0
        self.bp_30x_warn = 0.0
        self.bp_50x_warn = 0.0
        self.duplication_rate_fail = 0.0
        self.duplication_rate_warn = 0.0
        self.insert_size_fail = -1
        self.insert_size_warn = -1
        self.mapped_rate_fail = 0.0
        self.mapped_rate_warn = 0.0
        self.NTC_total_reads_fail = 0.0
        self.NTC_total_reads_warn = 0.0
        self.total_reads_fail = 0.0
        self.total_reads_warn = 0.0
        self.application_tag = "APP_TAG_NA"


class Report:
    def __init__(self):
        self.date = datetime.now()


if __name__ == "__main__":
    main()
