from django.shortcuts import redirect, render

from PhotoApp.forms import PhotoCategoryForm, PhotoForm
from PhotoApp.models import Photo, Photo_category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def all_photos(request):
    photos = Photo.objects.all()
    photoCategories = Photo_category.objects.all()
    return render(request, 'PhotoApp/all_photos.html', {'photos': photos, 'photo_categories': photoCategories})


# views.py
@login_required
def add_photo(request):
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        category_form = PhotoCategoryForm(request.POST)

        if photo_form.is_valid() and category_form.is_valid():
            photo = photo_form.save(commit= False)
            photo.user = request.user
            photo.save()

            category = category_form.save(commit=False)
            # the FK field on Photo_category is called `title` not `photo`
            category.title = photo
            category.save()

            # after adding redirect back to the listing so the new item is visible
            return redirect('all_photos')

    else:
        photo_form = PhotoForm()
        category_form = PhotoCategoryForm()

    return render(request, 'PhotoApp/add_photos.html', {
        'photo_form': photo_form,
        'category_form': category_form
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "PhotoApp/register.html", {"form": form})


@login_required
def delete_photo(request, id):
    photo = Photo.objects.get(id=id)

    if photo.user != request.user:
        return redirect("home")

    photo.delete()
    return redirect("home")

@login_required
def dashboard(request):
    return render(request, "PhotoApp/dashboard.html")