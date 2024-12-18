import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Universidad, Facultad, Carrera, Calificacion, Favorita
from .forms import UniversidadForm, FacultadForm, CarreraForm, CalificacionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.db.models import Avg 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from math import radians, cos, sin, sqrt, atan2
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name='PublicUsers')
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def universidad_list(request):
    filtro_nombre = request.GET.get('nombre', '').strip()
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    radio_km = request.GET.get('radio') 

    favoritas = Favorita.objects.filter(usuario=request.user)
    universidades = Universidad.objects.all()

    if filtro_nombre:
        universidades = universidades.filter(
            Q(nombre__icontains=filtro_nombre) | Q(descripcion__icontains=filtro_nombre)
        )

    if lat and lon and radio_km:
        lat = float(lat)
        lon = float(lon)
        radio_km = float(radio_km)

        from math import radians, cos, sin, sqrt, atan2

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        universidades = [
            uni for uni in universidades
            if haversine(lat, lon, float(uni.latitud), float(uni.longitud)) <= radio_km
        ]

    universidades_data = []
    for universidad in universidades:
        es_favorita = favoritas.filter(universidad=universidad).exists()
        universidad_data = {
            "id": universidad.pk,
            "nombre": universidad.nombre,
            "latitud": float(universidad.latitud) if universidad.latitud is not None else None,
            "longitud": float(universidad.longitud) if universidad.longitud is not None else None,
            "descripcion": universidad.descripcion,
            "imagen_url": universidad.imagen.url if universidad.imagen else None,
            "es_favorita": es_favorita,
            "tipo": universidad.tipo,
            "calificacion_promedio": float(universidad.calificacion_promedio) if universidad.calificacion_promedio is not None else None,
        }
        universidades_data.append(universidad_data)

    return render(request, 'geodata/universidad_list.html', {
        'universidades_json': json.dumps(universidades_data),
        'universidades': universidades,
    })



@login_required
def universidad_create(request):
    if request.method == 'POST':
        form = UniversidadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('universidad_list')
    else:
        form = UniversidadForm()
    return render(request, 'geodata/universidad_form.html', {'form': form})

@login_required
def universidad_edit(request, pk):
    universidad = get_object_or_404(Universidad, pk=pk)
    if request.method == 'POST':
        form = UniversidadForm(request.POST, request.FILES, instance=universidad)
        if form.is_valid():
            form.save()
            return redirect('universidad_list')
    else:
        form = UniversidadForm(instance=universidad)
    return render(request, 'geodata/universidad_form.html', {'form': form})

@login_required
def universidad_delete(request, pk):
    universidad = get_object_or_404(Universidad, pk=pk)
    if request.method == 'POST':
        universidad.delete()
        return redirect('universidad_list')
    return render(request, 'geodata/universidad_confirm_delete.html', {'universidad': universidad})

def universidad_create_edit(request, pk=None):
    # Si se proporciona un pk, es una edición
    if pk:
        universidad = get_object_or_404(Universidad, pk=pk)
    else:
        universidad = Universidad(user=request.user)  # Nuevo objeto para crear

    if request.method == 'POST':
        form = UniversidadForm(request.POST, request.FILES, instance=universidad) 
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

        # Solo coordenadas si se han proporcionado nuevas
        if latitud and longitud:
            universidad.latitud = latitud
            universidad.longitud = longitud

        if form.is_valid():
            form.save()
            return redirect('universidad_list')  
    else:
        form = UniversidadForm(instance=universidad)

    return render(request, 'geodata/universidad_form.html', {'form': form, 'universidad': universidad})

@login_required
def facultad_list(request):
    filtro_nombre = request.GET.get('nombre', '').strip()
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    radio_km = request.GET.get('radio')  

    favoritas = Favorita.objects.filter(usuario=request.user)

    facultades = Facultad.objects.all()

    if filtro_nombre:
        facultades = facultades.filter(
            Q(nombre_facultad__icontains=filtro_nombre) | Q(descripcion__icontains=filtro_nombre)
        )

    if lat and lon and radio_km:
        lat = float(lat)
        lon = float(lon)
        radio_km = float(radio_km)

        from math import radians, cos, sin, sqrt, atan2

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        facultades = [
            fac for fac in facultades
            if haversine(lat, lon, float(fac.latitud), float(fac.longitud)) <= radio_km
        ]

    facultades_data = []
    for facultad in facultades:
        es_favorita = favoritas.filter(facultad=facultad).exists()
        facultad_data = {
            "id": facultad.pk,
            "nombre": facultad.nombre_facultad,
            "latitud": float(facultad.latitud) if facultad.latitud is not None else None,
            "longitud": float(facultad.longitud) if facultad.longitud is not None else None,
            "descripcion": facultad.descripcion,
            "imagen_url": facultad.imagen.url if facultad.imagen else None,
            "es_favorita": es_favorita,
            "universidad": facultad.universidad.tipo,
            "universidad_nom": facultad.universidad.nombre,
            "calificacion_promedio": float(facultad.calificacion_promedio) if facultad.calificacion_promedio is not None else None,
        }
        facultades_data.append(facultad_data)

    return render(request, 'geodata/facultad_list.html', {
        'facultades_json': json.dumps(facultades_data),
        'facultades': facultades,
    })


@login_required
def facultad_create_edit(request, pk=None):
    if pk:
        facultad = get_object_or_404(Facultad, pk=pk)
    else:
        facultad = Facultad(user=request.user)  # Nuevo objeto para crear

    if request.method == 'POST':
        form = FacultadForm(request.POST, request.FILES, instance=facultad)
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

        if latitud and longitud:
            facultad.latitud = latitud
            facultad.longitud = longitud

        if form.is_valid():
            form.save()
            return redirect('facultad_list')  # Redirige a la lista después de guardar
    else:
        form = FacultadForm(instance=facultad)

    return render(request, 'geodata/facultad_form.html', {'form': form, 'facultad': facultad})

@login_required
def facultad_delete(request, pk):
    facultad = get_object_or_404(Facultad, pk=pk)
    if request.method == 'POST':
        facultad.delete()
        return redirect('facultad_list')
    return render(request, 'geodata/facultad_confirm_delete.html', {'facultad': facultad})

@login_required
def carrera_list(request):
    filtro_nombre = request.GET.get('nombre', '').strip()
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    radio_km = request.GET.get('radio') 
    costo_max = request.GET.get('costo_max')

    favoritas = Favorita.objects.filter(usuario=request.user)
    carreras = Carrera.objects.all()

    if filtro_nombre:
        carreras = carreras.filter(
            Q(nombre_carrera__icontains=filtro_nombre) | Q(descripcion__icontains=filtro_nombre)
        )

    if costo_max:
            carreras = carreras.filter(costo_matricula__lte=costo_max)

    if lat and lon and radio_km:
        lat = float(lat)
        lon = float(lon)
        radio_km = float(radio_km)

        from math import radians, cos, sin, sqrt, atan2

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        carreras = [
            car for car in carreras
            if haversine(float(lat), float(lon), float(car.latitud), float(car.longitud)) <= float(radio_km)
        ]

    carreras_data = []
    for carrera in carreras:
        es_favorita = favoritas.filter(carrera=carrera).exists()
        carrera_data = {
            "id": carrera.pk,
            "nombre": carrera.nombre_carrera,
            "latitud": float(carrera.latitud) if carrera.latitud is not None else None,
            "longitud": float(carrera.longitud) if carrera.longitud is not None else None,
            "descripcion": carrera.descripcion,
            "imagen_url": carrera.imagen.url if carrera.imagen else None,
            "es_favorita": es_favorita,
            "universidad": carrera.universidad.tipo,
            "modalidad_inscripcion": carrera.modalidad_inscripcion,
            "costo_matricula": str(carrera.costo_matricula),
            "duracion": carrera.duracion,
            "calificacion_promedio": float(carrera.calificacion_promedio) if carrera.calificacion_promedio is not None else None,
        }
        carreras_data.append(carrera_data)

    return render(request, 'geodata/carrera_list.html', {
        'carreras_json': json.dumps(carreras_data),
        'carreras': carreras,
    })


@login_required
def carrera_create_edit(request, pk=None):
    if pk:
        carrera = get_object_or_404(Carrera, pk=pk)
    else:
        carrera = Carrera(user=request.user)  

    if request.method == 'POST':
        form = CarreraForm(request.POST, request.FILES, instance=carrera)
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

        if latitud and longitud:
            carrera.latitud = latitud
            carrera.longitud = longitud

        if form.is_valid():
            form.save()
            return redirect('carrera_list')  
    else:
        form = CarreraForm(instance=carrera)

    # Relaciones Facultad -> Universidad
    relaciones_facultades = {
        str(facultad.id): facultad.universidad.id for facultad in Facultad.objects.select_related('universidad')
    }

    return render(request, 'geodata/carrera_form.html', {
        'form': form,
        'carrera': carrera,
        'relaciones_facultades': json.dumps(relaciones_facultades)  # Convertir a JSON
    })



@login_required
def carrera_delete(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    if request.method == 'POST':
        carrera.delete()
        return redirect('carrera_list')
    return render(request, 'geodata/carrera_confirm_delete.html', {'carrera': carrera})


def calcular_distancia(lat1, lng1, lat2, lng2):
    R = 6371  
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def public_map_view(request):

    universidades = Universidad.objects.all()
    facultades = Facultad.objects.all()
    carreras = Carrera.objects.all()

    universidades = [u for u in universidades ]
    facultades = [f for f in facultades ]
    carreras = [c for c in carreras ]

    universidades_data = [
        {
            "id": u.pk,
            "nombre": u.nombre,
            "descripcion": u.descripcion,
            "latitud": u.latitud,
            "longitud": u.longitud,
            "imagen_url": u.imagen.url if u.imagen else None,
            "calificacion_promedio": float(u.calificacion_promedio) if u.calificacion_promedio is not None else None,
            "tipo": "Universidad"
        }
        for u in universidades
    ]
    facultades_data = [
        {
            "id": f.pk,
            "nombre": f.nombre_facultad,
            "descripcion": f.descripcion,
            "latitud": f.latitud,
            "longitud": f.longitud,
            "imagen_url": f.imagen.url if f.imagen else None,
            "calificacion_promedio": float(f.calificacion_promedio) if f.calificacion_promedio is not None else None,
            "tipo": "Facultad"
        }
        for f in facultades
    ]
    carreras_data = [
        {
            "id": c.pk,
            "nombre": c.nombre_carrera,
            "descripcion": c.descripcion,
            "latitud": c.latitud,
            "longitud": c.longitud,
            "modalidad_inscripcion": c.modalidad_inscripcion,
            "costo_matricula": str(c.costo_matricula),
            "duracion": c.duracion,
            "imagen_url": c.imagen.url if c.imagen else None,
            "calificacion_promedio": float(c.calificacion_promedio) if c.calificacion_promedio is not None else None,
            "tipo": "Carrera"
        }
        for c in carreras
    ]

    return render(request, 'geodata/public_map.html', {
        'universidades_json': json.dumps(universidades_data),
        'facultades_json': json.dumps(facultades_data),
        'carreras_json': json.dumps(carreras_data)
    })


@login_required
def calificar(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        tipo_id = request.POST.get('tipo_id')
        calificacion_value = int(request.POST.get('calificacion'))
        comentario = request.POST.get('comentario')

        # Verificar si el tipo
        if tipo == 'Universidad':
            tipo_obj = Universidad.objects.get(id=tipo_id)
        elif tipo == 'Facultad':
            tipo_obj = Facultad.objects.get(id=tipo_id)
        elif tipo == 'Carrera':
            tipo_obj = Carrera.objects.get(id=tipo_id)
        else:
            return JsonResponse({'status': 'error', 'message': 'Tipo no válido'}, status=400)

        # Comprobar si el usuario ya ha calificado este punto
        calificacion_existente = Calificacion.objects.filter(
            usuario=request.user,
            universidad=tipo_obj if isinstance(tipo_obj, Universidad) else None,
            facultad=tipo_obj if isinstance(tipo_obj, Facultad) else None,
            carrera=tipo_obj if isinstance(tipo_obj, Carrera) else None
        ).first()

        if calificacion_existente:
            
            calificacion_existente.calificacion = calificacion_value
            calificacion_existente.comentario = comentario
            calificacion_existente.save()
        else:
            
            calificacion = Calificacion(
                usuario=request.user,
                calificacion=calificacion_value,
                comentario=comentario
            )
            
            
            if isinstance(tipo_obj, Universidad):
                calificacion.universidad = tipo_obj
            elif isinstance(tipo_obj, Facultad):
                calificacion.facultad = tipo_obj
            elif isinstance(tipo_obj, Carrera):
                calificacion.carrera = tipo_obj

            calificacion.save()

        # Actualizar el promedio
        if tipo == 'Universidad':
            promedio = Calificacion.objects.filter(universidad=tipo_obj).aggregate(promedio=Avg('calificacion'))['promedio']
            tipo_obj.calificacion_promedio = float(promedio) if promedio is not None else None
            tipo_obj.save()
        elif tipo == 'Facultad':
            promedio = Calificacion.objects.filter(facultad=tipo_obj).aggregate(promedio=Avg('calificacion'))['promedio']
            tipo_obj.calificacion_promedio = float(promedio) if promedio is not None else None
            tipo_obj.save()
        elif tipo == 'Carrera':
            promedio = Calificacion.objects.filter(carrera=tipo_obj).aggregate(promedio=Avg('calificacion'))['promedio']
            tipo_obj.calificacion_promedio = float(promedio) if promedio is not None else None
            tipo_obj.save()

        return JsonResponse({'status': 'success', 'message': 'Calificación guardada con éxito'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)





def top_items_view(request):
    top_universidades = Universidad.objects.annotate(promedio=Avg('calificacion_promedio')) \
                                           .order_by('-promedio')[:3]
    
    top_facultades = Facultad.objects.annotate(promedio=Avg('calificacion_promedio')) \
                                     .order_by('-promedio')[:3]
    
    top_carreras = Carrera.objects.annotate(promedio=Avg('calificacion_promedio')) \
                                  .order_by('-promedio', 'costo_matricula')[:3]
    
    universidades_data = [
        {
            "id": u.pk,
            "nombre": u.nombre,
            "descripcion": u.descripcion,
            "imagen_url": u.imagen.url if u.imagen else None,
            "calProm": float(u.calificacion_promedio) if u.calificacion_promedio is not None else None,
        }
        for u in top_universidades
    ]
    facultades_data = [
        {
            "id": f.pk,
            "nombre": f.nombre_facultad,
            "descripcion": f.descripcion,
            "imagen_url": f.imagen.url if f.imagen else None,
            "calProm": float(f.calificacion_promedio) if f.calificacion_promedio is not None else None,
        }
        for f in top_facultades
    ]
    carreras_data = [
        {
            "id": c.pk,
            "nombre": c.nombre_carrera,
            "descripcion": c.descripcion,
            "imagen_url": c.imagen.url if c.imagen else None,
            "calProm": float(c.calificacion_promedio) if c.calificacion_promedio is not None else None,
            "costo_matricula": str(c.costo_matricula),
            "duracion": c.duracion,
            "modalidad_inscripcion": c.modalidad_inscripcion
        }
        for c in top_carreras
    ]

    return render(request, 'geodata/top_items.html', {
        'universidades': universidades_data,
        'facultades': facultades_data,
        'carreras': carreras_data,
    })


@login_required
def toggle_favorito(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tipo = data.get("tipo")
        objeto_id = data.get("id")

        if tipo == "universidad":
            objeto = Universidad.objects.get(id=objeto_id)
            favorito, creado = Favorita.objects.get_or_create(
                usuario=request.user, universidad=objeto
            )
        elif tipo == "facultad":
            objeto = Facultad.objects.get(id=objeto_id)
            favorito, creado = Favorita.objects.get_or_create(
                usuario=request.user, facultad=objeto
            )
        elif tipo == "carrera":
            objeto = Carrera.objects.get(id=objeto_id)
            favorito, creado = Favorita.objects.get_or_create(
                usuario=request.user, carrera=objeto
            )

        if not creado:
            favorito.delete()
            return JsonResponse({"status": "removed"})

        return JsonResponse({"status": "added"})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def favoritos_list(request):
    
    favoritos = Favorita.objects.filter(usuario=request.user)

    universidades_favoritas = [f.universidad for f in favoritos if f.universidad]
    facultades_favoritas = [f.facultad for f in favoritos if f.facultad]
    carreras_favoritas = [f.carrera for f in favoritos if f.carrera]

    universidades_data = [
        {
            "id": uni.pk,
            "nombre": uni.nombre,
            "descripcion": uni.descripcion,
            "imagen_url": uni.imagen.url if uni.imagen else None,
            "calProm": float(uni.calificacion_promedio) if uni.calificacion_promedio is not None else None,
        }
        for uni in universidades_favoritas
    ]
    facultades_data = [
        {
            "id": fac.pk,
            "nombre": fac.nombre_facultad,
            "descripcion": fac.descripcion,
            "imagen_url": fac.imagen.url if fac.imagen else None,
            "calProm": float(fac.calificacion_promedio) if fac.calificacion_promedio is not None else None,
        }
        for fac in facultades_favoritas
    ]
    carreras_data = [
        {
            "id": car.pk,
            "nombre": car.nombre_carrera,
            "descripcion": car.descripcion,
            "imagen_url": car.imagen.url if car.imagen else None,
            "calProm": float(car.calificacion_promedio) if car.calificacion_promedio is not None else None,
            "modalidad_inscripcion": car.modalidad_inscripcion,
            "costo_matricula": float(car.costo_matricula) if car.costo_matricula else None,
            "duracion": car.duracion,
        }
        for car in carreras_favoritas
    ]

    return render(request, 'geodata/favoritos_list.html', {
        'universidades': universidades_data,
        'facultades': facultades_data,
        'carreras': carreras_data,
    })

