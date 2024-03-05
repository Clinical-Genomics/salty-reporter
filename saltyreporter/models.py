from datetime import date, datetime

from typing import List


class Sample:
    def __init__(self, CG_ID_sample: str):
        # [x] Implement
        self.seq_types: List[
            SeqType
        ] = []  # relationship("Seq_types", back_populates="samples")
        # [/] Implement
        self.projects = None  # relationship("Projects", back_populates="samples")
        # [/] Implement
        self.resistances = None  # relationship("Resistances", back_populates="samples")
        # [/] Implement
        self.steps = None  # relationship("Steps", back_populates="samples")
        # [/] Implement
        self.expacs = None  # relationship("Expacs", back_populates="samples")

        # [x] Implement
        self.CG_ID_sample: str = (
            CG_ID_sample  # db.Column(db.String(15), primary_key=True, nullable=False)
        )
        # [x] Implement
        self.CG_ID_project: str = (
            ""  # db.Column(db.String(15), ForeignKey("projects.CG_ID_project"))
        )
        # [x] Implement
        self.Customer_ID_sample: str = ""  # db.Column(db.String(40))
        # [x] Implement
        self.organism: str = ""  # db.Column(db.String(30))
        # [x] Implement
        self.ST: int = -1  # db.Column(db.SmallInteger, default=-1)
        # [x] Implement
        self.pubmlst_ST: int = -1  # db.Column(db.SmallInteger, default=-1)
        # [>] Implement TODO: Important to fix this!
        self.genome_length: int = -1  # db.Column(db.Integer, default=-1)
        # [x] Implement
        self.gc_percentage: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        # [x] Implement
        self.n50: int = -1  # db.Column(db.Integer, default=-1)
        # [x] Implement
        self.contigs: int = -1  # db.Column(db.Integer, default=-1)
        # [x] Implement
        self.priority: str = ""  # db.Column(db.String(20))

        # [x] Implement
        self.total_reads: int = -1  # db.Column(db.Integer)  # Fetch from bcl2fastq
        # [x] Implement
        self.insert_size: int = -1  # db.Column(db.Integer)
        # [x] Implement
        self.duplication_rate: float = 0.0  # db.Column(db.Float)
        # [>] Implement
        self.mapped_rate: float = 0.0  # db.Column(db.Float)
        # [x] Implement
        self.coverage_10x: float = 0.0  # db.Column(db.Float)
        # [x] Implement
        self.coverage_30x: float = 0.0  # db.Column(db.Float)
        # [-] Implement
        self.coverage_50x: float = 0.0  # db.Column(db.Float)
        # [x] Implement
        self.coverage_100x: float = 0.0  # db.Column(db.Float)
        # [x] Implement
        self.average_coverage: float = 0.0  # db.Column(db.Float)
        # [x] Implement
        self.reference_genome: str = ""  # db.Column(db.String(32))
        # [x] Implement
        self.reference_length: int = -1  # db.Column(db.Integer)

        # [x] Implement
        self.application_tag: str = ""  # db.Column(db.String(15))
        # [x] Implement
        self.date_arrival: datetime = datetime.now()  # db.Column(db.DateTime)
        # [x] Implement
        self.date_analysis: datetime = datetime.now()  # db.Column(db.DateTime)
        # [x] Implement
        self.date_sequencing: datetime = datetime.now()  # db.Column(db.DateTime)
        # [x] Implement
        self.date_libprep: datetime = datetime.now()  # db.Column(db.DateTime)
        # [x] Implement
        self.method_sequencing: str = ""  # db.Column(db.String(15))
        # [x] Implement
        self.method_libprep: str = ""  # db.Column(db.String(15))


class SeqType:
    def __init__(self, CG_ID_sample: str, loci: str):
        # [ ] Implement
        self.samples = None  # relationship("Samples", back_populates="seq_types")

        # [ ] Implement
        self.CG_ID_sample: str = CG_ID_sample  # db.Column(db.String(15), ForeignKey("samples.CG_ID_sample"), primary_key=True)
        # [ ] Implement
        self.loci: str = loci  # db.Column(db.String(10), primary_key=True)

        # [ ] Implement
        self.allele: int = -1  # db.Column(db.SmallInteger)
        # [ ] Implement
        self.contig_name: str = ""  # db.Column(db.String(20), primary_key=True)
        # [ ] Implement
        self.contig_length: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.contig_coverage: float = 0.0  # db.Column(db.Float(6, 2))
        # [ ] Implement
        self.identity: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        # [ ] Implement
        self.span: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        # [ ] Implement
        self.evalue: str = ""  # db.Column(db.String(10))
        # [ ] Implement
        self.bitscore: int = -1  # db.Column(db.SmallInteger)
        # [ ] Implement
        self.subject_length: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.st_predictor: bool = (
            True  # db.Column(db.Boolean, default=0) # TODO: Change back to false
        )
        # [ ] Implement
        self.contig_start: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.contig_end: int = -1  # db.Column(db.Integer)


class Resistances:
    def __init__(self):
        # [ ] Implement
        self.samples = None  # relationship("Samples", back_populates="resistances")
        # [ ] Implement
        self.CG_ID_sample: str = ""  # db.Column(db.String(15), ForeignKey("samples.CG_ID_sample"), primary_key=True)
        # [ ] Implement
        self.gene: str = ""  # db.Column(db.String(50), primary_key=True)
        # [ ] Implement
        self.instance: str = ""  # db.Column(db.String(30), primary_key=True)
        # [ ] Implement
        self.contig_name: str = ""  # db.Column(db.String(20), primary_key=True)
        # [ ] Implement
        self.contig_length: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.contig_coverage: float = 0.0  # db.Column(db.Float(6, 2))
        # [ ] Implement
        self.identity: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        # [ ] Implement
        self.span: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        # [ ] Implement
        self.evalue: str = ""  # db.Column(db.String(10))
        # [ ] Implement
        self.bitscore: int = -1  # db.Column(db.SmallInteger)
        # [ ] Implement
        self.subject_length: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.reference: str = ""  # db.Column(db.String(40))
        # [ ] Implement
        self.resistance: str = ""  # db.Column(db.String(120))
        # [ ] Implement
        self.contig_start: int = -1  # db.Column()
        # [ ] Implement
        self.contig_end: int = -1  # db.Column(db.Integer)


class Expacs:
    def __init__(self):
        # [ ] Implement
        self.samples = None  # relationship("Samples", back_populates="expacs")
        # [ ] Implement
        self.CG_ID_sample: str = ""  # db.Column(db.String(15), ForeignKey("samples.CG_ID_sample"), primary_key=True)
        # [ ] Implement
        self.gene: str = ""  # db.Column(db.String(50), primary_key=True)
        # [ ] Implement
        self.instance: str = ""  # db.Column(db.String(30), primary_key=True)
        # [ ] Implement
        self.contig_name: str = ""  # db.Column(db.String(20), primary_key=True)
        # [ ] Implement
        self.contig_length: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.contig_coverage: float = 0.0  # db.Column(db.Float(6, 2))
        # [ ] Implement
        self.identity: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        # [ ] Implement
        self.span: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        # [ ] Implement
        self.evalue: str = ""  # db.Column(db.String(10))
        # [ ] Implement
        self.bitscore: int = -1  # db.Column(db.SmallInteger)
        # [ ] Implement
        self.subject_length: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.reference: str = ""  # db.Column(db.String(40))
        # [ ] Implement
        self.virulence: str = ""  # db.Column(db.String(120))
        # [ ] Implement
        self.contig_start: int = -1  # db.Column(db.Integer)
        # [ ] Implement
        self.contig_end: int = -1  # db.Column(db.Integer)


class Projects:
    def __init__(self):
        # [ ] Implement
        self.samples = None  # relationship("Samples", back_populates="projects")
        # [ ] Implement
        self.reports = None  # relationship("Reports", back_populates="projects")
        # [ ] Implement
        self.CG_ID_project: str = (
            ""  # db.Column(db.String(15), primary_key=True, nullable=False)
        )
        # [ ] Implement
        self.Customer_ID_project: str = ""  # db.Column(db.String(15))
        # [ ] Implement
        self.date_ordered: datetime = datetime.now()  # db.Column(db.DateTime)
        # [ ] Implement
        self.Customer_ID: str = ""  # db.Column(db.String(15))


class Versions:
    def __init__(self):
        # [ ] Implement
        self.name: str = (
            ""  # db.Column(db.String(45), primary_key=True, nullable=False)
        )
        # [ ] Implement
        self.version: str = ""  # db.Column(db.String(10))


class Reports:
    def __init__(self):
        # [ ] Implement
        self.projects = None  # relationship("Projects", back_populates="reports")
        # [ ] Implement
        self.CG_ID_project: str = ""  # db.Column(db.String(15), ForeignKey("projects.CG_ID_project"), primary_key=True)
        # [ ] Implement
        self.steps_aggregate: str = ""  # db.Column(db.String(100))
        # [ ] Implement
        self.date: datetime = datetime.now()  # db.Column(db.DateTime)
        # [ ] Implement
        self.version: int = -1  # db.Column(db.Integer, default=1, primary_key=True)


class Collections:
    def __init__(self):
        # [ ] Implement
        self.ID_collection: str = ""  # db.Column(db.String(15), primary_key=True)
        # [ ] Implement
        self.CG_ID_sample: str = ""  # db.Column(db.String(15), primary_key=True)
