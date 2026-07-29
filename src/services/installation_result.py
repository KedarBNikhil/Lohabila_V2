from dataclasses import dataclass

@dataclass
class InstallationResult:
    success: bool
    exit_code: int
    stdout: str
    stderr: str