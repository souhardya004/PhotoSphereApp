from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse

from PhotoApp.forms import PhotoCategoryForm, PhotoForm
from PhotoApp.models import Photo, Photo_category,Like,Comment
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
        return redirect("profile")

    photo.delete()
    return redirect("profile")

@login_required
def edit_photo(request, id):
    photo = get_object_or_404(Photo, id=id)
    if photo.user != request.user:
        return redirect('profile')

    category = photo.category.first()

    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES, instance=photo)
        if category:
            category_form = PhotoCategoryForm(request.POST, instance=category)
        else:
            category_form = PhotoCategoryForm(request.POST)

        if photo_form.is_valid() and category_form.is_valid():
            photo_form.save()
            
            cat = category_form.save(commit=False)
            cat.title = photo
            cat.save()
            
            return redirect('profile')

    else:
        photo_form = PhotoForm(instance=photo)
        if category:
            category_form = PhotoCategoryForm(instance=category)
        else:
            category_form = PhotoCategoryForm()

    return render(request, 'PhotoApp/edit_photo.html', {
        'photo_form': photo_form,
        'category_form': category_form,
        'photo': photo
    })

@login_required
def dashboard(request):
    return render(request, "PhotoApp/dashboard.html")

@login_required
def profile_view(request) :
    user_photos = Photo.objects.filter(user = request.user).order_by('-uploaded_at')

    liked_photos = Photo.objects.filter(like__user=request.user)
    commented_photos = Photo.objects.filter(comment__user=request.user).distinct()
    
    all_unique_photos = set(list(user_photos) + list(liked_photos) + list(commented_photos))

    context = {
        'photos' : user_photos,
        'liked_photos': liked_photos,
        'commented_photos': commented_photos,
        'all_unique_photos': all_unique_photos,
    }
    return render(request,'PhotoApp/profile.html',context)


@login_required
def toggle_like(request,photo_id):
    photo = get_object_or_404(Photo,id = photo_id)
    like, created = Like.objects.get_or_create(user=request.user, photo=photo, defaults={'like': 1})

    if not created:
        like.delete()

    return JsonResponse({
        'likes': Like.objects.filter(photo=photo).count()
    })


@login_required
def add_comment(request, photo_id):
    if request.method == "POST":
        photo = get_object_or_404(Photo, id=photo_id)
        
        import json
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            text = data.get('comment')
        else:
            text = request.POST.get('comment')

        if text:
            comment = Comment.objects.create(
                user=request.user,
                photo=photo,
                comment=text
            )
            if request.content_type == 'application/json' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({
                    'status': 'success',
                    'username': request.user.username,
                    'text': comment.comment,
                })

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('all_photos')