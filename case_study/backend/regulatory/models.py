from django.db import models

class RegulatoryRequirement(models.Model):
    """
    Model representing regulatory requirements for emissions compliance.
    
    This is a starter implementation. Candidates should extend this model
    with additional fields and methods as needed.
    """
    FACILITY_CLASSIFICATIONS = [
        ('LARGE_EMITTER', 'Large Emitter'),
        ('SMALL_EMITTER', 'Small Emitter'),
        ('AGGREGATE', 'Aggregate Facility'),
    ]
    
    year = models.IntegerField()
    facility_classification = models.CharField(max_length=50, choices=FACILITY_CLASSIFICATIONS)
    tightening_activity_group = models.CharField(max_length=100)
    reduction_target = models.DecimalField(max_digits=5, decimal_places=4)
    tightening_rate = models.DecimalField(max_digits=5, decimal_places=4)
    credit_use_limit = models.DecimalField(max_digits=5, decimal_places=4)
    carbon_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    # TODO: Add additional fields and methods as needed
    
    def __str__(self):
        return f"{self.tightening_activity_group} - {self.year}"
    
    class Meta:
        unique_together = ('year', 'facility_classification', 'tightening_activity_group')
        verbose_name_plural = "Regulatory Requirements"


class GlobalWarmingPotential(models.Model):
    """
    Model representing global warming potential values for different gases.
    
    This is a starter implementation. Candidates should extend this model
    with additional fields and methods as needed.
    """
    chemical_name = models.CharField(max_length=255)
    gas = models.CharField(max_length=50)
    value = models.IntegerField()
    assessment = models.CharField(max_length=50, default='AR5')
    
    # TODO: Add additional fields and methods as needed
    
    def __str__(self):
        return f"{self.chemical_name} ({self.gas}): {self.value}"
    
    class Meta:
        verbose_name_plural = "Global Warming Potentials"
