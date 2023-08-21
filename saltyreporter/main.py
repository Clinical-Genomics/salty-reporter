import argparse
import models
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
    "--output-basename",
    help="Base namne for output HTML reports",
    required=True,
)
args = argp.parse_args()


def main():
    with open(args.input_file) as jasen_report_f:
        jasen_report = json.load(jasen_report_f)

    # Initiate some dummy objects
    MISSING_IN_JASEN_REPORT = "MISSING IN JASEN REPORT!"
    entry = Entry()

    # ----------------------------------------------------------------------------
    # Populate fields with data from JASEN report as far as possible
    # ----------------------------------------------------------------------------
    jasen_sample_id = jasen_report["sample_id"]

    sample = models.Sample(CG_ID_sample=jasen_sample_id)
    sample.CG_ID_project = (
        MISSING_IN_JASEN_REPORT  # TODO: Is run_metadata / workflow_name the same?
    )
    sample.Customer_ID_sample = ""  # TODO: Do we have this?
    sample.organism = MISSING_IN_JASEN_REPORT  # TODO: This is pre-specified, right?

    mlst_result = [tr for tr in jasen_report["typing_result"] if tr["type"] == "mlst"][
        0
    ]
    sample.ST = mlst_result.get("sequence_type", -1)
    sample.pubmlst_ST = mlst_result.get("sequence_type", -1)
    sample.date_analysis = datetime.fromisoformat(
        jasen_report["run_metadata"]["run"]["date"]
    )

    quast_qc = [qc for qc in jasen_report["qc"] if qc["software"] == "quast"][0]
    quast_res = quast_qc["result"]
    sample.genome_length = -1  # TODO: total_length? target_length? reference_length?
    sample.gc_percentage = quast_res["assembly_gc"]
    sample.n50 = quast_res["n50"]
    sample.contigs = quast_res["n_contigs"]
    sample.priority = MISSING_IN_JASEN_REPORT  # TODO: look into

    postalign_qc = [qc for qc in jasen_report["qc"] if qc["software"] == "postalignqc"][
        0
    ]
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
    sample.coverage_50x = 0.0  # TODO: MISSING IN JASEN DATA
    sample.coverage_100x = postalign_res["pct_above_x"]["100"]  # TODO: Verify
    sample.average_coverage = postalign_res["mean_cov"]
    sample.reference_genome = MISSING_IN_JASEN_REPORT
    sample.reference_length = quast_res["reference_length"]

    sample.application_tag = MISSING_IN_JASEN_REPORT  # TODO: Look into
    # self.date_arrival = MISSING_DATE TODO: Missing in JASEN data
    # self.date_analysis = MISSING_DATE TODO: Missing in JASEN data
    # self.date_sequencing = MISSING_DATE TODO: Missing in JASEN data
    # self.date_libprep = MISSING_DATE TODO: Missing in JASEN data
    jasen_run = jasen_report["run_metadata"]["run"]
    sample.method_sequencing = f"{jasen_run['sequencing_platform']} / {jasen_run['sequencing_type']}"  # TODO: Verify

    # ----------------------------------------------------------------------------
    # End: populate with JASEN data
    # ----------------------------------------------------------------------------

    # Set some dummy values
    version = "1.0"
    user = "ABC"
    verified_organisms = ["Homo Sapiens"]
    todays_date = date.today().isoformat()

    samples = [sample, sample, sample]
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
    st_html = st_tpl.render() # TODO: Implement
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
