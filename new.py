import Tkinter as tk
import tkFileDialog
from tkFileDialog import *
import tkMessageBox
import cv2
import face_recognition
import sys
import os
import pandas as pd
from datetime import datetime

LARGE_FONT = ("Verdana", 12)

class first_class(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Automated Attendence System")
        container = tk.Frame(self)

        container.pack(side="top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

# def upload_image():
#     img = ImageTk.PhotoImage(Image.open(self.filename))


# def browse_image():
#     from tkFileDialog import askopenfilename

#     Tk().withdraw() 
#     self.filename = askopenfilename()


    



class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Upload Image for Training", font = (None, 15)).grid(row = 1, sticky = "n")

        label1 = tk.Label(self, text="Name of the person", font = LARGE_FONT).grid(row = 3,padx=10, pady=10)
        
        #textBox = tk.Text(self, height=1, width=15, bd = 4).grid(row = 3, column = 1)
        v = tk.StringVar()

        e1 = tk.Entry(self,textvariable=v, bd =4).grid(row = 3, column = 1,padx=10, pady=10)
        #v.set("a default value")
        
        filename = []

        def browsefunc():
            
            self.filename = tkFileDialog.askopenfilenames(filetypes = (("JPG image", "*.jpg"), ("PNG Image", "*.png")))
            print(self.filename[0])

        def retrieve_input():
            inputValue  = v.get()
              # Path where  we want to save images
            newpath = r'/home/puneet/Opened.ai/Images'
            newpath = newpath + '/'
            newpath = newpath + inputValue
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            for i in range(0,len(self.filename)):
                img = cv2.imread(self.filename[i], 1)
                cv2.imwrite(str(newpath) + '/' + inputValue + str(i) + '.jpg',img)
                

            print('Images saved!')
            #print(self.filename[1])
            #print(inputValue)

        button1= tk.Button(self, text="Browse", command=browsefunc).grid(row = 3, column = 2,padx=10, pady=10)
        #button1.pack(side = tk.LEFT)    

        button2= tk.Button(self, text="Submit", command=lambda: retrieve_input()).grid(row = 3, column = 3,padx=10, pady=10)
        #button2.pack(side = tk.LEFT)

        label = tk.Label(self, text = "Video Processing", font = (None, 15)).grid(row = 7, padx=20, pady=20)

        # label2 = tk.Label(self, text="Upload Existing Video", font = LARGE_FONT).grid(row = 11)

        self.video_path = None   
        videoname = []
        def upload_video():    
            videoname = tkFileDialog.askopenfilenames(filetypes = (("MP4 Video", "*.mp4"), ("AVI Video", "*.avi")))
            self.video_path = videoname[0]
            print('Video Uploaded Successfully!')

        # button3 = tk.Button(self, text="Upload Video", command=upload_video).grid(row = 11, column = 1)
#
        def run_algorithm():
            cap = cv2.VideoCapture(self.video_path)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            path = os.getcwd()
            # outpath = os.path.join(path,'aip.avi')
            # print(os.path.join(path,'ai2.mp4'))
            out = cv2.VideoWriter(os.path.join(path,'ai7.mp4') , fourcc, 1.0, (848,480))
            # Load a sample picture and learn how to recognize it.
            # imageFolder = "/home/atul/Desktop/"


            # obama_image = face_recognition.load_image_file("6.jpg")
            # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

            # dog = face_recognition.load_image_file("3.jpg")
            # dog_face_encoding = face_recognition.face_encodings(dog)[0]
            # print(dog_face_encoding)
            # obama_image = face_recognition.load_image_file("1.jpg")
            # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
            # Initialize some variables
            face_locations = []
            face_encodings = []
            face_names = []
            process_this_frame = True
            i=0
            self.nameArr=[]
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
                            print(name)                                                       
                            face_names.append(name)
                    # print(face_names)
                    process_this_frame = not process_this_frame
                    self.nameArr.append(list(set(face_names)))
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
                    # print(frame.shape)
                    cv2.imshow('Video', frame)

                    # Hit 'q' on the keyboard to quit!
                    # Hit 'q' on the keyboard to quit!
                    key = cv2.waitKey(20)
                    if key == 27: # exit on ESC
                        break
                    # c = cv2.waitKey(0)
                    # if 'q' == chr(c & 255):
                    #     QuitProgram()
                        # cap.release()
                        # out.release()

                        # cv2.destroyAllWindows()
                        # break
            print(self.nameArr)
                        # Release handle to the webcam
            cap.release()
            out.release()

            cv2.destroyAllWindows()
            print('Algorithm implemented Successfully!')


        # button4 = tk.Button(self, text="Run Algorithm", command=run_algorithm).grid(row = 11, column = 2)

        #print(self.video_path)
        
        

        # label3 = tk.Label(self, text="OR", font = LARGE_FONT).grid(row = 13, column = 1, padx=10, pady=10)

        label4 = tk.Label(self, text="Capture Live Video", font = LARGE_FONT).grid(row = 15)

        def live_feed():
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            path = os.getcwd()
            # outpath = os.path.join(path,'aip.avi')
            # print(os.path.join(path,'ai2.mp4'))
            out = cv2.VideoWriter(os.path.join(path,'output_video.mp4') , fourcc, 1.0, (848,480))
            # Load a sample picture and learn how to recognize it.
            # imageFolder = "/home/atul/Desktop/"


            # obama_image = face_recognition.load_image_file("6.jpg")
            # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

            # dog = face_recognition.load_image_file("3.jpg")
            # dog_face_encoding = face_recognition.face_encodings(dog)[0]
            # print(dog_face_encoding)
            # obama_image = face_recognition.load_image_file("1.jpg")
            # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
            # Initialize some variables
            face_locations = []
            face_encodings = []
            face_names = []
            process_this_frame = True
            i=0
            self.nameArr=[]
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
                            print("Student Name: ", name)
                            print("Student Entered at:", str(datetime.now()))
                            face_names.append(name)
                    # print(face_names)
                    process_this_frame = not process_this_frame
                    self.nameArr.append(list(set(face_names)))
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
                    # print(frame.shape)
                    cv2.imshow('Video', frame)

                    # Hit 'q' on the keyboard to quit!
                    # Hit 'q' on the keyboard to quit!
                    key = cv2.waitKey(20)
                    if key == 27: # exit on ESC
                        break
                    # c = cv2.waitKey(0)
                    # if 'q' == chr(c & 255):
                    #     QuitProgram()
                        # cap.release()
                        # out.release()

                        # cv2.destroyAllWindows()
                        # break
            print(self.nameArr)
                        # Release handle to the webcam
            cap.release()
            out.release()

            cv2.destroyAllWindows()
            
        button6 = tk.Button(self, text="Live Feed", command=live_feed).grid(row = 15, column = 1)

        # label5 = tk.Label(self, text = "Results", font=(None, 15)).grid(row = 20,padx=10, pady=10)

        def show_video():
            cap = cv2.VideoCapture(self.video_path)
            count = 0
            print(cap.isOpened())
            while cap.isOpened():
                ret,frame = cap.read()
                count = count + 1
                cv2.imshow('Uploaded Video',frame)
                #cv2.imwrite("frame%d.jpg" % count, frame)
                
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cap.destroyAllWindows()
            print('Hello')

        # button5 = tk.Button(self, text="Show Video", command=show_video).grid(row = 20, column = 1)
        # def download_csv():
        #     df = pd.DataFrame(self.nameArr)
        #     df.to_csv('attendence.csv',index = False, header = False)
        #     print('csv file downloaded!')

        # button7 = tk.Button(self, text="Download csv", command=download_csv).grid(row = 20, column = 1,padx=10, pady=10)
        

app = first_class()
app.mainloop()

