from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random

def home(request):
    queryset = list(Recipe.objects.all())
    featured_recipes = random.sample(queryset, 3)
    context = {"featured_recipes": featured_recipes}

    queryset = Recipe.objects.all()

    if request.GET.get("search"):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get("search"))

        context = {"recipes": queryset}

        return render(request, "recipes.html", context)

    return render(request, "home.html", context)

@login_required(login_url = "/login/")
def add_recipes(request):
    if request.method == "POST":
        data = request.POST

        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get("recipe_image")
        recipe_prep = data.get("recipe_prep")

        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image,
            recipe_prep= recipe_prep,
        )

        return redirect('/recipes/')
    return render(request, "add_recipe.html")


def recipes(request):
    queryset = Recipe.objects.all()
    context = {"recipes": queryset}
    if request.GET.get("search"):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get("search"))

        context = {"recipes": queryset}

        return render(request, "recipes.html", context)

    return render(request, "recipes.html", context)


def delete_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    queryset.delete()
    return redirect("/recipes/")

@login_required(login_url= "/")
def update_recipe(request, id):
    queryset = Recipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get("recipe_image")
        recipe_prep = data.get("recipe_prep")

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        queryset.recipe_prep = recipe_prep
        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect("/recipes/")

    context = {"recipes" : queryset}
    return render(request, "update_recipes.html", context)

def full_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    context = {"full_recipe": queryset}
    if request.GET.get("search"):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get("search"))

        context = {"recipes": queryset}

        return render(request, "recipes.html", context)

    return render(request, "full_recipe.html", context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username")
            return redirect("/")
        
        user = authenticate(username = username, password= password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("/")

        else:
            login(request, user)
            return redirect("/")

    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("/")



def register(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect("/register/") 

        user = User.objects.create(
            first_name= first_name, 
            last_name= last_name,
            username= username, 
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully")
        return redirect("/register/")

    return render(request, "register.html")