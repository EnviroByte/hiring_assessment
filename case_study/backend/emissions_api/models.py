from django.db import models
from facilities.models import Facility

class ComplianceProjection(models.Model):
    """
    Model representing compliance projections for a facility.
    
    This is a starter implementation. Candidates should extend this model
    with additional fields and methods as needed.
    """
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='compliance_projections')
    year = models.IntegerField()
    projected_emissions = models.DecimalField(max_digits=15, decimal_places=2)
    compliance_obligation = models.DecimalField(max_digits=15, decimal_places=2)
    compliance_gap = models.DecimalField(max_digits=15, decimal_places=2)
    credit_requirement = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # TODO: Add additional fields and methods as needed
    
    def __str__(self):
        return f"{self.facility.name} - {self.year} Projection"
    
    class Meta:
        unique_together = ('facility', 'year')
        verbose_name_plural = "Compliance Projections"


class EmissionFactor(models.Model):
    """
    Model representing emission factors for different activities.
    
    This is a starter implementation. Candidates should extend this model
    with additional fields and methods as needed.
    """
    activity_type = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=15, decimal_places=6)
    gas = models.CharField(max_length=50, default='CO2')
    source = models.CharField(max_length=255, null=True, blank=True)
    
    # TODO: Add additional fields and methods as needed
    
    def __str__(self):
        return f"{self.activity_type}: {self.value} {self.gas}/{self.unit}"
    
    class Meta:
        verbose_name_plural = "Emission Factors"
