# FaceRecognition

This script can detect and recognize faces in pictures. It is written in C# and dotnet using [FaceRecognitionDotNet](https://github.com/takuya-takeuchi/FaceRecognitionDotNet).

## Usage

### Input data

We have the picture [two_people.jpg](https://github.com/bennetrr/FaceRecognition/blob/main/two_people.jpg) which shows Biden and Obama. The directory [encodings](https://github.com/bennetrr/FaceRecognition/blob/main/encodings) contains json files (e.g. the 1234.json file). The json file consist of multiple elements with a `Name` and an `Encoding` property. `Encoding` is a list of doubles that describe the face.

### Getting the encodings

You can simply getting the encodings for a person on an image file by calling `main.getFaceNames(String encodings_file, String unknown_image_file)`. For testing, I programmed a main method into the class that runs this command and converts it to json so you can paste it directly into the json file.

If you want to get the encodings of an unkown face, you simply have to call `getFaceNames` with an encodings file and with the picture. The method returns the name (in this case `null`), the location of the face and the encodings. Next you can copy the encodings to the encodings file and add the name of the person. Now you defined a new person and the script can recognize it now.

### Getting the name and the location of a person

The same way you get the encoding of a face you can get the name of a face. The only thing is that the face was previously saved in the encodings file. You can use the output to display a box around the face and show the name of the person or whatever.
