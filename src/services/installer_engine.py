from src.services.config_writer import ConfigWriter

from pathlib import Path

from src.services.installation_result import InstallationResult

from src.services.file_deployment_service import FileDeploymentService

import subprocess


class InstallerEngine:

    def __init__(self, context):
        self.context = context

        self.project_root = Path(__file__).resolve().parents[2]

        self.runtime_package = self.project_root /  "build" / "BackupAgent"


    def install(self):

        deployment = FileDeploymentService(
            self.runtime_package,
            Path(self.context.install_directory)
)

        print(f"Runtime package: {self.runtime_package}")
        print(f"Install directory: {self.context.install_directory}")
        deployment.deploy()

        install_ps1 = (
            Path(self.context.install_directory)
            / "Modules"
            / "Install.ps1"
)

        writer = ConfigWriter(self.context)

        config_path = writer.write()

        if not config_path.exists():
            return InstallationResult(
        success=False,
        exit_code=-1,
        stdout="",
        stderr=f"Configuration file not found: {config_path}"
    )

        if not install_ps1.exists():
            return InstallationResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Installer script not found: {install_ps1}"
    )

        try:
            print("Install.ps1 :", install_ps1)
            print("Config path :", config_path)
            print("Config exists:", config_path.exists())

            process = subprocess.run(
                [
                    "powershell.exe",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(install_ps1),
                    "-ConfigFile",
                    str(config_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=600,
            )
            print("Exit Code:", process.returncode)
            print("STDOUT:")
            print(process.stdout)
            print("STDERR:")
            print(process.stderr)
        except Exception as e:

            return InstallationResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=str(e)
            )

        return InstallationResult(
            success=process.returncode == 0,
            exit_code=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr
        )