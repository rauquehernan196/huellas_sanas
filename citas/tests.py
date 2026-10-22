from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Cita, Mascota


class RecepcionTests(TestCase):
    def setUp(self):
        self.paciente = Mascota.objects.create(
            nombre='Luna',
            especie='Perro',
            raza='Mestiza',
            nombre_dueno='Ana Pérez',
        )

    def test_agenda_muestra_solo_citas_de_la_fecha_seleccionada(self):
        hoy = timezone.localdate()
        ayer = hoy - timezone.timedelta(days=1)
        cita_hoy = Cita.objects.create(
            mascota=self.paciente,
            fecha=hoy,
            hora='09:30',
            motivo_consulta='Vacunación',
        )
        Cita.objects.create(
            mascota=self.paciente,
            fecha=ayer,
            hora='10:00',
            motivo_consulta='Revisión',
        )

        response = self.client.get(reverse('agenda_diaria'), {'fecha': hoy})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['citas']), [cita_hoy])
        self.assertContains(response, 'Ana Pérez')

    def test_agenda_rechaza_una_fecha_invalida(self):
        response = self.client.get(reverse('agenda_diaria'), {'fecha': 'no-es-fecha'})

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            'La fecha indicada no es válida',
            status_code=400,
        )

    def test_registro_guarda_paciente_y_redirige_a_la_agenda(self):
        response = self.client.post(
            reverse('nuevo_paciente'),
            {
                'nombre': 'Toby',
                'especie': 'Gato',
                'raza': 'Siamés',
                'nombre_dueno': 'Luis Gómez',
                'observaciones': 'Alergia a ciertos alimentos',
            },
        )

        self.assertRedirects(response, reverse('agenda_diaria'))
        paciente = Mascota.objects.get(nombre='Toby')
        self.assertEqual(paciente.observaciones, 'Alergia a ciertos alimentos')

    def test_formulario_de_alta_muestra_observaciones(self):
        response = self.client.get(reverse('nuevo_paciente'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Observaciones')
        self.assertContains(response, 'Alergias, antecedentes')

    def test_registro_muestra_errores_si_faltan_datos(self):
        response = self.client.post(
            reverse('nuevo_paciente'),
            {'nombre': '', 'especie': 'Gato', 'raza': 'Siamés', 'nombre_dueno': ''},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio')
        self.assertEqual(Mascota.objects.count(), 1)

    def test_atencion_guarda_sintomas_y_diagnostico(self):
        cita = Cita.objects.create(
            mascota=self.paciente,
            fecha=timezone.localdate(),
            hora='09:30',
            motivo_consulta='Revisión',
        )

        response = self.client.post(
            reverse('atender_cita', args=[cita.pk]),
            {
                'sintomas': 'Falta de apetito desde ayer',
                'diagnostico': 'Gastritis leve',
            },
        )

        cita.refresh_from_db()
        self.assertEqual(cita.sintomas, 'Falta de apetito desde ayer')
        self.assertEqual(cita.diagnostico, 'Gastritis leve')
        self.assertRedirects(
            response,
            f"{reverse('agenda_diaria')}?fecha={cita.fecha.isoformat()}",
        )

    def test_agenda_enlaza_a_la_atencion_de_cada_cita(self):
        cita = Cita.objects.create(
            mascota=self.paciente,
            fecha=timezone.localdate(),
            hora='09:30',
            motivo_consulta='Revisión',
        )

        response = self.client.get(reverse('agenda_diaria'))

        self.assertContains(
            response,
            reverse('atender_cita', args=[cita.pk]),
        )
        self.assertContains(response, 'Registrar')

    def test_ficha_de_atencion_muestra_campos_clinicos(self):
        cita = Cita.objects.create(
            mascota=self.paciente,
            fecha=timezone.localdate(),
            hora='09:30',
            motivo_consulta='Revisión',
        )

        response = self.client.get(reverse('atender_cita', args=[cita.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Síntomas')
        self.assertContains(response, 'Diagnóstico')
        self.assertContains(response, 'Describe los síntomas')

    def test_ficha_de_atencion_inexistente_responde_404(self):
        response = self.client.get(reverse('atender_cita', args=[999]))

        self.assertEqual(response.status_code, 404)
