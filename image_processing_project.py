import cv2 as cv
import numpy as np
from abc import *
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image

window = Tk()
window.title("Term Project")
cap_frame = LabelFrame(window, bg="gray")
cap_frame.grid(row=0, column=0, padx=10, pady=2)
frame2 = Label(cap_frame)
frame2.grid(row=0, column=0)

# Callback function for sliders (can be improved later)
def callback_val(x):
    print(x)

class Frame_Grab(ABC):
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def Change_Format(self):
        frame = self.cap.read()[1]
        frame = cv.flip(frame, 1)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        return hsv

class Sliders_Data(ABC):
    def __init__(self):
        self.y = Frame_Grab()
        self.hsv = None
        self.height = 0
        self.width = 0
        self.res = None

    def Set_Sliders_Data(self):
        cv.namedWindow('Term Project')
        self.__positions = [cv.createTrackbar('LH', 'Term Project', 0, 255, callback_val),
                            cv.createTrackbar('UH', 'Term Project', 255, 255, callback_val),
                            cv.createTrackbar('LS', 'Term Project', 0, 255, callback_val),
                            cv.createTrackbar('US', 'Term Project', 255, 255, callback_val),
                            cv.createTrackbar('LV', 'Term Project', 0, 255, callback_val),
                            cv.createTrackbar('UV', 'Term Project', 255, 255, callback_val),
                            cv.createTrackbar('threshold', 'Term Project', 0, 255, callback_val)]

    def Get_Sliders_Data(self):
        self.hsv = self.y.Change_Format()

        l_h = cv.getTrackbarPos('LH', 'Term Project')
        l_s = cv.getTrackbarPos('LS', 'Term Project')
        l_v = cv.getTrackbarPos('LV', 'Term Project')
        u_h = cv.getTrackbarPos('UH', 'Term Project')
        u_s = cv.getTrackbarPos('US', 'Term Project')
        u_v = cv.getTrackbarPos('UV', 'Term Project')
        th_val = cv.getTrackbarPos("threshold", 'Term Project')

        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
        return [l_b, u_b, th_val]

    def Connect_Data(self):
        x = self.Get_Sliders_Data()
        l_b = x[0]
        u_b = x[1]
        mask = cv.inRange(self.hsv, l_b, u_b)
        self.res = cv.bitwise_and(self.hsv, self.hsv, mask=mask)

        self.height, self.width = self.res.shape[:2]

        cv.line(self.res, (170, 0), (170, self.height), (150, 200, 255), 4)
        cv.line(self.res, (340, 0), (340, self.height), (150, 200, 255), 4)

        self.frame = ImageTk.PhotoImage(Image.fromarray(self.res))
        frame2["image"] = self.frame
        window.update()
        
class Region:
    def __init__(self, start_x, end_x,res):
        self.start_x = start_x
        self.end_x = end_x
        self.res = res

class Region:
    def __init__(self, start_x, end_x, res):
        self.start_x = start_x
        self.end_x = end_x
        self.res = res  # Pass the processed image (res) to the Region class

    def Pixel_Calculation(self):
        print(f"Calculating pixels from x={self.start_x} to x={self.end_x}")

        # Crop the image to the specified region
        region_image = self.res[:, self.start_x:self.end_x]  # Crop the region from the image

        # Convert the region to grayscale (if it's a color image)
        region_gray = cv.cvtColor(region_image, cv.COLOR_BGR2GRAY)

        # Example of counting non-zero pixels in the region
        non_zero_pixels = cv.countNonZero(region_gray)
        print(f"Non-zero pixels in the region: {non_zero_pixels}")


class Filter(Frame_Grab, Sliders_Data):
    def __init__(self):
        Sliders_Data.__init__(self)
        Frame_Grab.__init__(self)
        self.thval = 0

    def Filter_Implement(self):
        x = Sliders_Data.Get_Sliders_Data(self)
        self.thval = x[2]
        while True:
            Sliders_Data.Connect_Data(self)
            _, th3 = cv.threshold(self.hsv, self.thval, 255, cv.THRESH_TRUNC)
            cv.imshow("Term Project", th3)

            if cv.waitKey(1) == 27:
                self.cap.release()
                cv.destroyAllWindows()
                break

def main():
    c = Sliders_Data()
    c.Set_Sliders_Data()

    frame1 = Frame(window)
    frame1.place(x=500, height=700, width=400)
    fontx = font.Font(family='Helvetica', size=10, weight='bold')

    # Create Filter object before passing it to the command
    filter_obj = Filter()

    btn1 = Button(frame1, text="Apply\nThreshold", height=3, width=14, fg="white", bg="gray", font=fontx,
                  highlightbackground='#3E4149', relief="groove", command=filter_obj.Filter_Implement)
    btn1.place(x=30, y=100)
    
    btn2 = Button(frame1, text="calculate\n Region1", height=3, width=14, fg="white", bg="gray", font=fontx,
                  highlightbackground='#3E4149', relief="groove", command=lambda: Region(0, 170,c.res).Pixel_Calculation())
    btn2.place(x=30, y=170)
    
    btn3 = Button(frame1, text="calculate\n Region2", height=3, width=14, fg="white", bg="gray", font=fontx,
                  highlightbackground='#3E4149', relief="groove", command=lambda: Region(170, 340,c.res).Pixel_Calculation())
    btn3.place(x=30, y=240)
    
    btn4 = Button(frame1, text="calculate\n Region3", height=3, width=14, fg="white", bg="gray", font=fontx,
                  highlightbackground='#3E4149', relief="groove", command=lambda: Region(340, 640,c.res).Pixel_Calculation())
    btn4.place(x=30, y=310)

    while True:
        c.Connect_Data()

    window.mainloop()

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
