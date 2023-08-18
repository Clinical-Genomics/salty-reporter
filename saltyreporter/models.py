from datetime import date, datetime


class Sample:
    def __init__(self, CG_ID_sample: str):
        self.seq_types = None  # relationship("Seq_types", back_populates="samples")
        self.projects = None  # relationship("Projects", back_populates="samples")
        self.resistances = None  # relationship("Resistances", back_populates="samples")
        self.steps = None  # relationship("Steps", back_populates="samples")
        self.expacs = None  # relationship("Expacs", back_populates="samples")

        self.CG_ID_sample: str = (
            CG_ID_sample  # db.Column(db.String(15), primary_key=True, nullable=False)
        )
        self.CG_ID_project: str = (
            ""  # db.Column(db.String(15), ForeignKey("projects.CG_ID_project"))
        )
        self.Customer_ID_sample: str = ""  # db.Column(db.String(40))
        self.organism: str = ""  # db.Column(db.String(30))
        # ST = Sequence Type
        self.ST: int = -1  # db.Column(db.SmallInteger, default=-1)
        self.pubmlst_ST: int = -1  # db.Column(db.SmallInteger, default=-1)
        self.date_analysis: datetime = (
            None  # db.Column(db.DateTime) # FIXME: Add real date
        )
        self.genome_length: int = -1  # db.Column(db.Integer, default=-1)
        self.gc_percentage: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        self.n50: int = -1  # db.Column(db.Integer, default=-1)
        self.contigs: int = -1  # db.Column(db.Integer, default=-1)
        self.priority: str = ""  # db.Column(db.String(20))

        self.total_reads: int = -1  # db.Column(db.Integer)  # Fetch from bcl2fastq
        self.insert_size: int = -1  # db.Column(db.Integer)
        self.duplication_rate: float = 0.0  # db.Column(db.Float)
        self.mapped_rate: float = 0.0  # db.Column(db.Float)
        self.coverage_10x: float = 0.0  # db.Column(db.Float)
        self.coverage_30x: float = 0.0  # db.Column(db.Float)
        self.coverage_50x: float = 0.0  # db.Column(db.Float)
        self.coverage_100x: float = 0.0  # db.Column(db.Float)
        self.average_coverage: float = 0.0  # db.Column(db.Float)
        self.reference_genome: str = ""  # db.Column(db.String(32))
        self.reference_length: int = -1  # db.Column(db.Integer)

        self.application_tag: str = ""  # db.Column(db.String(15))
        self.date_arrival: datetime = (
            datetime.now()
        )  # db.Column(db.DateTime) # FIXME: Add real date
        self.date_analysis: datetime = (
            datetime.now()
        )  # db.Column(db.DateTime) # FIXME: Add real date
        self.date_sequencing: datetime = (
            datetime.now()
        )  # db.Column(db.DateTime) # FIXME: Add real date
        self.date_libprep: datetime = (
            datetime.now()
        )  # db.Column(db.DateTime) # FIXME: Add real date
        self.method_sequencing: str = ""  # db.Column(db.String(15))
        self.method_libprep: str = ""  # db.Column(db.String(15))


class SeqType:
    def __init__(self, CG_ID_sample: str, loci: str):
        self.samples = None  # relationship("Samples", back_populates="seq_types")

        self.CG_ID_sample: str = CG_ID_sample  # db.Column(db.String(15), ForeignKey("samples.CG_ID_sample"), primary_key=True)
        self.loci: str = loci  # db.Column(db.String(10), primary_key=True)

        self.allele: int = -1  # db.Column(db.SmallInteger)
        self.contig_name: str = ""  # db.Column(db.String(20), primary_key=True)
        self.contig_length: int = -1  # db.Column(db.Integer)
        self.contig_coverage: float = 0.0  # db.Column(db.Float(6, 2))
        self.identity: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        self.span: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        self.evalue: str = ""  # db.Column(db.String(10))
        self.bitscore: int = -1  # db.Column(db.SmallInteger)
        self.subject_length: int = -1  # db.Column(db.Integer)
        self.st_predictor: bool = False  # db.Column(db.Boolean, default=0)
        self.contig_start: int = -1  # db.Column(db.Integer)
        self.contig_end: int = -1  # db.Column(db.Integer)


class Resistances:
    def __init__(self):
        self.samples = None  # relationship("Samples", back_populates="resistances")
        self.CG_ID_sample: str = ""  # db.Column(db.String(15), ForeignKey("samples.CG_ID_sample"), primary_key=True)
        self.gene: str = ""  # db.Column(db.String(50), primary_key=True)
        self.instance: str = ""  # db.Column(db.String(30), primary_key=True)
        self.contig_name: str = ""  # db.Column(db.String(20), primary_key=True)
        self.contig_length: int = -1  # db.Column(db.Integer)
        self.contig_coverage: float = 0.0  # db.Column(db.Float(6, 2))
        self.identity: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        self.span: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        self.evalue: str = ""  # db.Column(db.String(10))
        self.bitscore: int = -1  # db.Column(db.SmallInteger)
        self.subject_length: int = -1  # db.Column(db.Integer)
        self.reference: str = ""  # db.Column(db.String(40))
        self.resistance: str = ""  # db.Column(db.String(120))
        self.contig_start: int = -1  # db.Column()
        self.contig_end: int = -1  # db.Column(db.Integer)


class Expacs:
    def __init__(self):
        self.samples = None  # relationship("Samples", back_populates="expacs")
        self.CG_ID_sample: str = ""  # db.Column(db.String(15), ForeignKey("samples.CG_ID_sample"), primary_key=True)
        self.gene: str = ""  # db.Column(db.String(50), primary_key=True)
        self.instance: str = ""  # db.Column(db.String(30), primary_key=True)
        self.contig_name: str = ""  # db.Column(db.String(20), primary_key=True)
        self.contig_length: int = -1  # db.Column(db.Integer)
        self.contig_coverage: float = 0.0  # db.Column(db.Float(6, 2))
        self.identity: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        self.span: float = 0.0  # db.Column(db.Float(3, 2), default=0.0)
        self.evalue: str = ""  # db.Column(db.String(10))
        self.bitscore: int = -1  # db.Column(db.SmallInteger)
        self.subject_length: int = -1  # db.Column(db.Integer)
        self.reference: str = ""  # db.Column(db.String(40))
        self.virulence: str = ""  # db.Column(db.String(120))
        self.contig_start: int = -1  # db.Column(db.Integer)
        self.contig_end: int = -1  # db.Column(db.Integer)


class Projects:
    def __init__(self):
        self.samples = None  # relationship("Samples", back_populates="projects")
        self.reports = None  # relationship("Reports", back_populates="projects")
        self.CG_ID_project: str = (
            ""  # db.Column(db.String(15), primary_key=True, nullable=False)
        )
        self.Customer_ID_project: str = ""  # db.Column(db.String(15))
        self.date_ordered: datetime = datetime.now()  # db.Column(db.DateTime)
        self.Customer_ID: str = ""  # db.Column(db.String(15))


class Versions:
    def __init__(self):
        self.name: str = (
            ""  # db.Column(db.String(45), primary_key=True, nullable=False)
        )
        self.version: str = ""  # db.Column(db.String(10))


class Reports:
    def __init__(self):
        self.projects = None  # relationship("Projects", back_populates="reports")
        self.CG_ID_project: str = ""  # db.Column(db.String(15), ForeignKey("projects.CG_ID_project"), primary_key=True)
        self.steps_aggregate: str = ""  # db.Column(db.String(100))
        self.date: datetime = datetime.now()  # db.Column(db.DateTime)
        self.version: int = -1  # db.Column(db.Integer, default=1, primary_key=True)


class Collections:
    def __init__(self):
        self.ID_collection: str = ""  # db.Column(db.String(15), primary_key=True)
        self.CG_ID_sample: str = ""  # db.Column(db.String(15), primary_key=True)
