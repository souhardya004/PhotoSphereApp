from django import forms

from PhotoApp.models import Photo_category, Photo


class PhotoCategoryForm(forms.ModelForm):
    # the foreign key to Photo will be set in the view; we don't expose it to the user
    class Meta:
        model = Photo_category
        fields = ['category_types']
        widgets = {
            'category_types': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg'})
        }

class PhotoForm(forms.ModelForm):
    # use the model's choices directly; the form will render a select widget automatically
    # you can customize the widget if you need extra CSS classes later
    class Meta:
        model = Photo
        fields = ['title', 'description', 'date', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }
