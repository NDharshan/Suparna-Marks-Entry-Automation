import numpy as np
import cv2
import imutils
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pytesseract
from PIL import Image

def image_processing():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    Tk().withdraw()
    filename = askopenfilename(
        filetypes=[("Jpg files", r"C:\Users\DELL\Desktop\imgs\DocScanner 27 May 2022 8-37 pm_page-0002.jpg")])
    image = cv2.imread(filename)
    image = imutils.resize(image, width=500)
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    gray_scaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_scaled = cv2.bilateralFilter(gray_scaled, 15, 20, 20)
    edges = cv2.Canny(gray_scaled, 170, 200)
    # half = cv2.resize(edges, (700, 700), fx = 0.1, fy = 0.1)
    # a=half[500:540,490:590]
    contours, heirarchy = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1 = image.copy()
    cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
    cv2.imshow("All of the contours", img1)
    cv2.waitKey(0)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    Number_Plate_Contour = 0
    for current_contour in contours:
        perimeter = cv2.arcLength(current_contour, True)
        approx = cv2.approxPolyDP(current_contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            Number_Plate_Contour = approx
            break
    mask = np.zeros(gray_scaled.shape, np.uint8)
    new_image1 = cv2.drawContours(mask, [Number_Plate_Contour], 0, 255, -1, )
    new_image1 = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("Number is", new_image1)
    cv2.waitKey(0)
    gray_scaled1 = cv2.cvtColor(new_image1, cv2.COLOR_BGR2GRAY)
    ret, processed_img = cv2.threshold(np.array(gray_scaled1), 125, 255, cv2.THRESH_BINARY)
    cv2.imshow("Number is", processed_img)
    cv2.waitKey(0)
    text = pytesseract.image_to_string(processed_img)
    print("Number is :", text)
    cv2.waitKey(0)



def firebase_work():
    import pyrebase
    firebaseConfig = {
        'apiKey': "AIzaSyArKFFDqMwXZR1QCCJvBmcOUn0ajIISs3Y",
        'authDomain': "suparna-7dd6e.firebaseapp.com",
        'databaseURL': "https://suparna-7dd6e-default-rtdb.firebaseio.com",
        'projectId': "suparna-7dd6e",
        'storageBucket': "suparna-7dd6e.appspot.com",
        'messagingSenderId': "292555253504",
        'appId': "1:292555253504:web:63ad4c6273dffd7f6eb5e5"
    };

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    auth = firebase.auth()
    storage = firebase.storage()

    # authentication
    # login
    def login_firebase():
        print("Login")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        try:
            auth.sign_in_with_email_and_password(email, password)
            print("Signed-in successfully")
        except:
            print("Invalid user or password, Try again")

    # signup
    def signup_firebase():
        print("Sign Up")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        confirmpass = input("Confirm your password: ")
        if password == confirmpass:
            try:
                auth.create_user_with_email_and_password(email, password)
                print("Created id %s !" % (email))
            except:
                print("User exists")

    # Storage
    def storage_firebase(i):
        def upload_firebase():
            filename = input("Enter file name: ")
            cloudfilename = input("Enter file name to store in cloud: ")
            storage.child(cloudfilename).put(filename)

        def download_firebase():
            filenm = input("Enter file name: ")
            cloudfilename = rf"C:\Users\DELL\Desktop\imgs\{filenm}"
            storage.child(filenm).download("", "downloaded.txt")
            return cloudfilename
            # upload_firebase()

        if i == 1:
            upload_firebase()
        else:
            return download_firebase()
    storage_firebase(1)

image_processing()