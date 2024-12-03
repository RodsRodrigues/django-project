from django.db import models

class CotacaoHistorico(models.Model):
    code = models.CharField(max_length=100, null=False, blank=False)
    codein = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    high = models.FloatField(null=False, blank=False)
    low = models.FloatField(null=False, blank=False)
    varBid = models.FloatField(null=False, blank=False)
    pctChange = models.FloatField(null=False, blank=False)
    bid = models.FloatField(null=False, blank=False)
    ask = models.FloatField(null=False, blank=False)
    create_date = models.DateTimeField (null=False, blank=False)

    def __str__(self):
        return f"Nome da Moeda:{self.name}"