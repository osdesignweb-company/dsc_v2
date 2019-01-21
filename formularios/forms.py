from django.forms import ModelForm
from .models import Edades, MunicipioAfectado, PersonasSinDiscapacidad, PersonasConDiscapacidad, DescripcionFormulario

class MunicipioForm(ModelForm):
    class Meta:
        model = MunicipioAfectado
        fields = ['municipio_fk','poblacion']

class EdadesForm(ModelForm):
    class Meta:
        model = Edades
        fields = [
            'de_0_a_6',
            'de_7_a_11',
            'de_12_a_14',
            'de_15_a_17',
            'de_18_a_25',
            'de_26_a_60',
            'mas_de_60'
        ]

class PersonaSDForm(ModelForm):
    class Meta:
        model = PersonasSinDiscapacidad
        fields = [
            "cant_indigenas_m",
            "cant_indigenas_f",
            "cant_afro_m",
            "cant_afro_f",
            "cant_raizal_m",
            "cant_raizal_f",
            "cant_palenque_m",
            "cant_palenque_f",
            "cant_campesino_m",
            "cant_campesino_f",
            "cant_romm_m",
            "cant_romm_f",
            "cant_lgbti",
            "cant_singrupo_m",
            "cant_singrupo_f"
        ]

class PersonaCDForm(ModelForm):
    class Meta:
        model = PersonasConDiscapacidad
        fields = [
            "cant_fisica_m",
            "cant_fisica_f",
            "cant_sensorial_m",
            "cant_sensorial_f",
            "cant_intelectual_m",
            "cant_intelectual_f"
        ]

class DescripcionForm(ModelForm):
    class Meta:
        model = DescripcionFormulario
        fields = [
            'fecha_presentacion',
            'mes_reportado',
            'departamento',
            'municipio_form',
            'nombre_proyecto',
            'nombre_operador',
            'cargo',
            'num_contrato',
            'fecha_inicio',
            'fecha_fin',
            'persona_diligencia',
            'correo',
            'cedula',
            'telefono'
        ]