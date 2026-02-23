from django.db import models

class CryptoAggregate(models.Model):
    symbol = models.CharField(max_length=20)
    window_start = models.DateTimeField()
    window_end = models.DateTimeField()
    total_volume_inr = models.DecimalField(max_digits=18, decimal_places=2)
    avg_price_inr = models.DecimalField(max_digits=18, decimal_places=2)
    trade_count = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'crypto_aggregates'
        managed = False

class WhaleAlert(models.Model):
    symbol = models.CharField(max_length=20)
    alert_timestamp = models.DateTimeField()
    trade_price_inr = models.DecimalField(max_digits=18, decimal_places=2)
    trade_volume_inr = models.DecimalField(max_digits=18, decimal_places=2)
    volume_multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    is_acknowledged = models.BooleanField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'whale_alerts'
        managed = False