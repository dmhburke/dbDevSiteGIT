
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

    context = {
        'form': form,
        'uploadedImages': uploadedImages,
        # 'deleteForm': deleteForm,

    }

    return render(request, 'rotateimage.html', context=context)

# Set content variables for report
adjective1 = 'Frenchette'
player1 = 'Lisa'
player2 = 'Daniel'

round_report_text = """Hello {} - this is the original text!

""".format(
            player1,
            adjective1,
            player2
            )


def pollyset(request):

    context={
            'round_report_text': round_report_text,
    }

    return render(request, 'pollyset.html', context=context)

def pollyplay (request):
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
    from contextlib import closing
    import os
    import sys
    import subprocess
    from tempfile import gettempdir
    import subprocess

    # Define session
    polly_client = boto3.Session().client('polly',region_name='us-east-1')

    # Function to create audio file
    def createReport(text, version, voice):
        #Define Polly synthesize_speech request
        response = polly_client.synthesize_speech(
                        VoiceId=voice,
                        OutputFormat='mp3',
                        Text = text,
                        Engine='neural')

        #Create and save audio file
        filename = 'RoundReport-' + version + '-' + voice + '.mp3'
        file = open(filename, 'wb')
        file.write(response['AudioStream'].read())
        file.close()

        #Play audio file when function is executed
        from playsound import playsound
        playsound(filename)
        # return_code = subprocess.call(['afplay', filename])

    # Set report specifics
    speaker_persona = 'Kendra' #<-- Can be form input
    version = '1'

    createReport(round_report_text, version, speaker_persona)

    context = {
        'round_report_text': round_report_text,
    }

    return render(request, 'pollyplay.html', context=context)
