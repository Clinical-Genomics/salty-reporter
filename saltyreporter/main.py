import argparse
import models
from datetime import date, datetime
from jinja2 import BaseLoader, Environment, FileSystemLoader, Template
import json

argp = argparse.ArgumentParser()
argp.add_argument(
    "-j",
    "--jasen-report",
    help="Input JASEN report file in JSON format",
    required=True,
)
argp.add_argument(
    "-s",
    "--sample-info",
    help="Input sample info file in JSON from CG",
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
    with open(args.jasen_report) as jasen_report_f:
        jasen_report = json.load(jasen_report_f)
    with open(args.sample_info) as sample_info_f:
        sample_infos = json.load(sample_info_f)

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
        ][0]["result"]
        # import ipdb; ipdb.set_trace()
        sample.ST_status = ""
        sample.ST = int(mlst_result.get("sequence_type", -1))
        sample.pubmlst_ST = int(mlst_result.get("sequence_type", -1))
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
        sample.method_sequencing = f"{jasen_run['sequencing_platform']} / {jasen_run['sequencing_type']}"  # TODO: Verify

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


def gen_add_info(sample_info=dict()):
    """Enhances a sample info struct by adding ST_status, threshold info, versioning and sorting"""
    # Set ST status
    output = dict()
    output["samples"] = list()
    output["versions"] = dict()
    output["single_sample"] = ""

    # Sorts sample names
    valid = True
    for sam in sample_info.all():
        if sam.CG_ID_project is None:
            valid = False
            break
    if valid:
        try:
            sample_info = sorted(
                sample_info,
                key=lambda sample: int(
                    sample.CG_ID_sample.replace(sample.CG_ID_project, "")[1:]
                ),
            )
        except ValueError as e:
            pass

    for s in sample_info:
        s.CG_ID_project = s.projects.CG_ID_project
        s.ST_status = str(s.ST)
        if s.Customer_ID_sample is not None:
            if (
                s.Customer_ID_sample.startswith("NTC")
                or s.Customer_ID_sample.startswith("0-")
                or s.Customer_ID_sample.startswith("NK-")
                or s.Customer_ID_sample.startswith("NEG")
                or s.Customer_ID_sample.startswith("CTRL")
                or s.Customer_ID_sample.startswith("Neg")
                or s.Customer_ID_sample.startswith("blank")
                or s.Customer_ID_sample.startswith("dual-NTC")
            ):
                s.ST_status = "Kontroll (prefix)"

        if "Kontroll" in s.ST_status or "Control" in s.ST_status or s.ST == -1:
            s.threshold = "-"
        elif s.ST == -3:
            s.threshold = "Failed"
        elif hasattr(s, "seq_types") and s.seq_types != [] or s.ST == -2:
            near_hits = 0
            s.threshold = "Passed"
            for seq_type in s.seq_types:
                # Identify single deviating allele
                if (
                    seq_type.st_predictor
                    and seq_type.identity >= preset_config["threshold"]["mlst_novel_id"]
                    and preset_config["threshold"]["mlst_id"] > seq_type.identity
                    and 1 - abs(1 - seq_type.span)
                    >= (preset_config["threshold"]["mlst_span"] / 100.0)
                ):
                    near_hits = near_hits + 1
                elif (
                    seq_type.identity < preset_config["threshold"]["mlst_novel_id"]
                    or seq_type.span < (preset_config["threshold"]["mlst_span"] / 100.0)
                ) and seq_type.st_predictor:
                    s.threshold = "Failed"

            if near_hits > 0 and s.threshold == "Passed":
                s.ST_status = "Okänd ({} allele[r])".format(near_hits)
        else:
            s.threshold = "Failed"

        if not ("Control" in s.ST_status or "Kontroll" in s.ST_status) and s.ST < 0:
            if s.ST == -1:
                s.ST_status = "Data saknas"
            elif s.ST <= -4 or s.ST == -2:
                s.ST_status = "Okänd (Novel ST, Novel allele[r])"
            else:
                s.ST_status = "None"

        # Resistence filter
        for r in s.resistances:
            if (
                r.identity >= preset_config["threshold"]["motif_id"]
                and r.span >= preset_config["threshold"]["motif_span"] / 100.0
            ):
                r.threshold = "Passed"
            else:
                r.threshold = "Failed"
        for v in s.expacs:
            if (
                v.identity >= preset_config["threshold"]["motif_id"]
                and v.span >= preset_config["threshold"]["motif_span"] / 100.0
            ):
                v.threshold = "Passed"
            else:
                v.threshold = "Failed"

        # Seq_type and resistance sorting
        s.seq_types = sorted(s.seq_types, key=lambda x: x.loci)
        s.resistances = sorted(s.resistances, key=lambda x: x.instance)
        s.expacs = sorted(s.expacs, key=lambda x: x.gene)
        output["samples"].append(s)
        output["single_sample"] = s

    versions = session.query(Versions).all()
    session.close()
    for version in versions:
        name = version.name[8:]
        output["versions"][name] = version.version

    process = subprocess.Popen("id -un".split(), stdout=subprocess.PIPE)
    user, error = process.communicate()
    output["user"] = user.decode("utf-8").replace(".", " ").title()

    return output


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
