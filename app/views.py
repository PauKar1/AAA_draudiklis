from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import (KlientasRegistrationForm, ProfileUpdateForm, KlientasUpdateForm, KlientaiForm,
                    PolisaiForm, NaujaKlientoRegistracijosForma, BrokeriaiUpdateForm, BrokerLoginForm,
                    BrokerRegisterForm, TravelContractForm, InsuranceCostCalculationForm, UserRegisterForm,
                    BrokerKlientaiUserCreateForm, KlientaiUpdateForm)
from .models import (Profile, Country, Paslaugos, Klientai, Brokeriai, Polisai, BrokerProfile,
                     Cover1, Cover2, Cover3, TravelMode, Iskaita)
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction


# Pagrindinis puslapis
def home(request):
    return render(request, 'home.html')


# Žemėlapio peržiūra
def map_view(request):
    return render(request, 'country_map.html')


# Vartotojo registracija
def registracija(request):
    if request.method == 'POST':
        form = KlientasRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    klientas = form.save(commit=False)
                    password = form.cleaned_data['password1']
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['el_pastas']

                    # Užtikrinti, kad vartotojo vardas būtų unikalus
                    if User.objects.filter(username=username).exists():
                        unique_suffix = 1
                        while User.objects.filter(username=f"{username}{unique_suffix}").exists():
                            unique_suffix += 1
                        username = f"{username}{unique_suffix}"

                    # Patikrinti, ar el. paštas jau egzistuoja
                    user, created = User.objects.get_or_create(email=email, defaults={'username': username})
                    if not created:
                        if Klientai.objects.filter(user=user).exists():
                            messages.error(request,
                                           "Nepavyko sukurti paskyros. Vartotojas jau susietas su kitu klientu.")
                            return render(request, 'registracija.html', {'form': form})
                        else:
                            user.username = username
                            user.set_password(password)
                            user.save()
                    else:
                        user.set_password(password)
                        user.save()

                    # Priskirti vartotoją 'Klientai' grupei
                    group, group_created = Group.objects.get_or_create(name='Klientai')
                    user.groups.add(group)

                    # Priskirti vartotoją klientui ir išsaugoti
                    klientas.user = user
                    klientas.save()

                    try:
                        user_profile = user.profile
                    except Profile.DoesNotExist:
                        user_profile = Profile(user=user)
                    user_profile.save()

                    # Autentifikuoti ir prisijungti vartotoją
                    authenticated_user = authenticate(username=username, password=password)
                    if authenticated_user is not None:
                        login(request, authenticated_user)
                        messages.success(request, f"Paskyra sukurta: {username}!")
                        return redirect('registracija_success')
            except IntegrityError as e:
                messages.error(request, "Nepavyko sukurti paskyros dėl vidinės klaidos.")
                print(f"IntegrityError: {e}")  # Debugging output
            except Exception as e:
                messages.error(request, "Nepavyko sukurti paskyros dėl vidinės klaidos.")
                print(f"Exception: {e}")  # Debugging output
        else:
            messages.error(request, "Nepavyko sukurti paskyros. Patikrinkite formą.")
            print(form.errors)  # Debugging output to check form errors
    else:
        form = KlientasRegistrationForm()
    return render(request, 'registracija.html', {'form': form})


# Registracijos sėkmės puslapis (tik prisijungusiems vartotojams)
@login_required
def registracija_success(request):
    return render(request, 'registracija_success.html', {'user': request.user})


# Vartotojo atsijungimas
def logout_view(request):
    logout(request)
    messages.info(request, "Jūs sėkmingai atsijungėte.")
    return redirect('home')


# Kliento paskyros peržiūra ir prisijungimas
def kliento_paskyra(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Sveiki atvykę, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Neteisingas vartotojo vardas arba slaptažodis.")
        else:
            messages.error(request, "Neteisingas vartotojo vardas arba slaptažodis.")
    else:
        form = AuthenticationForm()
    return render(request, 'kliento_paskyra.html', {'form': form})


# Kliento poliso peržiūra (tik prisijungusiems vartotojams)
@login_required
def client_policies(request):
    try:
        klientas = Klientai.objects.get(user=request.user)
        policies = klientas.polisai.all()
    except Klientai.DoesNotExist:
        policies = []
    return render(request, 'client_policies.html', {'policies': policies})


# Kliento informacijos atnaujinimas (tik prisijungusiems vartotojams)
@login_required
def update_klientas(request):
    try:
        klientas = request.user.klientai
    except Klientai.DoesNotExist:
        klientas = Klientai(user=request.user)

    if request.method == 'POST':
        form = KlientasUpdateForm(request.POST, instance=klientas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilis sėkmingai atnaujintas!')
            return redirect('profile')
        else:
            messages.error(request, 'Prašome ištaisyti klaidas formoje.')
    else:
        form = KlientasUpdateForm(instance=klientas)

    return render(request, 'update_klientas.html', {'form': form})


# Naujo vartotojo registracija
def naujas_user_register(request):
    if request.method == 'POST':
        form = NaujaKlientoRegistracijosForma(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Paskyra sukurta: {user.username}!")
            return redirect('profile')
        else:
            messages.error(request, "Nepavyko sukurti paskyros. Patikrinkite formą.")
    else:
        form = NaujaKlientoRegistracijosForma()
    return render(request, 'naujas_user_register.html', {'form': form})


# Pasirinkti paskyros tipą (tik prisijungusiems vartotojams)
@login_required
def choose_account_type(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        if account_type == 'client':
            return redirect('update_klientas')
        elif account_type == 'broker':
            return redirect('update_brokeris')
    return render(request, 'choose_account_type.html')


# Brokerio informacijos atnaujinimas (tik prisijungusiems vartotojams)
@login_required
def update_brokeris(request):
    try:
        brokeris = request.user.brokeriai
    except Brokeriai.DoesNotExist:
        brokeris = Brokeriai(user=request.user)

    if request.method == 'POST':
        form = BrokeriaiUpdateForm(request.POST, instance=brokeris)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brokerio profilis sėkmingai atnaujintas!')
            return redirect('profile')
        else:
            messages.error(request, 'Prašome ištaisyti klaidas formoje.')
    else:
        form = BrokeriaiUpdateForm(instance=brokeris)

    return render(request, 'update_brokeris.html', {'form': form})


# Profilio redagavimas (tik prisijungusiems vartotojams)
@login_required
def profile_view(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        username = request.POST.get('username')
        if form.is_valid():
            if username:
                request.user.username = username
                request.user.save()
            form.save()
            messages.success(request, 'Profilis sėkmingai atnaujintas!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user_profile)

    profile_picture_url = user_profile.picture.url if user_profile.picture else None
    return render(request, 'profile_edit.html',
                  {'form': form, 'profile': user_profile, 'user_profile_picture': profile_picture_url})


# Profilio peržiūra (tik prisijungusiems vartotojams)
@login_required
def profile(request):
    request.user.username
    try:
        klientai = request.user.klientai
        contracts = Polisai.objects.filter(klientai=klientai)
    except Klientai.DoesNotExist:
        klientai = None
        contracts = []

    return render(request, 'profile.html', {'profile': klientai, 'contracts': contracts})


# Draudimo produktų peržiūra
def draudimo_produktai(request):
    return render(request, 'draudimo_produktai.html')


# Kelionių draudimo peržiūra
def keliones_draudimas(request):
    return render(request, 'keliones_draudimas.html')


# Dažniausiai užduodami klausimai
def faq(request):
    return render(request, 'faq.html')


# Kontaktų forma
def contact(request):
    return render(request, 'contact.html')


# Brokerio prisijungimas
def broker_login(request):
    if request.method == 'POST':
        form = BrokerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                try:
                    broker = Brokeriai.objects.get(el_pastas=email)
                    login(request, user)
                    return redirect('broker_profile', broker_id=broker.id)
                except Brokeriai.DoesNotExist:
                    form.add_error(None, 'Brokerio informacija neteisinga.')
            else:
                form.add_error(None, 'Neteisingas vartotojo vardas arba slaptažodis.')
    else:
        form = BrokerLoginForm()
    return render(request, 'broker_login.html', {'form': form})


# Brokerio registracija
def broker_register(request):
    if request.method == 'POST':
        form = BrokerRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['el_pastas']
            password = form.cleaned_data['password']

            # Patikrinti, ar el. paštas jau egzistuoja
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Šis el. paštas jau užregistruotas.')
                return redirect('broker_register')

            user = User.objects.create_user(username=email, email=email, password=password)
            broker = form.save(commit=False)
            broker.user = user
            broker.save()

            # Sukurti BrokerProfile
            BrokerProfile.objects.create(user=user, broker=broker)

            login(request, user)
            return redirect('broker_profile', broker_id=broker.id)
    else:
        form = BrokerRegisterForm()
    return render(request, 'broker_register.html', {'form': form})


# Brokerio profilis (tik prisijungusiems vartotojams)
@login_required
def broker_profile(request, broker_id):
    broker_profile = get_object_or_404(BrokerProfile, broker__id=broker_id)
    clients = Klientai.objects.filter(polisai__brokeriai=broker_profile.broker).distinct()
    contracts = Polisai.objects.filter(brokeriai=broker_profile.broker)

    if request.method == 'POST':
        form = BrokeriaiUpdateForm(request.POST, instance=broker_profile.broker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilis sėkmingai atnaujintas!')
            return redirect('broker_profile', broker_id=broker_id)
    else:
        form = BrokeriaiUpdateForm(instance=broker_profile.broker)

    return render(request, 'broker_profile.html', {
        'profile': broker_profile,
        'form': form,
        'clients': clients,
        'contracts': contracts,
        'user_profile_picture': broker_profile.profile_picture.url if broker_profile.profile_picture else None
    })


# Brokeris sukuria kliento vartotoją
def broker_klientai_user_create(request):
    BrokerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = BrokerKlientaiUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Sukurti Klientai įrašą ir priskirti vartotoją
            client = Klientai(user=user)
            client.save()

            messages.success(request, f'Klientas sėkmingai užregistruotas! Vartotojo vardas: {user.username}')
            return redirect('broker_update_klientas', client_id=client.id)
    else:
        form = BrokerKlientaiUserCreateForm()

    return render(request, 'broker_update_klientas.html', {'form': form})


# Brokeris atnaujina kliento informaciją
def broker_update_klientas(request, client_id):
    klientas = get_object_or_404(Klientai, id=client_id, user=request.user)

    if request.method == 'POST':
        form = KlientaiUpdateForm(request.POST, instance=klientas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilis sėkmingai atnaujintas!')
            return redirect('broker_profile', client_id=klientas.id)
        else:
            messages.error(request, 'Prašome ištaisyti klaidas formoje.')
    else:
        form = KlientaiUpdateForm(instance=klientas)

    return render(request, 'broker_update_klientas.html', {'form': form})


# Brokerio atsijungimas
def broker_logout(request):
    logout(request)
    return render(request, 'broker_logout.html')


# Draudimo kainos skaičiuoklė
def price_calculator(request):
    if request.method == 'POST':
        form = InsuranceCostCalculationForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country']
            travel_mode = form.cleaned_data['travel_mode']
            trip_duration = form.cleaned_data['trip_duration']
            cover1 = form.cleaned_data.get('cover1')
            cover2 = form.cleaned_data.get('cover2')
            cover3 = form.cleaned_data.get('cover3')
            iskaita = form.cleaned_data['iskaita']
            paslaugos = form.cleaned_data['paslaugos']
            paslaugos_kaina = paslaugos.kaina

            # Atlikti kainos skaičiavimą
            base_cost = paslaugos_kaina * trip_duration
            cover1_cost = base_cost * cover1.na_kof if cover1 else 0
            cover2_cost = base_cost * cover2.civ_kof if cover2 else 0
            cover3_cost = base_cost * cover3.med_kof if cover3 else 0
            iskaita_cost = iskaita.sum

            total_cost = base_cost + cover1_cost + cover2_cost + cover3_cost - iskaita_cost

            # Išsaugoti formos duomenis sesijoje
            request.session['policy_data'] = {
                'country': country.id,
                'travel_mode': travel_mode.id,
                'trip_duration': trip_duration,
                'cover1': cover1.id if cover1 else None,
                'cover2': cover2.id if cover2 else None,
                'cover3': cover3.id if cover3 else None,
                'iskaita': iskaita.id,
                'paslaugos': paslaugos.id,
            }

            context = {
                'form': form,
                'total_cost': total_cost,
                'country': country,
                'travel_mode': travel_mode,
                'trip_duration': trip_duration,
                'cover1': cover1,
                'cover2': cover2,
                'cover3': cover3,
                'iskaita': iskaita,
                'paslaugos_kaina': paslaugos_kaina,
                'register_contract_url': reverse('register_policy'),
            }
            return render(request, 'price_calculator.html', context)
        else:
            print(form.errors)
    else:
        form = InsuranceCostCalculationForm()

    return render(request, 'price_calculator.html', {'form': form})


# Kontrakto registracija (tik prisijungusiems vartotojams)
@login_required
def register_contract(request):
    if request.method == 'POST':
        klientai_form = KlientaiForm(request.POST)
        polisai_form = TravelContractForm(request.POST)
        if klientai_form.is_valid() and polisai_form.is_valid():
            klientai = klientai_form.save(commit=False)
            klientai.user = request.user
            klientai.save()

            polisai = polisai_form.save(commit=False)
            polisai.klientai = klientai

            if klientai.broker == request.user.brokerprofile.broker:
                polisai.save()
                return redirect('broker_profile')
            else:
                pass
    else:
        klientai_form = KlientaiForm()
        polisai_form = TravelContractForm()

    return render(request, 'register_contract.html', {'klientai_form': klientai_form, 'polisai_form': polisai_form})


# Vartotojo registracija
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sukurtas vartotojo profilis {username}!')
            login(request, user)
            return redirect('register_client')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# Kliento registracija (tik prisijungusiems vartotojams)
@login_required
def register_client(request):
    try:
        klientai = Klientai.objects.get(user=request.user)
        request.session['client_id'] = klientai.id
        messages.info(request, 'Jūs jau esate registruotas klientas.')
        return redirect('register_policy')
    except Klientai.DoesNotExist:
        pass

    if request.method == 'POST':
        form = KlientaiForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            request.session['client_id'] = client.id
            messages.success(request, 'Klientas sėkmingai užregistruotas. Dabar galite registruoti politiką.')
            return redirect('register_policy')
    else:
        form = KlientaiForm()
    return render(request, 'register_client.html', {'form': form})


# Poliso registracija (tik prisijungusiems vartotojams)
@login_required
def register_policy(request):
    klientai = get_object_or_404(Klientai, user=request.user)

    if request.method == 'POST':
        klientai_form = KlientaiForm(request.POST, instance=klientai)
        polisai_form = PolisaiForm(request.POST)

        if klientai_form.is_valid() and polisai_form.is_valid():
            klientai_form.save()
            policy = polisai_form.save(commit=False)
            policy.klientai = klientai

            # Kainos apskaičiavimas
            trip_duration = (policy.pabaigos_data - policy.pradzios_data).days
            paslaugos_kaina = policy.paslaugos.kaina

            base_cost = paslaugos_kaina * trip_duration
            cover1_cost = base_cost * policy.cover1.na_kof if policy.cover1 else 0
            cover2_cost = base_cost * policy.cover2.civ_kof if policy.cover2 else 0
            cover3_cost = base_cost * policy.cover3.med_kof if policy.cover3 else 0
            iskaita_cost = policy.iskaita.sum

            total_cost = base_cost + cover1_cost + cover2_cost + cover3_cost - iskaita_cost
            policy.price = total_cost

            policy.save()

            # Išsaugoti policy ID sesijoje
            request.session['policy_id'] = policy.id

            messages.success(request, 'Policy registered successfully.')
            return redirect('policy_success')
        else:
            print("Form errors:", klientai_form.errors, polisai_form.errors)
    else:
        klientai_form = KlientaiForm(instance=klientai)
        policy_data = request.session.get('policy_data', {})
        if policy_data:
            polisai_form = PolisaiForm(initial=policy_data)
        else:
            polisai_form = PolisaiForm()

    return render(request, 'register_policy.html', {'klientai_form': klientai_form, 'polisai_form': polisai_form})


# Poliso registracijos sėkmės puslapis
@login_required
def policy_success(request):
    policy_id = request.session.get('policy_id')
    if policy_id:
        policy = get_object_or_404(Polisai, id=policy_id)
        return render(request, 'policy_success.html', {'policy': policy})
    else:
        return render(request, 'policy_success.html', {'policy': None})



