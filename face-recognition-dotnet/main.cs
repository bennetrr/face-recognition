using System;
using FaceRecognitionDotNet;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.IO;

namespace faces_cs {
    class LocationData {
        public LocationData() {}
        public LocationData(int top, int left, int bottom, int right, double confidence = 0) {
            Top = top;
            Left = left;
            Bottom = bottom;
            Right = right;
            Confidence = confidence;
        }

        public Location toLocation() {return new Location(Left, Top, Right, Bottom, Confidence);}
        public int Top { get; set; }
        public int Left { get; set; }
        public int Bottom { get; set; }
        public int Right { get; set; }
        public double Confidence { get; set; }
    }

    class FaceData {
        public FaceData() {}
        public FaceData(Location loc = null, string name = null, double[] encoding = null) {
            Name = name;
            Encoding = encoding;
            Location = new LocationData(loc.Top, loc.Left, loc.Bottom, loc.Right, loc.Confidence);
        }
        public FaceData(LocationData loc = null, string name = null, double[] encoding = null) {
            Name = name;
            Encoding = encoding;
            Location = loc;
        }

        public string Name { get; set; }
        public double[] Encoding { get; set; }
        public LocationData Location { get; set; }
    }

    class main {
        static List<FaceData> getFaceNames(String encodings_path, String unknown_image_file) {
            // setting up FaceRegocnitionDotNet
            FaceRecognition.InternalEncoding = System.Text.Encoding.GetEncoding("utf-8");
            FaceRecognition face_recognition = FaceRecognition.Create("models");

            // get known faces
            var known_faces = JsonSerializer.Deserialize<FaceData[]>(File.ReadAllText(encodings_path));

            // load faces in unknown image
            Image unknown_image = FaceRecognition.LoadImageFile(unknown_image_file);
            List<FaceData> unknown_faces = face_recognition.FaceLocations(unknown_image).Select(x => new FaceData(x)).ToList();

            foreach (var unknown_face in unknown_faces) {
                // load face encoding of the unknown faces
                unknown_face.Encoding = face_recognition.FaceEncodings(unknown_image, new List<Location>{unknown_face.Location.toLocation()}).ToArray().First().GetRawEncoding();
                foreach (var known_face in known_faces) {
                    // compare the faces
                    var match = FaceRecognition.CompareFace(FaceRecognition.LoadFaceEncoding(known_face.Encoding), FaceRecognition.LoadFaceEncoding(unknown_face.Encoding));
                    // because this version of the API return true or false and not a numer as in python, check if this is a match
                    if(match) {
                        // if yes, save the name and go on with the next face
                        unknown_face.Name = known_face.Name;
                        break;
                    }
                }
            }
            return(unknown_faces);
        }

        public static void Main(string[] args)
        {
            Console.WriteLine(JsonSerializer.Serialize(getFaceNames("encodings/1234.json", "two_people.jpg")));
        }
    }
}