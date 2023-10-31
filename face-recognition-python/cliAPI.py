import subprocess

def debug(msg):
    print('DEBUG', str(msg))

# Config
known_images_folder = 'kunde1'
unknown_image_file = 'two_people.jpg'

# Detect faces in the picture
face_detection = subprocess.run(['face_detection', '--cpus=-1', unknown_image_file], capture_output=True, text=True)
# Raise an SubprocessError if stderr is not empty
if face_detection.stderr != '':
    raise subprocess.SubprocessError('The face detection process exited with an error: {}'.format(face_detection.stderr))

# Split the output into a string for each detected face
found_faces_text = face_detection.stdout.rstrip().split('\n')
debug(face_detection.stdout)
debug(found_faces_text)

found_faces = []
for item in found_faces_text:
    debug(item)
    # Split the face string into the coordinates and remove the file name
    found_faces.append(item.split(',')[1:])

debug(found_faces)

# Recognize the persons in the pictures
face_recognition = subprocess.run(['face_recognition', '--cpus=-1', known_images_folder, unknown_image_file], capture_output=True, text=True)
if face_recognition.stderr != '':
    # Raise an SubprocessError if stderr is not empty
    raise subprocess.SubprocessError('The face recognition process exited with an error: {}'.format(face_recognition.stderr))

# Split the output into a string for each recognized face
recognized_faces_text = face_recognition.stdout.rstrip().split('\n')
debug(face_recognition.stdout)
debug(recognized_faces_text)

recognized_faces = []
for item in recognized_faces_text:
    debug(item)
    recognized_faces.append(item.split(',')[1])

debug(recognized_faces)