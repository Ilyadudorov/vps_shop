import libvirt
import xml.etree.ElementTree as ET
from django.conf import settings
from .models import Vps

class VpsService:
    def __init__(self):
        """Подключение к гипервизору"""
        self.conn = libvirt.open("qemu:///system")  # Подключаемся к локальному гипервизору
        if self.conn is None:
            raise Exception("Ошибка подключения к гипервизору")

    def create_vps(self, name, cpu, ram, disk_size, user):
        """Создание VPS через libvirt"""
        # Простейший XML-шаблон для создания VPS (упрощенный)
        xml = f"""
        <domain type='kvm'>
            <name>{name}</name>
            <memory unit='MB'>{ram}</memory>
            <vcpu>{cpu}</vcpu>
            <os>
                <type arch='x86_64'>hvm</type>
            </os>
            <devices>
                <disk type='file' device='disk'>
                    <source file='/var/lib/libvirt/images/{name}.img'/>
                    <target dev='vda' bus='virtio'/>
                </disk>
                <interface type='network'>
                    <source network='default'/>
                </interface>
            </devices>
        </domain>
        """

        try:
            self.conn.defineXML(xml)  # Создаем виртуальную машину в libvirt
        except libvirt.libvirtError as e:
            raise Exception(f"Ошибка создания VPS: {str(e)}")

        # Создаем запись в БД Django
        vps = Vps.objects.create(
            name=name,
            user=user,
            cpu=cpu,
            ram=ram,
            disk_size=disk_size,
            status="created"
        )
        return vps

    def delete_vps(self, vps):
        """Удаление VPS из libvirt и БД"""
        domain = self.conn.lookupByName(vps.name)
        if domain:
            domain.undefine()  # Удаляем машину из libvirt

        vps.delete()  # Удаляем из БД

    def restart_vps(self, vps):
        """Перезапуск VPS"""
        domain = self.conn.lookupByName(vps.name)
        if domain:
            domain.reboot(libvirt.VIR_DOMAIN_REBOOT_DEFAULT)
        else:
            raise Exception("Виртуальная машина не найдена")

    def get_status(self, vps):
        """Получение статуса VPS"""
        domain = self.conn.lookupByName(vps.name)
        if domain:
            state, _ = domain.state()
            return state  # Вернет код состояния libvirt
        return "not found"

    def close(self):
        """Закрываем соединение с гипервизором"""
        self.conn.close()