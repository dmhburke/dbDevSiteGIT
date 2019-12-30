from django.shortcuts import render, redirect

#Import models here
from catalog.models import uploadImage

#Import forms here
from catalog.forms import uploadImageForm

# Create your views here.
def rotateimage (request):
    """Function that can rotate image (good for fixing selfies)"""

    if request.method == 'POST':
        form = uploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # post = form.save(commit=False)
            # uploadImage = post.uploadImage
            form.save()
            return redirect('rotateimage')
    else:
        form = uploadImageForm()

    uploadedImages = uploadImage.objects.all()

    context = {
        'form': form,
        'uploadedImages': uploadedImages,

    }

    return render(request, 'rotateimage.html', context=context)
