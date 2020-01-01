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

    uploadedImages = uploadImage.objects.all().order_by('-uploaded_at')

    # deleteImageValue = {}
    #
    # if request.method == 'POST':
    #     deleteForm = deleteImageForm(request.POST)
    #     if deleteForm.is_valid():
    #         # post = deleteForm.save(commit=False)
    #         # uploadImage = post.uploadImage
    #         deleteImageValue = "Yes"
    #         post.save()
    #         return redirect('rotateimage')
    # else:
    #     deleteForm = deleteImageForm()
    #
    # if deleteImageValue == "Yes":
    #     uploadImage.objects.all().delete()
    # else:
    #     pass

    context = {
        'form': form,
        'uploadedImages': uploadedImages,
        # 'deleteForm': deleteForm,

    }

    return render(request, 'rotateimage.html', context=context)
