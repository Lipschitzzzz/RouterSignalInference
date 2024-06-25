from typing import Any
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

class BaseStation(models.Model):
    # def __init__(self, *args: Any, **kwargs: Any) -> None:
    #     super().__init__(*args, **kwargs)
        # self.enci = enci
        # self.longitude = longitude
        # self.latitude = latitude
        # self.height = height
        # self.azimuth = azimuth
    enci = models.IntegerField(validators=[MinValueValidator(0)]) # 基站 id
    # pci = models.BigIntegerField(validators=[MinValueValidator(0)]) # 小区 id 改为外键
    longitude = models.FloatField() # 经度
    latitude = models.FloatField() # 纬度
    height = models.FloatField() # 高度
    azimuth = models.IntegerField(validators=[MinValueValidator(0)]) # 天线水平法线

class PciBaseStation(models.Model):
    # def __init__(self, pci, base_station_id):
    #     self.pci = pci
    #     self.base_station_id = base_station_id
    pci = models.BigIntegerField(validators=[MinValueValidator(0)]) # 小区 id
    base_station_id = models.ForeignKey(BaseStation, on_delete = models.CASCADE) # 基站 id

class MobileBaseStation(models.Model):
    # def __init__(self, msisdn, base_station_id, imsi):
    #     self.msisdn = msisdn
    #     self.base_station_id = base_station_id
    #     self.imsi = imsi
    msisdn = models.BigIntegerField() # 手机号码
    base_station_id = models.ForeignKey(BaseStation, on_delete = models.CASCADE) # 基站 id
    imsi = models.BigIntegerField() # 手机号码编号


