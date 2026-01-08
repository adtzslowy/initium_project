from .base import BasePackageManager

class MockPackageManager(BasePackageManager):
    @property
    def name(self)->str:
        return "mock"

    def is_available(self)->bool:
        return True
    
    def install(self, package_id: str)->bool:
        return True

    def is_installed(self, pacakge_id: str) -> bool:
        return False
