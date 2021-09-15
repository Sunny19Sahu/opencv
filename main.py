from flask import Flask, render_template, Response
import cv2
import time
import winsound

app = Flask(__name__)

cascPath = 'haarcascade_frontalface_dataset.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

t=30

def camera_stream():
     # Capture frame-by-frame
    global t
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(t)
        if(t<=0):
            cv2.putText(frame, "Log off System", (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
            for x in range(0,10):
                winsound.Beep(1000, 1000)
                time.sleep(0.5)
            t=30
        else:
            #print(timer, end="\r")
            cv2.putText(frame, timer, (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        time.sleep(1)
        t=t-1

    # Display the resulting frame in browser
    return cv2.imencode('.jpg', frame)[1].tobytes()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen_frame():
    while True:
        frame = camera_stream()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True)
