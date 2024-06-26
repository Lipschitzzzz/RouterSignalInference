from typing import Any
from django.db import models
from django.core.validators import MinValueValidator

class LocationInfo(models.Model):
    seq_no = models.BigIntegerField(validators=[MinValueValidator(0)]) # 消息计数器
    ue_id = models.BigIntegerField(validators=[MinValueValidator(0)]) # UE 唯一标识

    serv_pci = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 服务小区PCI
    serv_rsrp = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 服务小区测量RSRP
    serv_rsrq = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 服务小区测量RSRQ
    serv_sinr = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 服务小区测量SINR
    serv_ta = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 服务小区ta调整量
    serv_rssi = models.SmallIntegerField() # 服务小区测试rssi, dbm

    reserve_1 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 保留位，字节对齐
    reserve_2 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 保留位，字节对齐

    nbr_pci_1 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区1PCI
    nbr_rsrp_1 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区1测量RSRP
    nbr_rsrq_1 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区1测量RSRQ
    nbr_sinr_1 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区1测量SINR

    nbr_pci_2 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区2PCI
    nbr_rsrp_2 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区2测量RSRP
    nbr_rsrq_2 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区2测量RSRQ
    nbr_sinr_2 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区2测量SINR

    nbr_pci_3 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区3PCI
    nbr_rsrp_3 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区3测量RSRP
    nbr_rsrq_3 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区3测量RSRQ
    nbr_sinr_3 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区3测量SINR

    nbr_pci_4 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区4PCI
    nbr_rsrp_4 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区4测量RSRP
    nbr_rsrq_4 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区4测量RSRQ
    nbr_sinr_4 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区4测量SINR

    nbr_pci_5 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区5PCI
    nbr_rsrp_5 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区5测量RSRP
    nbr_rsrq_5 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区5测量RSRQ
    nbr_sinr_5 = models.SmallIntegerField(validators=[MinValueValidator(0)]) # 相邻小区5测量SINR

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
    # base_station_id = models.ForeignKey(BaseStation, on_delete = models.CASCADE) # 基站 id
    imsi = models.BigIntegerField() # 手机号码编号


