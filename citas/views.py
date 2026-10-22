from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date

from .forms import AtencionCitaForm, MascotaForm
from .models import Cita


def agenda_diaria(request):
    fecha_seleccionada = timezone.localdate()
    fecha_parametro = request.GET.get('fecha')
    if fecha_parametro:
        fecha_seleccionada = parse_date(fecha_parametro)
        if fecha_seleccionada is None:
            return render(
                request,
                'citas/agenda_diaria.html',
                {
                    'fecha': timezone.localdate(),
                    'citas': Cita.objects.none(),
                    'fecha_invalida': True,
                },
                status=400,
            )

    citas = (
        Cita.objects.filter(fecha=fecha_seleccionada)
        .select_related('mascota')
        .order_by('hora')
    )
    return render(
        request,
        'citas/agenda_diaria.html',
        {'fecha': fecha_seleccionada, 'citas': citas},
    )


def nuevo_paciente(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(
                request,
                f'{paciente.nombre} se registró correctamente.',
            )
            return redirect('agenda_diaria')
    else:
        form = MascotaForm()

    return render(request, 'citas/nuevo_paciente.html', {'form': form})


def atender_cita(request, cita_id):
    cita = get_object_or_404(
        Cita.objects.select_related('mascota'),
        pk=cita_id,
    )
    if request.method == 'POST':
        form = AtencionCitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'La atención se guardó correctamente.')
            return redirect(
                f"{reverse('agenda_diaria')}?fecha={cita.fecha.isoformat()}"
            )
    else:
        form = AtencionCitaForm(instance=cita)

    return render(
        request,
        'citas/atender_cita.html',
        {'cita': cita, 'form': form},
    )
