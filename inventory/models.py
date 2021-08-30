import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Principal(models.Model):
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Distributor(models.Model):
    principal = models.ManyToManyField(
        Principal,
        through='Customer',
        through_fields=('distributor', 'principal'))
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Customer(models.Model):
    class Meta:
        unique_together = (('principal','distributor'),)
    principal = models.ForeignKey(Principal, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    ns_code = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return "%s , %s" % (self.principal.name, self.distributor.name)


class Ssd(models.Model):
    size_choices = [
        (120, '120'),
        (250, '250'),
    ]
    manufacturer_choices = [
        ('SanDisk', 'SanDisk')
    ]
    type_choices = [
        ('SSD PLUS', 'SSD PLUS'),
        ('ULTRA', 'ULTRA'),
    ]
    serial_number = models.CharField(max_length=50)
    manufacturer = models.CharField(choices=manufacturer_choices, max_length=50)
    type = models.CharField(choices=type_choices, max_length=50)
    size = models.IntegerField(choices=size_choices)

    def __str__(self):
        return self.serial_number


class Hdd(models.Model):
    size_choices = [
        (160, '160'),
    ]
    manufacturer_choices = [
        ('Seagate', 'Seagate'),
    ]
    type_choices = [
        ('Barracuda 7200.10', 'Barracuda 7200.10'),
    ]
    serial_number = models.CharField(max_length=50)
    manufacturer = models.CharField(choices=manufacturer_choices, max_length=50)
    type = models.CharField(choices=type_choices, max_length=50)
    size = models.IntegerField(choices=size_choices)

    def __str__(self):
        return self.serial_number


class Motherboard(models.Model):
    manufacturer_choices = [
        ('ASUSTek COMPUTER INC', 'Asus'),
    ]
    type_choices = [
        ('H61M-E', 'H61M-E'),
    ]
    cpu_choices = [
        ('i5-2500', 'i5-2500'),
    ]
    serial_number = models.CharField(max_length=50)
    manufacturer = models.CharField(choices=manufacturer_choices, max_length=50)
    cpu = models.CharField(choices=cpu_choices, max_length=50)
    type = models.CharField(choices=type_choices, max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return self.model


class Psu(models.Model):
    manufacturer_choices = [
        ('ARMAGGEDDON', 'Armagedon'),
        ('CORSAIR', 'Corsair'),
    ]
    power_choices = [
        ('450W', '450Watt'),
    ]
    model_choices = [
        ('CV450', 'CV450'),
        ('VOLTRON PRO 475X', 'VOLTRON PRO 475X'),
    ]
    serial_number = models.CharField(max_length=50)
    manufacturer = models.CharField(choices=manufacturer_choices, max_length=50)
    power = models.CharField(choices=power_choices, max_length=50)
    model = models.CharField(choices=model_choices, max_length=50)

    def __str__(self):
        return self.model


class Ram(models.Model):
    type_choices = [
        ('DDR3', 'DDR3'),
    ]
    manufacturer_choices = [
        ('KINGSTON', 'Kingston'),
        ('VGEN', 'Vgen'),
    ]
    size_choices = [
        (4, '4 GB'),
        (8, '8 GB'),
    ]

    serial_number = models.CharField(max_length=50)
    manufacturer = models.CharField(choices=manufacturer_choices, max_length=50)
    size = models.IntegerField(choices=size_choices, default=8)
    type = models.CharField(choices=type_choices, max_length=50)

    def __str__(self):
        return "%s, %s GB, %s" % (self.manufacturer, self.size, self.serial_number)


def increment_pc_number():
    last_pc = Pc.objects.all().order_by('pc_number').last()
    if last_pc is not None:
        pc_int = int(last_pc.pc_number[7:len(last_pc.pc_number)])
        new_pc_int = pc_int + 1
        new_pc_id = 'PC' + str(datetime.datetime.now().strftime("%y")) \
                    + str(datetime.datetime.now().strftime("%m")) \
                    + '-' + str(new_pc_int).zfill(3)
        return new_pc_id
    else:
        return 'PC' + str(datetime.datetime.now().strftime("%y")) + str(datetime.date.today().month) + '-' + '000'


class Pc(models.Model):
    pc_number = models.CharField(primary_key=True, default=increment_pc_number, max_length=50)
    motherboard = models.OneToOneField(Motherboard, null=True, blank=True, on_delete=models.SET_NULL)
    psu = models.OneToOneField(Psu, null=True, blank=True, on_delete=models.SET_NULL)
    ssd = models.OneToOneField(Ssd, null=True, blank=True, on_delete=models.SET_NULL)
    hdd = models.OneToOneField(Hdd, null=True, blank=True, on_delete=models.SET_NULL)
    ram1 = models.OneToOneField(Ram, related_name='ram1', null=True, blank=True, on_delete=models.SET_NULL)
    ram2 = models.OneToOneField(Ram, related_name='ram2', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if Pc.objects.filter(ram1=self.ram1).exists() or Pc.objects.filter(
                ram2=self.ram2).exists() or self.ram1 == self.ram2:
            raise ValueError
        else:
            super(Pc, self).save(*args, **kwargs)

    def __str__(self):
        return self.pc_number

    def get_ram_size(self):
        if self.ram2 is not None:
            return str(self.ram1.size + self.ram2.size) + "GB"
        else:
            return str(self.ram1.size) + "GB"

    def get_ram_serial_number(self):
        if self.ram2 is not None:
            return self.ram1.serial_number + "," + self.ram2.serial_number
        else:
            return self.ram1.serial_number

    def get_ram_manufacturer(self):
        if self.ram2 is not None:
            return self.ram1.manufacturer + "," + self.ram2.manufacturer
        else:
            return self.ram1.manufacturer

    def get_ram_type(self):
        if self.ram2 is not None:
            return self.ram1.type + "," + self.ram2.type
        else:
            return self.ram1.type

    def get_ssd_size(self):
        if self.ssd is not None:
            return str(self.ssd.size) + "GB"

    def get_ssd_serial_number(self):
        if self.ssd is not None:
            return self.ssd.serial_number

    def get_ssd_manufacturer(self):
        if self.ssd is not None:
            return self.ssd.manufacturer

    def get_ssd_type(self):
        if self.ssd is not None:
            return self.ssd.type

    def get_hdd_size(self):
        if self.hdd is not None:
            return str(self.hdd.size) + "GB"

    def get_hdd_serial_number(self):
        if self.hdd is not None:
            return self.hdd.serial_number

    def get_hdd_manufacturer(self):
        if self.hdd is not None:
            return self.hdd.manufacturer

    def get_hdd_type(self):
        if self.hdd is not None:
            return self.hdd.type

    def get_mother_board_cpu(self):
        if self.motherboard is not None:
            return self.motherboard.cpu

    def get_mother_board_serial_number(self):
        if self.motherboard is not None:
            return self.motherboard.serial_number

    def get_mother_board_manufacturer(self):
        if self.motherboard is not None:
            return self.motherboard.manufacturer

    def get_mother_board_type(self):
        if self.motherboard is not None:
            return self.motherboard.type

    def get_mother_board_model(self):
        if self.motherboard is not None:
            return self.motherboard.model

    def get_psu_manufacturer(self):
        if self.psu is not None:
            return self.psu.manufacturer

    def get_psu_serial_number(self):
        if self.psu is not None:
            return self.psu.serial_number

    def get_psu_model(self):
        if self.psu is not None:
            return self.psu.model

    def get_psu_power(self):
        if self.psu is not None:
            return self.psu.power

    def get_spec(self):
        return self.get_ram_size() + "/" + self.get_ssd_size()


class Profile(models.Model):
    department_choices = [
        ('SALES', 'SALES'),
        ('DEV', 'DEV'),
        ('IMP', 'IMP'),
        ('CS', 'CS'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(choices=department_choices, max_length=100)
    signature = models.ImageField(upload_to='signature/')

    def __str__(self):
        return self.user.get_full_name()


def increment_doc_number():
    last_doc = RequestServer.objects.all().order_by('id').last()
    if last_doc is not None:
        doc_int = int(last_doc.document_number[4:len(last_doc.document_number)])
        new_doc_int = doc_int + 1
        new_doc_num = 'PS' + str(datetime.datetime.now().strftime("%y")) + str(new_doc_int).zfill(3)
        return new_doc_num
    else:
        return 'PS' + str(datetime.datetime.now().strftime("%y")) + '000'


def increment_loc_number():
    last_loc = RequestServer.objects.all().order_by('id').last()
    if last_loc is not None:
        loc_int = int(last_loc.location_number[2:len(last_loc.location_number)])
        new_loc_int = loc_int + 1
        new_loc_num = str(datetime.datetime.now().strftime("%y")) + str(new_loc_int).zfill(4)
        return new_loc_num
    else:
        return str(datetime.datetime.now().strftime("%y")) + '0000'


class RequestServer(models.Model):
    remark_choices = [
        ('8GB/120GB', '8GB/120GB'),
        ('16GB/250GB', '16GB/250GB'),
    ]
    status_choices = [
        ('prepare', 'prepare'),
        ('ready', 'ready'),
        ('sent', 'sent'),
        ('completed', 'completed')
    ]

    document_number = models.CharField(default=increment_doc_number, max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location_number = models.CharField(default=increment_loc_number, max_length=20)
    implementation_date = models.DateField('date implementation')
    remark = models.CharField(choices=remark_choices, max_length=50, null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='approve')
    pc = models.OneToOneField(Pc, on_delete=models.CASCADE, null=True, blank=True)
    pc_status = models.CharField(choices=status_choices, max_length=50, null=True, blank=True)
    created_at = models.DateTimeField('date created', default=timezone.now)
    updated_at = models.DateTimeField('date updated', null=True, blank=True)
    approved_at = models.DateTimeField('date approved', null=True, blank=True)
    document_sent_at = models.DateTimeField('date sent document', null=True, blank=True)
    document_received_back_at = models.DateTimeField('date received back document', null=True, blank=True)
    sent_at = models.DateTimeField('date approved', null=True, blank=True)

    def __str__(self):
        return "%s , %s" % (self.customer.principal.name, self.customer.distributor.name)

    def get_creation_date(self):
        if self.created_at is not None:
            return self.created_at.strftime('%M/%d/%Y')

    def get_implementation_date(self):
        if self.implementation_date is not None:
            return self.implementation_date.strftime("%d %B %Y")

    def get_doc_num(self):
        if self.document_number is not None:
            return self.document_number

    def get_attachment_num(self):
        if self.get_doc_num() is not None:
            return self.get_doc_num() + "-L" + self.get_doc_num()[4:len(self.get_doc_num())]

    def is_approved(self):
        now = timezone.now()
        if self.approved_by:
            return True
        else:
            return False

    is_approved.admin_order_field = 'created_at'
    is_approved.boolean = True
    is_approved.short_description = 'Approved yet?'


class AntiVirus(models.Model):
    provider_choices = [
        ('ESET', 'ESET'),
        ('BITDEFENDER', 'BITDEFENDER'),
    ]
    provider = models.CharField(choices=provider_choices, max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    activation_link = models.CharField(max_length=200, null=True, blank=True)
    activated_at = models.DateField()
    expired_at = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)


class RequestSsd(models.Model):
    document_number = models.CharField(default=increment_doc_number, max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    implementation_date = models.DateField('date implementation')
    ssd = models.OneToOneField(Ssd, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date created', default=timezone.now)
    updated_at = models.DateTimeField('date updated', null=True, blank=True)
    document_sent_at = models.DateTimeField('date sent document', null=True, blank=True)
    document_received_back_at = models.DateTimeField('date received back document', null=True, blank=True)
    sent_at = models.DateTimeField('date approved', null=True, blank=True)
