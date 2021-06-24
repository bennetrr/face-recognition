using System;
using FaceRecognitionDotNet;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.IO;

namespace faces_cs
{
    class SetFaceNames
    {
        static string locations_to_encode_text = "[{\"Name\":\"Unknown\", \"Location\":{\"Bottom\":242, \"Left\":778, \"Right\":964, \"Top\":57}},{ \"Name\":\"Unknown\",\"Location\":{ \"Bottom\":202,\"Left\":253,\"Right\":408,\"Top\":47} }]";
        
        static void Main2(string[] args)
        {
            FaceRecognition.InternalEncoding = System.Text.Encoding.GetEncoding("utf-8");
            FaceRecognition face_recognition = FaceRecognition.Create("models");

            var locations_to_encode = JsonSerializer.Deserialize<FaceData[]>(locations_to_encode_text);
            var known_locations = locations_to_encode.Select(x => x.Location).ToList();
            var known_names = locations_to_encode.Select(x => x.Name).ToList();

            Image unknown_image = FaceRecognition.LoadImageFile(Config.unknown_image_file);
            
            var locations = known_locations.Select(x => new Location(x.Left, x.Top, x.Left, x.Bottom)).ToList();            
            var face_encodings = face_recognition.FaceEncodings(unknown_image, knownFaceLocation: locations);
            
            List<Dictionary<string, dynamic>> output = new();

            for (int i = 0; i < face_encodings.ToArray().Length; i++) {
                Dictionary<string, dynamic> temp = new();
                temp.Add("Name", known_names[i]);
                temp.Add("Encoding", face_encodings.ToArray()[i].GetRawEncoding());
                output.Add(temp);                
            }

            Console.WriteLine(JsonSerializer.Serialize(output));
        }
    } 
}
