from anyio import sleep
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, FileResponse
from django.template import loader
from django import forms
import yt_dlp
import base64
from pathlib import Path
from os import listdir
import threading




def test(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        url = str()
        if form.is_valid():
            url = request.POST.get('url', '')
            print(url)
            # Redirect to a new URL:
            #return redirect('student_course')
            data = download(url)
            print(data)
            video_path = f'/static/{data[0]}'
            file_name = data[1]

            return render(request, 'downloadfile.html', {'video_path': video_path, 'file_name': file_name})

    else:
        # Display the form for the first time
        form = URLForm()

    # Render the HTML template with the form
    return render(request, 'download.html', {'form': form})

class URLForm(forms.Form):
    # Define your form fields here
    url = forms.CharField(label='URL', max_length=10000)

def download(url: str):
    config = dict()
    path = "project/static/"
    full_file_name = "Not found."
    # get title
    with yt_dlp.YoutubeDL() as dlp:
        title = dlp.sanitize_info(dlp.extract_info(url, download=False))['title']
        file = str(hash(url))
        config['outtmpl'] = {'default': f'project/static/{file}'}

    # download
    with yt_dlp.YoutubeDL(config) as dlp:
        dlp.download([url])

    # get filename and filename extension
    files = listdir(path)
    for f in files:
        if file == f[:len(file)]:
            full_file_name = f

    return [f"{full_file_name}", f"{title}.webm"]

