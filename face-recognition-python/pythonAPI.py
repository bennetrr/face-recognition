import os
import face_recognition
import numpy
from PIL import Image, ImageDraw, ImageFont

def debug(*msgs):
    temp = '[DEBUG] '
    for msg in msgs:
        temp = temp + str(msg) + ' '
    print(temp)

# Config
#known_images_folder = 'kunde1'
unknown_image_file = 'two_people copy 2.jpg'

known_images = [[ 0.00212634,  0.18151696,  0.08942953, -0.02890662, -0.13226929,
        0.04053921, -0.03351216, -0.07746185,  0.05412482, -0.05690686,
        0.24183109, -0.05402808, -0.25743544, -0.05157363,  0.06138313,
        0.12605764, -0.14946274, -0.06552805, -0.20102572, -0.06235627,
       -0.01103389, -0.0410016 ,  0.02593715, -0.07272571, -0.20662072,
       -0.23533899, -0.04712093, -0.1022827 , -0.02789485, -0.16243912,
        0.07824211, -0.03084383, -0.14441712, -0.05164247, -0.04710121,
       -0.0298584 , -0.01722826, -0.05847342,  0.13154459,  0.0262634 ,
       -0.17892288,  0.13025905,  0.0073351 ,  0.21587208,  0.29474819,
       -0.00523595,  0.04717013, -0.08853557,  0.13626243, -0.24181861,
        0.05437332,  0.03498961,  0.16807069,  0.05769813,  0.14244418,
       -0.0731723 ,  0.02392231,  0.18972901, -0.200625  ,  0.03737672,
        0.05043876, -0.05482149,  0.03411502, -0.04349234,  0.12301472,
        0.11024218, -0.009777  , -0.09036201,  0.19369094, -0.09519793,
       -0.11277228,  0.03078757, -0.06616243, -0.12772179, -0.33526269,
        0.00107876,  0.27036449,  0.1360216 , -0.29611111, -0.07562292,
       -0.04549194,  0.00518049,  0.03369439,  0.00834185, -0.03430053,
       -0.13692579, -0.05488759, -0.01437558,  0.24373633, -0.10935871,
        0.00704367,  0.22373417,  0.04802165, -0.14844172,  0.05571177,
       -0.03593142, -0.11785192, -0.01510648, -0.1176923 , -0.05191775,
       -0.0226258 , -0.1587825 , -0.03008005,  0.0665701 , -0.26241189,
        0.16402586, -0.01417352, -0.07986997, -0.05631709, -0.04092155,
        0.01244701,  0.06576453,  0.22907118, -0.24998775,  0.20107335,
        0.22818169, -0.05759405,  0.07731683,  0.01206532,  0.06270912,
       -0.03904255,  0.0357298 , -0.08620857, -0.13285436, -0.00430028,
       -0.02123452,  0.0096128 ,  0.06677761], [-0.09143443,  0.13086104,  0.01314377, -0.05788449,  0.0162896 ,
        0.0004133 , -0.08469845, -0.09900515,  0.17989591, -0.10539673,
        0.24560221,  0.08059315, -0.21611468, -0.13486724,  0.04742456,
        0.12056779, -0.16367504, -0.07826024, -0.11224693, -0.10610127,
        0.03652949,  0.00634991,  0.1053369 ,  0.04300563, -0.12117682,
       -0.33629149, -0.06974638, -0.18218069, -0.00158561, -0.11208323,
       -0.09656747, -0.02059189, -0.18194009, -0.10914117,  0.02073216,
       -0.02022123,  0.00240959, -0.00374011,  0.20474009,  0.02820575,
       -0.11632425,  0.09632836,  0.01547989,  0.21318351,  0.28629941,
        0.07692295, -0.01180617, -0.09913057,  0.10386179, -0.21633521,
        0.0727405 ,  0.14290071,  0.08237928,  0.04238795,  0.09769623,
       -0.18852286,  0.00360183,  0.08834422, -0.14143486,  0.00837212,
        0.00788715, -0.08102694, -0.04035502,  0.03879581,  0.20594744,
        0.09965958, -0.12292912, -0.05094444,  0.13211262, -0.02900145,
        0.02445139,  0.02434405, -0.1843133 , -0.20063356, -0.22774032,
        0.09293826,  0.37345201,  0.19359812, -0.20881185,  0.01955769,
       -0.19599997,  0.02415313,  0.0610562 ,  0.00819605, -0.07174445,
       -0.13538508, -0.04118636,  0.05282187,  0.08226584,  0.0320852 ,
       -0.04098896,  0.21506967, -0.03382798,  0.06236767,  0.01853625,
        0.05682234, -0.15838754, -0.03170493, -0.16015242, -0.06845069,
        0.01404161, -0.04203653,  0.03085325,  0.14781637, -0.23243298,
        0.05921925,  0.00418686, -0.04666767,  0.02229128,  0.07022517,
       -0.02721729, -0.03373834,  0.05814214, -0.23816797,  0.24889059,
        0.23403467,  0.02495457,  0.17327933,  0.07225875,  0.03394284,
       -0.01637946, -0.02267806, -0.18229848, -0.06459417,  0.06046801,
        0.07552323,  0.08523151,  0.00671962]]
known_names = ['Joe Biden', 'Barack Obama']

# List every file in known_images_folder
# for file in os.listdir(known_images_folder):
#     debug(file, type(file))
#     # Check extensions
#     if file.endswith(('.jpg','.png')):
#         # Load file
#         known_images.append(face_recognition.face_encodings(face_recognition.load_image_file(os.path.join(known_images_folder,file)))[0])
#         # Put file name without extension in known_names
#         known_names.append(os.path.splitext(file)[0])

debug('known names:', len(known_names), known_names)
debug('known images:', len(known_images))
debug('unknown image:', unknown_image_file)

# Load unknown image
unknown_image = face_recognition.load_image_file(unknown_image_file)

# Some variables
face_locations = []
face_encodings = []
face_names = []

# Find faces in the picture
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

debug('Found ', len(face_locations), 'faces in the picture')

for face_encoding in face_encodings:
    # Look for matches
    matches = face_recognition.compare_faces(known_images, face_encoding)
    name = 'Unknown'

    # Use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_images, face_encoding)
    best_match_index = numpy.argmin(face_distances)
    if matches[best_match_index]:
        name = known_names[best_match_index]

    face_names.append(name)
    debug('Found person:', name, face_encoding)

# Open the picture to write person data in it
img = Image.open(unknown_image_file)
imgdraw = ImageDraw.Draw(img)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 25)

for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Draw recangles for every found person
    imgdraw.rectangle((left, top, right, bottom), outline='red', width=5)
    imgdraw.text((left, bottom), name, font=font, stroke_width=1, stroke_fill='black', fill='white')

# Save the edited picture
img.save(unknown_image_file)