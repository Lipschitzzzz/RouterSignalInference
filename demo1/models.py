from django.db import models
from django.core.validators import MinValueValidator

class Info(models.Model):
    unsigned_message_count = models.BigIntegerField(validators=[MinValueValidator(0)]) # 消息计数器
    ue_id = models.BigIntegerField(validators=[MinValueValidator(0)]) # UE 唯一标识
    pci_0 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区 PCI
    rsrp_0 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区 RSRP
    pci_1 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区1 PCI
    rsrp_1 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区1 RSRP
    pci_2 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区2 PCI
    rsrp_2 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区2 RSRP
    pci_3 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区3 PCI
    rsrp_3 = models.SmallIntegerField(validators=[MinValueValidator(0)]) #服务小区3 RSRP
