from flask import Flask, redirect, render_template, url_for, request
import subprocess, shutil, threading

app = Flask(__name__)

counter = 0


@app.route('/video/<int:count>')
def player(count):
    lock = threading.Lock()
    lock.acquire()
    shutil.copy("static/out/file.m3u8", f"static/out/{count}.m3u8")
    lock.release()
    rtmp_url = f"rtmp://localhost:1936/stream/{count}"
    command = ['ffmpeg',
               '-y',
               '-re',
               '-i', 'static/out/file.m3u8',

               '-f', 'flv',
               rtmp_url
               ]

    subprocess.Popen(command, shell=True)
    return render_template('player.html', value=count)


@app.route('/', methods=['GET', 'POST'])
def main():  # put application's code here
    if request.method == "POST":
        global counter
        counter += 1
        return redirect(url_for("player", count=counter))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5001)

# get id of video and return /video/<ID>/counter
# We need to a html file to show video
