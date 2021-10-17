# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template , request ,send_file
from pytube import YouTube
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def convertFloatToDecimal(f=0.0, precision=2):
    return ("%." + str(precision) + "f") % f

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/video')
def video(downloadPath,thumbnailUrl,title,size,audioPath):
    return render_template('download.html', path=downloadPath, thumbnail=thumbnailUrl, title=title, size=size,audioPath=audioPath)


@app.route('/download', methods=['POST', 'GET'])
def downloadVid():
    if request.method == 'POST':
        url = request.form['url']
        yt = YouTube(url)
        main = yt.streams
        file = main.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().url
        fileSize = main.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().filesize
        audioPath = main.get_audio_only().url
    else:
        url = request.args.get('url')
        yt = YouTube(url)
        file = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().url
        fileSize = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().filesize
        audioPath = yt.streams.filter(progressive=True, file_extension='mp4').get_audio_only().url

    print("Audio Path is : ",audioPath)
    return video(file,yt.thumbnail_url,yt.title,convertFloatToDecimal((fileSize/1024.0**2), 0),audioPath)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()