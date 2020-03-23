
from django.shortcuts import render, redirect

#Import models here
from catalog.models import uploadImage, reportInput

#Import forms here
from catalog.forms import uploadImageForm, PollyForm

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

def pollyset(request):
    """View that sets the details of the voiced report"""
    polly_voice_selected = {}
    player_selected = {}

    if request.method =='POST':
         form = PollyForm(request.POST)
         if form.is_valid():
             polly_voice_selected = form.polly_voice_input(request)
             player_selected = form.player_input(request).player_name

    else:
          form = PollyForm()

    try:
        player_input = reportInput.objects.get(player_name=player_selected).input_one
        player_name = reportInput.objects.get(player_name=player_selected).player_name
    except:
        player_input = "No value"
        player_name = "No value"

# ===START REPORT TEXT===

    round_report_text = """

    Hello {} - this is {} speaking. It is nice to meet you

    """.format(
                player_name,
                polly_voice_selected,
                player_input
                )

# === END REPORT TEXT ===

    request.session['round_report_text'] = round_report_text

    context= {
            # passed variables
            'polly_voice_selected': polly_voice_selected,
            'player_selected': player_selected,
            # other variables
            'form': form,
            'round_report_text': round_report_text,
            }

    return render(request, 'pollyset.html', context=context)


def pollyplay (request, voice):
    """View that sets creates the synthesize_speech function"""

    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
    from contextlib import closing
    import os
    import sys
    import subprocess
    from tempfile import gettempdir

    round_report_text = request.session['round_report_text']

    # Define session
    polly_client = boto3.Session().client('polly',region_name='us-east-1')

    # Function to create audio file
    def createReport(text, version, voice):
        #Define Polly synthesize_speech request
        response = polly_client.synthesize_speech(
                        VoiceId=voice,
                        OutputFormat='mp3',
                        Text = text,
                        Engine='standard')

        #Create and save audio file
        filename = 'RoundReport-' + version + '-' + voice
        file = open(filename, 'wb')
        file.write(response['AudioStream'].read())
        file.close()

        from playsound import playsound
        playsound(filename)

        #Play audio file when function is executed

        # - local CLI -- WORKS WELL DOESNT WORK AWAY FROM LOCAL MACHINE
        # return_code = subprocess.call(['afplay', filename])

        # - pyglet option -
        # import pyglet
        #
        # music = pyglet.resource.media(filename)
        # music.play()
        #
        # pyglet.app.run()

        # - playsound option -- WORKS WELL but FAILS ON HEROKU BUILD

        # - simpleaudio option FAILS AS NO MP3 SUPPORT (and Polly has no wave format)
        # import simpleaudio as sa
        # wave_obj = sa.WaveObject.from_wave_file(filename)
        # play_obj = wave_obj.play()
        # play_obj.wait_done()

        # - pydub option FAILS ERROR NO SUCH FILE/DIRECTORY AS FFPROBE
        # from pydub import AudioSegment
        # from pydub.playback import play
        #
        # sound = AudioSegment.from_mp3(filename)
        # play(sound)

    # from catalog.settings import *
    #
    # s3 = boto3.client(
    # "s3",
    # aws_access_key_id=
    # )


# Set report specifics
    version = '1'
# CALL CREATE REPORT FUNCTION TO GENERATE REPORT
    createReport(round_report_text, version, voice)



    context = {
        # 'round_report_text': round_report_text,
    }

    return render(request, 'pollyplay.html', context=context)

#===VIRTUAL COCKTAIL===
from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.db.models import Q

#Import models here
from catalog.models import masterRecord, restaurantRecord, transactionRecord, addRestaurant

#Import forms here
from catalog.forms import OrderForm, RestaurantSearchForm, AddRestaurantForm


def cocktailhomepage(request):

    restaurant_select = []

    if request.method =='POST':
         form = RestaurantSearchForm(request.POST)
         if form.is_valid():
             restaurant_select = form.search_input(request)

    else:
          form = RestaurantSearchForm()

    # generate list of restaurants
    # restaurant_list = ""

    if len(restaurant_select) == 0:
        restaurant_list = masterRecord.objects.all()
    else:
        restaurant_list = masterRecord.objects.filter(
        Q(restaurant_name__restaurant_name__icontains=restaurant_select)
        ).order_by('-total_amount')

    context = {
    'form': form,
    'restaurant_list': restaurant_list,
    }

    return render(request, 'cocktailhomepage.html', context=context)

def restaurantdetail(request, restaurant_name):

    restaurant_name = restaurantRecord.objects.get(restaurant_name=restaurant_name)

    restaurant_image = restaurant_name.background_image

    if request.method =='POST':
         form = OrderForm(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.restaurant_name = restaurant_name
            post.number_input = post.number_input
            post.amount = post.number_input * 15
            post.save()
            return redirect('paymentconfirm')

    else:
          form = OrderForm()

    request.session['restaurant_name'] = restaurant_name.restaurant_name

    context = {
    'restaurant_name': restaurant_name,
    'restaurant_image': restaurant_image,
    'form': form,
    }

    return render(request, 'restaurantdetail.html', context=context)

def paymentconfirm(request):

    restaurant_name = request.session['restaurant_name']
    number_output = transactionRecord.objects.latest('number_input').number_input

    context = {
    'restaurant_name': restaurant_name,
    'number_output': number_output,
    }

    return render(request, 'paymentconfirm.html', context=context)

def submitrestaurant(request):

    if request.method =='POST':
         form = AddRestaurantForm(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('submitrestaurant') # change to confirmation page
    else:
          form = AddRestaurantForm()

    context = {

    'form': form,

    }

    return render(request, 'submitrestaurant.html', context=context)

def instatest(request):

    from instapy_cli import client
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    username = 'virtualcocktailorg' #your username
    password = 'Rooster2020' #your password
    image = 'minettaImage_h3pc9Np.jpeg' #here you can put the image directory
    text = '' #Here you can put your caption for the post' + '\r\n' + 'you can also put your hashtags #pythondeveloper #webdeveloper'

    with client(username, password) as cli:
        cli.upload(image, text)

    context = {}

    return render(request, 'instatest.html', context=context)
