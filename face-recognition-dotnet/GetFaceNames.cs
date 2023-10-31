using System;
using FaceRecognitionDotNet;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.IO;

namespace faces_cs
{
    class Config
    {
        public static string unknown_image_file = "two_people.jpg";
        public static string custumer_id = "1234";
    }
    class GetFaceNames
    {   
        static void Main3(string[] args) {
            FaceRecognition.InternalEncoding = System.Text.Encoding.GetEncoding("utf-8");
            FaceRecognition face_recognition = FaceRecognition.Create("models");

            var known_face_encodings = JsonSerializer.Deserialize<FaceData[]>(File.ReadAllText($"encodings/{Config.custumer_id}.json"));
            var known_names = known_face_encodings.Select(x => x.Name).ToList();
            var known_faces = known_face_encodings.Select(x => FaceRecognition.LoadFaceEncoding(x.Encoding)).ToList();

            Image unknown_image = FaceRecognition.LoadImageFile(Config.unknown_image_file);
            IEnumerable<Location> face_locations = face_recognition.FaceLocations(unknown_image);
            IEnumerable<FaceEncoding> face_encodings = face_recognition.FaceEncodings(unknown_image, knownFaceLocation: face_locations).ToList();

            List<string> face_names = new();
            foreach(var face_encoding in face_encodings) {
                string name = "Unknown";
                if(known_faces.Count() != 0) {
                    List<bool> matches = FaceRecognition.CompareFaces(known_faces, face_encoding).ToList();
                    List<double> face_distances = FaceRecognition.FaceDistances(known_faces, face_encoding).ToList();
                    double best_match = face_distances.Min();
                    int best_match_index = face_distances.IndexOf(best_match);
                    if(matches[best_match_index]) {
                        name = known_names[best_match_index];
                    }
                }

                face_names.Add(name);
            }

            List<Dictionary<string, dynamic>> output = new();

            for (int i = 0; i < face_names.ToArray().Length; i++)
            {
                Dictionary<string, dynamic> temp = new();
                temp.Add("Name", face_names[i]);
                temp.Add("Location", face_locations.ToArray()[i]);
                output.Add(temp);
            }

            Console.WriteLine(JsonSerializer.Serialize(output));

        }
    }
}
