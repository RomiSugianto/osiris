from django import forms
from django.forms import ModelForm

from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'cols': 20, 'rows': 5})
        }


class RequestServerNewForm(ModelForm):
    class Meta:
        model = RequestServer
        fields = ('document_number', 'customer', 'implementation_date', 'created_by')
        widgets = {
            'created_by': forms.HiddenInput(),
            'implementation_date': forms.DateInput(attrs={'type': 'date'}),
        }


class RequestServerForm(ModelForm):
    class Meta:
        model = RequestServer
        fields = ('document_number', 'customer', 'implementation_date', 'pc', 'pc_status')
        widgets = {
            'implementation_date': forms.DateInput(attrs={'type': 'date'}),
        }


class RequestServerSetPcForm(ModelForm):
    class Meta:
        model = RequestServer
        fields = ('pc', 'pc_status')


class PrincipalForm(ModelForm):
    class Meta:
        model = Principal
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'cols': 20, 'rows': 5})
        }


class DistributorForm(ModelForm):
    class Meta:
        model = Distributor
        fields = '__all__'
        exclude = ('principal',)
        widgets = {
            'address': forms.Textarea(attrs={'cols': 20, 'rows': 5})
        }


class AntiVirusForm(ModelForm):
    class Meta:
        model = AntiVirus
        fields = '__all__'
        widgets = {
            'activated_at': forms.DateInput(attrs={'type': 'date'}),
            'expired_at': forms.DateInput(attrs={'type': 'date'}),
            'created_at': forms.HiddenInput(),
            'updated_at': forms.HiddenInput(),
            'activation_link': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }


class PcForm(ModelForm):
    ram1 = forms.ModelChoiceField(Ram.objects.filter(ram1__pc_number__isnull=True, ram2__pc_number__isnull=True), required=True, empty_label='RAM SLOT 1', widget=forms.Select(attrs={'class': 'form-control'}))
    ram2 = forms.ModelChoiceField(Ram.objects.filter(ram1__pc_number__isnull=True, ram2__pc_number__isnull=True), required=True, empty_label='RAM SLOT 2', widget=forms.Select(attrs={'class': 'form-control'}))
    hdd = forms.ModelChoiceField(Hdd.objects.filter(pc__isnull=True), required=True, empty_label='HDD', widget=forms.Select(attrs={'class': 'form-control'}))
    ssd = forms.ModelChoiceField(Ssd.objects.filter(pc__isnull=True), required=True, empty_label='SSD', widget=forms.Select(attrs={'class': 'form-control'}))
    psu = forms.ModelChoiceField(Psu.objects.filter(pc__isnull=True), required=True, empty_label='PSU', widget=forms.Select(attrs={'class': 'form-control'}))
    motherboard = forms.ModelChoiceField(Motherboard.objects.filter(pc__isnull=True), required=True, empty_label='MOTHERBOARD', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Pc
        fields = '__all__'


class SsdForm(ModelForm):
    class Meta:
        model = Ssd
        fields = '__all__'


class HddForm(ModelForm):
    class Meta:
        model = Hdd
        fields = '__all__'


class PsuForm(ModelForm):
    class Meta:
        model = Psu
        fields = '__all__'


class RamForm(ModelForm):
    class Meta:
        model = Ram
        fields = '__all__'


class MotherboardForm(ModelForm):
    class Meta:
        model = Motherboard
        fields = '__all__'