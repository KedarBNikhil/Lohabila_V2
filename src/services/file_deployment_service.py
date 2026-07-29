from pathlib import Path
import shutil


class FileDeploymentService:

    def __init__(self, source: Path, destination: Path):

        self.source = source
        self.destination = destination

    def deploy(self):

        if not self.source.exists():
            raise FileNotFoundError(
            f"Runtime package not found: {self.source}"
        )

        self.destination.mkdir(
            parents=True,
            exist_ok=True
    )

        shutil.copytree(
            self.source,
            self.destination,
            dirs_exist_ok=True
    )