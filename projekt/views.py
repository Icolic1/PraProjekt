from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Kolegij, Profesor, Korisnik, Admin
from .models import Obavijest
from django.views.decorators.cache import never_cache
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Kolegij
from django.contrib.auth.decorators import login_required
from projekt.models import is_admin, is_professor
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from .models import Kolegij
from projekt.models import is_admin, is_professor
from django.contrib.auth.decorators import login_required
@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('pocetna')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

@login_required
def ja_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'ja.html', context)

@login_required
def kolegij_view(request):
    profesori=Profesor.objects.all()
    kolegiji = Kolegij.objects.all()
    
    user = request.user  # Get the current user # Get the current user # Get the current user
    if hasattr(user, 'profesor') and user.profesor:
        user_role = 'Profesor'
    elif hasattr(user, 'admin') and user.admin:
        user_role = 'Admin'
    else:
        user_role = 'Unknown'

    # Now, you can use the `user_role` variable in your view logic
    if user_role == 'Profesor':
        template_name = 'profesor_kolegij.html'
    elif user_role == 'Admin':
        template_name = 'admin_kolegij.html'
    else:
        template_name = 'default_template.html'

   
    return render(request,  template_name, {'profesori': profesori, 'kolegiji': kolegiji})

from django.shortcuts import render, redirect
from django.utils.timezone import now

@login_required
def pocetna_view(request):
    # Retrieve latest obavijesti first
    obavijesti = Obavijest.objects.all().order_by('-publication_date')

    # Count the number of obavijesti
    obavijesti_count = obavijesti.count()

    # Calculate margin-top in pixels
    margin_top_pixels = obavijesti_count * 50
    margin_top_pixels1 = obavijesti_count * 200
    margin_top_pixels2 = obavijesti_count * 430
    # kreiranje obavijest
    kolegiji = Kolegij.objects.all()

    context = {
        'obavijesti': obavijesti,
        'kolegiji': kolegiji,
        'obavijesti_count': obavijesti_count,
        'margin_top_pixels': margin_top_pixels,  # Pass margin_top_pixels to the template
        'margin_top_pixels1': margin_top_pixels1,  # Pass margin_top_pixels to the template
        'margin_top_pixels2': margin_top_pixels2,  # Pass margin_top_pixels to the template
    }

    return render(request, 'pocetna.html', context)
@login_required
def kolegij_list(request):
    kolegiji = Kolegij.objects.all()
     
    user = request.user  # Get the current user # Get the current user
    if hasattr(user, 'profesor') and user.profesor:
        user_role = 'Profesor'
    elif hasattr(user, 'admin') and user.admin:
        user_role = 'Admin'
    else:
        user_role = 'Unknown'

    # Now, you can use the `user_role` variable in your view logic
    if user_role == 'Profesor':
        template_name = 'profesor_kolegij.html'
    elif user_role == 'Admin':
        template_name = 'admin_kolegij.html'
    else:
        template_name = 'default_template.html'

    return render(request, template_name, {'kolegiji': kolegiji})
@login_required
def create_obavijest(request):
    if request.method == 'POST':
        title = request.POST.get('inputNaslov')
        content = request.POST.get('inputObavijest')
        publication_date = date.today()
        expiration_date = date.today() + timedelta(days=30)
        kolegij_id = request.POST.get('inputPredmet')  # Assuming this is the field for selecting a kolegij

        try:
            kolegij = Kolegij.objects.get(pk=kolegij_id)
            obavijest = Obavijest.objects.create(
                title=title,
                content=content,
                publication_date=publication_date,
                expiration_date=expiration_date,
                kolegij=kolegij  # Assign the selected kolegij here
            )
            obavijest.save()
            return redirect('pocetna')  # Redirect to a success page or any other desired page after saving data
        except Kolegij.DoesNotExist:
            # Handle the case where the selected Kolegij does not exist
            return redirect('pocetna')  # Redirect to the same page with an error message

    return render(request, 'pocetna.html')


@login_required
@login_required
def create_profesor(request):
    user = None  # Initialize user as None before the try block

    if request.method == 'POST':
        first_name = request.POST.get('inputFirst_name')
        last_name = request.POST.get('inputLast_name')
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')

        try:
            # Create a Korisnik object
            user = Korisnik.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)

            # Create a Profesor object and associate it with the Korisnik object
            profesor = Profesor(user=user)
            profesor.save()

            # Redirect to a success page or the same page
            return redirect('http://127.0.0.1:8000/pocetna/')  # Replace 'success_page' with the URL name of your success page

        except IntegrityError:
            # Handle the unique constraint error
            messages.error(request, 'Email already exists. Please choose a different email.')
            return redirect('http://127.0.0.1:8000/kolegij/')  # Redirect back to the same page with an error message

    # Rest of your code here

 

    
    if hasattr(user, 'profesor') and user.profesor:
        user_role = 'Profesor'
    elif hasattr(user, 'admin') and user.admin:
        user_role = 'Admin'
    else:
        user_role = 'Unknown'

    # Now, you can use the `user_role` variable in your view logic
    if user_role == 'Profesor':
        template_name = 'profesor_kolegij.html'
    elif user_role == 'Admin':
        template_name = 'admin_kolegij.html'
    else:
        template_name = 'admin_kolegij.html'


    return render(request, 'http://127.0.0.1:8000/pocetna/')


def create_kolegij(request):
    if request.method == 'POST':
        kolegij_naziv = request.POST.get('inputNaslov')
        profesor_email = request.POST.get('inputProfesor')

        try:
            profesor = Profesor.objects.get(user__email=profesor_email)
            kolegij = Kolegij.objects.create(kolegij_naziv=kolegij_naziv, profesor=profesor)
            return redirect('kolegij_list')  # Redirect to a success page or any other desired page after saving data
        except Profesor.DoesNotExist:
            # Handle the case where the professor was not found
            return redirect('kolegij_list')  # Redirect to the same page with an error message

    user = request.user  # Get the current user
    if hasattr(user, 'profesor') and user.profesor:
        user_role = 'Profesor'
    elif hasattr(user, 'admin') and user.admin:
        user_role = 'Admin'
    else:
        user_role = 'Unknown'

    # Now, you can use the `user_role` variable in your view logic
    if user_role == 'Profesor':
        template_name = 'profesor_kolegij.html'
    elif user_role == 'Admin':
        template_name = 'admin_kolegij.html'
    else:
        template_name = 'default_template.html'


    return render(request, template_name)

@login_required
def edit_obavijest_view(request, obavijest_id):
    try:
        obavijest = Obavijest.objects.get(id=obavijest_id)
    except Obavijest.DoesNotExist:
        return redirect('pocetna')

    if request.method == 'POST':
        obavijest.title = request.POST.get('updated_title')
        obavijest.content = request.POST.get('updated_content')
        obavijest.save()
        return redirect('http://127.0.0.1:8000/pocetna/')

    # Return a JSON response with obavijest data
    return JsonResponse({'id': obavijest.id, 'title': obavijest.title, 'content': obavijest.content})
@login_required
def edit_profesor_view(request, profesor_id):
    try:
        profesor = Profesor.objects.get(id=profesor_id)
    except Profesor.DoesNotExist:
        return redirect('kolegij')

    if request.method == 'POST':
        profesor.user.first_name = request.POST.get('updated_FirstName')
        profesor.user.last_name = request.POST.get('updated_LastName')
        profesor.user.email = request.POST.get('updated_Email')
        profesor.user.password = request.POST.get('updated_Password')
        profesor.save()
        return redirect('http://127.0.0.1:8000/kolegij/')

    # Return a JSON response with obavijest data
    return JsonResponse({'id': profesor.id, 'firstname': profesor.user.first_name, 'lastname': profesor.user.last_name, 'email': profesor.user.email, 'password': profesor.user.password})
@login_required
def edit_kolegij_view(request, kolegij_id):
    try:
        kolegij = Kolegij.objects.get(id=kolegij_id)
       
    except Profesor.DoesNotExist:
        return redirect('kolegij')

    if request.method == 'POST':
        kolegij.kolegij_naziv = request.POST.get('updated_Kolegij')
        kolegij.profesor = request.POST.get('updated_Profesor')
       
        kolegij.save()
        return redirect('http://127.0.0.1:8000/kolegij/')
    profesori = Profesor.objects.all()

    # Return a JSON response with obavijest data
    return JsonResponse({'id': kolegij.id, 'kolegij':  kolegij.kolegij_naziv, 'profesori': profesori,'profesor': kolegij.profesor})

@login_required
def get_obavijest_view(request, obavijest_id):
    obavijest = get_object_or_404(Obavijest, pk=obavijest_id)
    data = {
        'id': obavijest.id,
        'title': obavijest.title,
        'content': obavijest.content,
        # Include other relevant fields here
    }
    return JsonResponse(data)
@login_required
def get_profesor_view(request, profesor_id):
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    data = {'id': profesor.id, 'firstname': profesor.user.first_name, 'lastname': profesor.user.last_name, 'email': profesor.user.email, 'password': ""}
    return JsonResponse(data)
@login_required
def get_kolegij_view(request, kolegij_id):
    kolegij = get_object_or_404(Kolegij, pk=kolegij_id)

    profesori=Profesor.objects.all()
    data = {'id': kolegij.id, 'kolegij': kolegij.kolegij_naziv,'profesori': profesori}
    return JsonResponse(data)
@login_required
def kolegij_list(request):
    user = request.user  # Get the current user
    if hasattr(user, 'profesor') and user.profesor:
        user_role = 'Profesor'
    elif hasattr(user, 'admin') and user.admin:
        user_role = 'Admin'
    else:
        user_role = 'Unknown'

    # Now, you can use the `user_role` variable in your view logic
    if user_role == 'Profesor':
        template_name = 'profesor_kolegij.html'
    elif user_role == 'Admin':
        template_name = 'admin_kolegij.html'
    else:
        template_name = 'default_template.html'

 
    kolegiji = Kolegij.objects.all()

    return render(request, template_name, {'kolegiji': kolegiji})
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
def delete_obavijest(request, obavijest_id):
    obavijest = get_object_or_404(Obavijest, pk=obavijest_id)

    # Check if the user has permission to delete the obavijest
    if request.user.has_perm('projekt.delete_obavijest'):
        obavijest.delete()
        return JsonResponse({'message': 'Obavijest deleted successfully'})

    return JsonResponse({'message': 'Permission denied'}, status=403)