
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Event
from django.utils.dateparse import parse_date, parse_time
from decimal import Decimal, InvalidOperation




# Create your views here.
def homepage(request):
    return render(request, "homepage.html")
def aboutus(request):
    return render(request, "aboutus.html")
def features(request):
    return render(request, "features.html")
def events(request):
    return render(request, "events.html")
def howitworks(request):
    return render(request, "howitworks.html")

def signup(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

    
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

    
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html')


        if User.objects.filter(username=email).exists():
            messages.error(request, "Account already exists.")
            return render(request, 'signup.html')

        User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect('login')

    return render(request, 'signup.html')


# Login
def login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect('homepage')

        else:
            messages.error(
                request,
                "Invalid email or password."
            )

    return render(request, 'login.html')

def logout(request):

    auth_logout(request)

    messages.success(request, "Logged out successfully.")

    return redirect('homepage')

@login_required
def createanevent(request):

    if request.method == "POST":

        try:
            event_name = request.POST.get("event_name", "").strip()
            description = request.POST.get("description", "").strip()
            category = request.POST.get("category")
            event_format = request.POST.get("event_format")

            event_date = parse_date(
                request.POST.get("event_date", "")
            )

            registration_deadline = parse_date(
                request.POST.get("registration_deadline", "")
            )

            start_time = parse_time(
                request.POST.get("start_time", "")
            )

            end_time = parse_time(
                request.POST.get("end_time", "")
            )

            venue = request.POST.get("venue", "").strip()

         
            total_seats_value = request.POST.get("total_seats")

            total_seats = (
                int(total_seats_value)
                if total_seats_value
                else None
            )

        
            is_free = request.POST.get("is_free") == "on"

            ticket_price = (
                Decimal("0")
                if is_free
                else Decimal(request.POST.get("ticket_price") or "0")
            )

          
            event_image = request.FILES.get("event_image")

           
            action = request.POST.get("action", "draft")

            if action not in ["draft", "publish"]:
                raise ValueError("Invalid form submission.")

          
            event = Event(
                created_by=request.user,
                event_name=event_name,
                description=description,
                category=category,
                event_format=event_format,
                event_date=event_date,
                registration_deadline=registration_deadline,
                start_time=start_time,
                end_time=end_time,
                venue=venue,
                total_seats=total_seats,
                is_free=is_free,
                ticket_price=ticket_price,
                event_image=event_image,
                status="PUBLISHED" if action == "publish" else "DRAFT"
            )

           
            event.full_clean()

         
            event.save()

            if event.status == "PUBLISHED":
                messages.success(
                    request,
                    "Event published successfully!"
                )
            else:
                messages.success(
                    request,
                    "Event saved as draft successfully!"
                )

            return redirect("createanevent")

        except (ValidationError, ValueError, InvalidOperation) as error:

            messages.error(
                request,
                f"Unable to save event: {error}"
            )

    return render(request, "createanevent.html")

def enterpriseeventdashboard(request):
    events = Event.objects.all()
    recent_events = events.order_by("-created_at")[:8]

    context = {
        "recent_events": recent_events,
        "total_events": events.count(),
        "published_events": events.filter(status="PUBLISHED").count(),
        "draft_events": events.filter(status="DRAFT").count(),
        "total_seats": sum(
            events.values_list("total_seats", flat=True)
        ),
    }

    return render(request, "enterpriseeventdashboard.html", context)