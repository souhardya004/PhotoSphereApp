from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Prefetch

from PhotoApp.forms import PhotoCategoryForm, PhotoForm
from PhotoApp.models import Photo, Photo_category,Like,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


CATEGORY_SHOWCASE = [
    ("Wildlife", "Untamed encounters, patient waits, and the quiet drama of animals in motion."),
    ("Nature", "Landscapes, forests, and weather-filled frames that turn simple light into atmosphere."),
    ("Portrait", "People-first moments with mood, expression, and detail carrying the scene."),
    ("Architecture", "Lines, geometry, and structure captured with a more editorial point of view."),
    ("Street", "Fast observations, candid timing, and the energy of everyday city life."),
    ("Abstract", "Texture, color, and shape-forward shots that feel more interpretive than literal."),
]


def _base_photo_queryset():
    return (
        Photo.objects.select_related("user")
        .prefetch_related(
            "like_set",
            Prefetch(
                "comment_set",
                queryset=Comment.objects.select_related("user").order_by("created_at"),
            ),
            Prefetch("category", queryset=Photo_category.objects.order_by("id")),
        )
        .order_by("-uploaded_at")
    )


def _prepare_photos(queryset):
    photos = list(queryset)

    for photo in photos:
        categories = list(photo.category.all())
        comments = list(photo.comment_set.all())
        likes = list(photo.like_set.all())

        photo.category_names = [category.category_types for category in categories]
        photo.primary_category = photo.category_names[0] if photo.category_names else "General"
        photo.likes_total = len(likes)
        photo.comments_total = len(comments)
        photo.latest_comment = comments[-1] if comments else None

    return photos


# Create your views here.
@login_required
def all_photos(request):
    photos = _prepare_photos(_base_photo_queryset())
    featured_photo = next((photo for photo in photos if photo.image), None)

    category_sections = []
    for category_name, description in CATEGORY_SHOWCASE:
        section_photos = [
            photo for photo in photos
            if photo.image and category_name in photo.category_names
        ]
        category_sections.append({
            "title": category_name,
            "description": description,
            "photos": section_photos,
            "count": len(section_photos),
        })

    context = {
        "photos": photos,
        "featured_photo": featured_photo,
        "category_sections": category_sections,
        "total_photos": len(photos),
        "total_likes": sum(photo.likes_total for photo in photos),
        "total_comments": sum(photo.comments_total for photo in photos),
        "active_collections": sum(1 for section in category_sections if section["count"]),
    }
    return render(request, "PhotoApp/all_photos.html", context)


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
    user_photos = _prepare_photos(_base_photo_queryset().filter(user=request.user))
    liked_photos = _prepare_photos(_base_photo_queryset().filter(like__user=request.user).distinct())
    commented_photos = _prepare_photos(_base_photo_queryset().filter(comment__user=request.user).distinct())

    all_unique_photos_map = {}
    for photo in user_photos + liked_photos + commented_photos:
        all_unique_photos_map.setdefault(photo.id, photo)
    all_unique_photos = list(all_unique_photos_map.values())

    gallery_categories = sorted({
        category_name
        for photo in user_photos
        for category_name in photo.category_names
    })
    hero_photo = user_photos[0] if user_photos else (liked_photos[0] if liked_photos else None)

    context = {
        "photos": user_photos,
        "liked_photos": liked_photos,
        "commented_photos": commented_photos,
        "all_unique_photos": all_unique_photos,
        "hero_photo": hero_photo,
        "uploaded_count": len(user_photos),
        "liked_count": len(liked_photos),
        "commented_count": len(commented_photos),
        "received_likes": sum(photo.likes_total for photo in user_photos),
        "gallery_categories": gallery_categories,
        "gallery_categories_count": len(gallery_categories),
    }
    return render(request, "PhotoApp/profile.html", context)


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
