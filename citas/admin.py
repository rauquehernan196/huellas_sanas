from django.contrib import admin

from .models import Cita, Mascota


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'nombre_dueno')
    search_fields = ('nombre', 'especie', 'raza', 'nombre_dueno')
    list_filter = ('especie',)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'fecha', 'hora', 'estado', 'motivo_consulta')
    list_filter = ('fecha', 'estado')
    search_fields = ('mascota__nombre', 'motivo_consulta', 'mascota__nombre_dueno')
    date_hierarchy = 'fecha'
    ordering = ('fecha', 'hora')
