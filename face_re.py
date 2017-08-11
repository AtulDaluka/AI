import face_recognition
import cv2
import sys
import os
import pandas as pd

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
path = os.getcwd()
# outpath = os.path.join(path,'aip.avi')
# print(os.path.join(path,'ai2.mp4'))
out = cv2.VideoWriter(os.path.join(path,'ai6.mp4') , fourcc, 1.0, (848,480))
# Load a sample picture and learn how to recognize it.
# imageFolder = "/home/atul/Desktop/"


# obama_image = face_recognition.load_image_file("6.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# dog = face_recognition.load_image_file("3.jpg")
# dog_face_encoding = face_recognition.face_encodings(dog)[0]
# print(dog_face_encoding)
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
i=0
nameArr=[]
while(cap.isOpened()):
    i=i+1
    if((i%10)==0):
    # Grab a single frame of video
        ret, frame = cap.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(small_frame)
            
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            face_names = []
            path = os.getcwd()
            pathN = os.path.join(path,'Images')
            folders = os.listdir(pathN)
            for face_encoding in face_encodings:
                flag=False
                for fileName in folders:
                    files = os.listdir(os.path.join(pathN,fileName))
                    arr=[]
                    for everyFile in files:
                        #print(everyFile)
                        eImage = face_recognition.load_image_file(os.path.join(os.path.join(pathN,fileName),everyFile))
                        # print((os.path.join(os.path.join(pathN,fileName),everyFile)))
                        eImageEncoding = face_recognition.face_encodings(eImage)[0]

                    
                    # See if the face is a match for the known face(s)
                        match = face_recognition.compare_faces([eImageEncoding], face_encoding)
                        arr.append(match[0])
                        # match2 = face_recognition.compare_faces([dog_face_encoding], face_encoding)
                    # name = "Unknown"
                    # print(arr)
                    if (sum(arr)>=1):
                        name = fileName
                        flag=True
                    else:
                        pass
                if(flag==False):
                    name = "unknown"

                        # if match2[0]:
                        #     name = "Dog"
                            # print(face_encoding)                                                           
                face_names.append(name)
        # print(face_names)
        process_this_frame = not process_this_frame
        nameArr.append(list(set(face_names)))
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        out.write(frame)
        print(frame.shape)
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        c = cv2.waitKey(0)
        if 'q' == chr(c & 255):
            break
        
        # if cv2.waitKey(1) and 0xFF == ord('q'):
        #     break
print(nameArr)
df = pd.DataFrame(nameArr)
df.to_csv('attendence.csv',index = False, header = False)
# Release handle to the webcam
cap.release()
out.release()

cv2.destroyAllWindows()