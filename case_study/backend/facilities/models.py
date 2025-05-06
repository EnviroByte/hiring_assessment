from django.db import models

class Facility(models.Model):
    """
    Model representing a facility that reports emissions.
    
    This is a starter implementation. Candidates should extend this model
    with additional fields and methods as needed.
    """
    FACILITY_TYPES = [
        ('GAS_PROCESSING', 'Gas Processing'),
        ('OIL_PRODUCTION', 'Oil Production'),
        ('POWER_GENERATION', 'Power Generation'),
        ('MANUFACTURING', 'Manufacturing'),
        ('OTHER', 'Other'),
    ]
    
    CLASSIFICATION_TYPES = [
        ('LARGE_EMITTER', 'Large Emitter'),
        ('SMALL_EMITTER', 'Small Emitter'),
        ('AGGREGATE', 'Aggregate Facility'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    classification = models.CharField(max_length=50, choices=CLASSIFICATION_TYPES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    tightening_activity_group = models.CharField(max_length=100, null=True, blank=True)
    
    # TODO: Add additional fields and methods as needed
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Facilities"


class FacilityEmission(models.Model):
    """
    Model representing emissions data for a facility.
    
    This is a starter implementation. Candidates should extend this model
    with additional fields and methods as needed.
    """
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='emissions')
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)
    emissions_value = models.DecimalField(max_digits=15, decimal_places=2)
    unit = models.CharField(max_length=10, default='tCO2e')
    
    # TODO: Add additional fields and methods as needed
    
    def __str__(self):
        if self.month:
            return f"{self.facility.name} - {self.year}-{self.month}: {self.emissions_value} {self.unit}"
        return f"{self.facility.name} - {self.year}: {self.emissions_value} {self.unit}"
    
    class Meta:
        unique_together = ('facility', 'year', 'month')
        verbose_name_plural = "Facility Emissions"
