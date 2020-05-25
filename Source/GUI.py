import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
from matplotlib import style
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk
import tkinter as tk
import matplotlib
from decimal import Decimal
matplotlib.use("TkAgg")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Reset Graphs", command=reset_graphs)

        button1.pack()

        button2 = ttk.Button(self, text="Pause/Start Graphs",
                             command=pause_start_graphs)

        button2.pack()

        button3 = ttk.Button(self, text="Toggle Fan Control",
                             command=toggleFanControl)
                            
        button3.pack()

        button4 = ttk.Button(self, text="Turn Fan On", command=turnOnFan)

        button4.pack()

        button5 = ttk.Button(self, text="Turn Fan Off", command=turnOffFan)

        button5.pack()
        
        button6 = ttk.Button(self, text="Toggle Motor Control",
                             command=toggleFanControl)
                            
        button6.pack()
        
        button7 = ttk.Button(self, text="Turn Motor On", command=turnOffFan)

        button7.pack()
        
        button8 = ttk.Button(self, text="Turn Motor Off", command=turnOffFan)

        button8.pack()

        button9 = ttk.Button(self, text="Exit Program", command=quitProgram)

        button9.pack()

        canvas = FigureCanvasTkAgg(fig, self)

        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)

        toolbar.update()

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class graphApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        root = tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Extensible Sensor Network")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=5)
        container.grid_columnconfigure(0, weight=5)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]

        frame.tkraise()


# Data fields needed for plotting live data
entryCount = 0
pause_start = 0
temperatureGraph_x = []
temperatureGraph_y = []
humidityGraph_x = []
humidityGraph_y = []

# Set up our plots
fig = plt.figure(figsize=(6, 4))
fig.suptitle("Extensible Sensor Network", fontsize=16)
sub1 = plt.subplot(2, 2, 1)
sub2 = plt.subplot(2, 2, 2)
#sub3 = plt.subplot(2, 2, 3)
#sub4 = plt.subplot(2, 2, 4)
sub1.set_title("Temperature vs. Entries")
sub1.set_ylabel("Temperature (Celcius)")
sub1.set_xlabel("Entries")
sub2.set_title("Humidity vs. Entries")
sub2.set_ylabel("Humidity (Percentage)")
sub2.set_xlabel("Entries")

# Plot once to set labels
sub1.plot(temperatureGraph_x, temperatureGraph_y,
          color='blue', label='Temperature')
sub1.legend(loc='upper right')
sub1.set_xlim(left=max(0, entryCount - 50), right=entryCount + 25)

sub2.plot(humidityGraph_x, humidityGraph_y, color='red', label='Humidity')
sub2.legend(loc='upper right')
sub2.set_xlim(left=max(0, entryCount - 50), right=entryCount + 25)

# Animation function to update plot
def animate(i):
    global pause_start
    global time
    global temperatureGraph_x
    global temperatureGraph_y
    global humidityGraph_x
    global humidityGraph_y

    # Simple variable check to see if we pause graphing or not
    if (pause_start == 0):

        print("temp arrays: ")
        print(temperatureGraph_x)
        print(temperatureGraph_y)

        sub1.plot(temperatureGraph_x, temperatureGraph_y, color='blue')
        sub1.set_xlim(left=max(0, entryCount - 50), right=entryCount + 25)

        sub2.plot(humidityGraph_x, humidityGraph_y, color='red')
        sub2.set_xlim(left=max(0, entryCount - 50), right=entryCount + 25)


# Reset Graph Data
def reset_graphs():
    global sub1
    global sub2

    sub1.clear()
    sub2.clear()
    sub1.set_title("Temperature vs. Entries")
    sub1.set_ylabel("Temperature (Celcius)")
    sub1.set_xlabel("Entries")
    sub2.set_title("Humidity vs. Entries")
    sub2.set_ylabel("Humidity (Percentage)")
    sub2.set_xlabel("Entries")

# Function to start or pause graphs
def pause_start_graphs():
    global pause_start
    if (pause_start == 1):
        pause_start = 0
    elif (pause_start == 0):
        pause_start = 1


def HumidityTempUpdate(self, params, packet):
    global entryCount
    global temperatureGraph_x
    global temperatureGraph_y
    global humidityGraph_x
    global humidityGraph_y

    payloadDict = json.loads(packet.payload)

    Temp = Decimal(payloadDict["temperature"])
    Temp = round(Temp, 2)
    Humidity = Decimal(payloadDict["humidity"])
    Humidity = round(Humidity, 2)

    # Increment total number of entries stored in program
    entryCount = entryCount + 1

    # Push values to arrays for plotting
    temperatureGraph_y.append(Temp)
    temperatureGraph_x.append(entryCount)
    humidityGraph_y.append(Humidity)
    humidityGraph_x.append(entryCount)


def toggleFanControl():
    myMQTTClient.publish("RyanPi/ryan_pi/GUItoggleFanControl",
                         "payload doesn't matter", 0)

def toggleMotorControl():
    print("Not done yet")

def turnOnFan():
    myMQTTClient.publish("RyanPi/ryan_pi/GUIturnOnFan", "payload doesn't matter", 0)


def turnOffFan():
    myMQTTClient.publish("RyanPi/ryan_pi/GUIturnOffFan", "payload doesn't matter", 0)

def turnMotorOn():
    print("Not done yet")

def turnMotorOff(): 
    print("Not done yet")

def quitProgram():
    exit()


if __name__ == "__main__":
    try:

        # MQTT setup
        myMQTTClient = AWSIoTMQTTClient("NoName")
        myMQTTClient.configureEndpoint(
            "a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)
        myMQTTClient.configureCredentials("/home/ryan/Certificates/RootCA.crt",
                                          "/home/ryan/Certificates/78ac4c9e75-private.pem.key", "/home/ryan/Certificates/78ac4c9e75-certificate.pem.crt")
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)
        myMQTTClient.configureConnectDisconnectTimeout(10)
        myMQTTClient.configureMQTTOperationTimeout(5)
        myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myMQTTClient.connect()
        myMQTTClient.subscribe("RyanPi/ryan_pi/data", 1, HumidityTempUpdate)

        app = graphApp()
        app.minsize(1000, 800)
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        app.mainloop()

    except (KeyboardInterrupt):
        print("Exiting")
