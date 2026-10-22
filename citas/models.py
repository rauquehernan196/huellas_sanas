from django.db import models


class Mascota(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    especie = models.CharField(max_length=50, verbose_name='Especie')
    raza = models.CharField(max_length=80, verbose_name='Raza')
    nombre_dueno = models.CharField(max_length=150, verbose_name='Nombre del dueño')

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.especie})'


class Cita(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_ATENDIDA = 'atendida'
    ESTADO_CANCELADA = 'cancelada'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_ATENDIDA, 'Atendida'),
        (ESTADO_CANCELADA, 'Cancelada'),
    ]

    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='citas',
        verbose_name='Mascota'
    )
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')
    motivo_consulta = models.TextField(verbose_name='Motivo de consulta')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f'{self.mascota} - {self.fecha} {self.hora}'
