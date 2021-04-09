import os
from typing import List, Optional

import snpseq_metadata.utilities
from snpseq_metadata.models.experiment import ExperimentRef
from snpseq_metadata.models.file_models import FastqFile


class Flowcell:
    def __init__(self, runfolder_path: str, samplesheet: str = None) -> None:
        self.runfolder_path = runfolder_path
        self.runfolder_name = os.path.basename(self.runfolder_path)
        if samplesheet is not None:
            self.samplesheet = os.path.basename(samplesheet)
        self.checksum_method = "MD5"

    def __getattr__(self, item) -> str:
        if item == "samplesheet":
            self.samplesheet = snpseq_metadata.utilities.find_samplesheet(
                self.runfolder_path
            )[0]
        return getattr(self, item)

    def get_checksumfile(self) -> Optional[str]:
        checksumfile = os.path.join(
            self.runfolder_path, self.checksum_method, "checksums.md5"
        )
        return checksumfile if os.path.exists(checksumfile) else None

    def get_fastqdir_for_experiment(self, experiment: ExperimentRef) -> str:
        fastqdir = self.runfolder_path
        patterns = [
            ["Unaligned", "Demultiplexing"],
            [experiment.sample_project, f"Project_{experiment.sample_project}"],
            [experiment.sample_id, f"Project_{experiment.sample_id}"],
        ]
        for pattern in patterns:
            fastqdir = os.path.join(
                fastqdir,
                list(
                    filter(
                        lambda d: os.path.isdir(d) and d in pattern,
                        os.listdir(fastqdir),
                    )
                )[0],
            )
        return fastqdir

    def get_experiments(self) -> List[ExperimentRef]:
        samplesheet_data = snpseq_metadata.utilities.parse_samplesheet_data(
            os.path.join(self.runfolder_path, self.samplesheet)
        )
        experiments = []
        for samplesheet_row in samplesheet_data:
            experiment = ExperimentRef.from_samplesheet_row(samplesheet_row)
            if experiment not in experiments:
                experiments.append(experiment)
        return experiments

    def get_files_for_experiment(self, experiment: ExperimentRef) -> List[FastqFile]:
        fastqdir = self.get_fastqdir_for_experiment(experiment)
        fastq_extensions = ["fastq.gz", "fastq", "fq.gz", "fq"]
        fastqfiles = []
        for fastqfile in filter(
            lambda f: any(map(f.endswith, fastq_extensions)),
            os.listdir(fastqdir),
        ):
            fastqpath = os.path.join(fastqdir, fastqfile)
            querypath = os.path.relpath(fastqpath, os.path.dirname(self.runfolder_path))
            try:
                checksum = snpseq_metadata.utilities.lookup_checksum_from_file(
                    checksumfile=self.get_checksumfile(), querypath=querypath
                )
            except OSError:
                checksum = None
            fastqfiles.append(
                FastqFile(
                    filepath=fastqpath,
                    checksum=checksum,
                    checksum_method=self.checksum_method,
                )
            )
        return fastqfiles
