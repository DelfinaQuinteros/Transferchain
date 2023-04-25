from main.repositories import CertificateRepository
from main.models import Certificate


class CertificateService:

    def __init__(self):
        self.repository = CertificateRepository()

    def create(self, certificate: Certificate) -> Certificate:
        certificate = self.repository.create(certificate)
        return certificate

    def find_by_id(self, id):
        certificate = self.repository.find_by_id(id)
        return certificate

    def find_all(self):
        certificates = self.repository.find_all()
        return certificates
