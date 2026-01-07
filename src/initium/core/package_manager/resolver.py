from .winget import WingetPackageManager
from .choco import ChocoPackageManager

class PackageManagerResolver:
    """
    Resolver untuk menentukan package manager yang tersedia
    dan paling masuk akal untuk digunakan.
    """

    def __init__(self):
        self._managers = [
            WingetPackageManager(),
            ChocoPackageManager()
        ]

    def resolve(self):
        """
        Mengembalikan instance pacakge manager yang tersedia.
        Prioritas berdasarkan urutan di _managers.
        Return None jika tidak ada yang tersedia.
        """

        for manager in self._managers:
            if manager.is_available():
                return manager

        return None
