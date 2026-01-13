from abc import ABC, abstractmethod
from typing import Callable

class BasePackageManager(ABC):
    """
    Abstract base class untuk semua package manager.
    Winget, Cocholatey, atau yang lain harus mengikuti kontrak ini.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nama package manager (UI dan Logging).
        """
        pass

    @abstractmethod
    def install(self, pacakge_id: str) -> bool:
        """
        Install package manager identifier yang sesuai
        dengan package manager tersebut.
        Return true jika sukses, false jika gagal.
        """
        pass

    @abstractmethod
    def is_installed(self, pacakge_id: str) -> bool:
        """
        Cek apakah package sudah terinstall.
        """
        pass

    @abstractmethod
    def install_with_log(self, package_id: str, on_output: Callable[[str], None]) -> bool:
        """
        Install package and stream stdout/stderr
        to UI via callback
        """
        pass
