import cv2
import sys

def help(argv):
    print("\nThis program demonstrates the use of cv2.CascadeClassifier class to detect objects (Face + eyes). You can use Haar or LBP features.\n"
            "This classifier can recognize many kinds of rigid objects, once the appropriate classifier is trained.\n"
            "It's most known use is for faces.\n"
            "Usage:\n"
            f"{argv[0]}"
            "   [--cascade=<cascade_path> this is the primary trained classifier such as frontal face]\n"
            "   [--nested-cascade[=nested_cascade_path this an optional secondary classifier such as eyes]]\n"
            "   [--scale=<image scale greater or equal to 1, try 1.3 for example>]\n"
            "   [--try-flip]\n"
            "   [filename|camera_index]\n\n"
            "example:\n"
            f"{argv[0]}"
            " --cascade=\"data/haarcascades/haarcascade_frontalface_alt.xml\" --nested-cascade=\"data/haarcascades/haarcascade_eye_tree_eyeglasses.xml\" --scale=1.3\n\n"
            "During execution:\n\tHit any key to quit.\n"
            f"\tUsing OpenCV version {cv2.__version__}\n")

def detectAndDraw(img, cascade, nestedCascade, scale, tryflip):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = cascade.detectMultiScale(gray, scaleFactor=scale, minNeighbors=3, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        center = (x + w//2, y + h//2)
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if nestedCascade.empty():
            continue
        roi = gray[y:y+h, x:x+w]
        nestedObjects = nestedCascade.detectMultiScale(roi, scaleFactor=scale, minNeighbors=3, minSize=(20, 20), flags=cv2.CASCADE_SCALE_IMAGE)
        for (nx, ny, nw, nh) in nestedObjects:
            center = (x + nx + nw//2, y + ny + nh//2)
            img = cv2.rectangle(img, (x+nx, y+ny), (x+nx+nw, y+ny+nh), (255, 0, 0), 2)
    cv2.imshow("Face Detection", img)

cascadeName = "haarcascade_frontalface_alt.xml"
nestedCascadeName = "haarcascade_eye_tree_eyeglasses.xml"
scale = 1.3

if __name__ == '__main__':
    help(sys.argv)
    cascade = cv2.CascadeClassifier()
    nestedCascade = cv2.CascadeClassifier()
    if not cascade.load(cv2.samples.findFile(cascadeName)):
        print('--(!)Error loading face cascade')
        exit(0)
    if not nestedCascade.load(cv2.samples.findFile(nestedCascadeName)):
        print('--(!)Error loading eyes cascade')
        exit(0)
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print('--(!)Error opening camera')
        exit(0)
    while True:
        ret, frame = camera.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        detectAndDraw(frame, cascade, nestedCascade, scale, False)
        if cv2.waitKey(10) == 27:
            break