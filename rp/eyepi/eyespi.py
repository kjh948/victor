#!/usr/bin/python3

import pi3d
import time

import eyepi.eye as eye 
import eyepi.model as model
import eyepi.renderer as renderer
import eyepi.autonomous as autonomous
'''
import eye 
import model
import renderer
import autonomous
'''
try:
    import thread
except ImportError:
    import _thread as thread #Py3K changed it.

# Fake proximity sensor, changes its output every 3 seconds
class ProximitySensor:
    status = True
    end = 0

    def object_in_range(self):
        if self.end <= time.time():
            self.end = time.time() + 3
            self.status = not self.status
        return self.status

# This is the main logic / behaviour of the application.
# Basically we keep the eyas shut until proximity sensor tells us there is an object in range,
# then we open the eyes and keep them open (blinking an moving around) until
# proximity sensor says there is not object in range.
# At this point we close the eyes and start from the beginning.
def controlThread(renderer, eyesModel):

  proximitySensor = ProximitySensor()

  eyePosInput = autonomous.AutonomousEyePositionInput()
  pupilSizeInput = autonomous.AutonomousPupilSizeInput()

  while True:

    # Start with the eyes closed
    #eyesModel.close_eye(model.ALL, time.time(), 0)
    eyesModel.set_position(0, 0)
    eyesModel.set_pupil_size(0)

    renderer.start()

    # Wake up, open eyes slowly
    #eyesModel.open_eye(model.ALL, time.time(), 0.7)
    eyesModel.enable_autoblink(time.time())

    # Put simulators to the same state as the model so there won't be a sudden jump
    # in eye position or pupil size
    #eyePosInput.set_position(0, 0)
    pupilSizeInput.set_size(0)

    last_frame = None

    # While there is an object in range of the sensor, do autonomous eye movement
    while proximitySensor.object_in_range():
        now = time.time()

        # Get data from simulators
        x, y = eyePosInput.get_position(now)
        pupilSize = pupilSizeInput.get_size(now)

        eyesModel.set_position(x, y)
        eyesModel.set_pupil_size(pupilSize)

        # There is no point in moving the eye faster than renderer can draw it
        # otherwise it is going to be a very tight, CPU hogging loop.
        # So wait until Renderer produces another frame even though we do not need it here
        last_frame = renderer.wait_frame(last_frame)

    print("No object in range, going to sleep")

    # Going to sleep, close eyes slowly
    #eyesModel.disable_autoblink()
    #eyesModel.close_eye(model.ALL, time.time(), 0.7)
    # Give the model time to go through the transition
    #time.sleep(1)
    # Stop rendering to not waste resources while we are sleeping
    #renderer.stop()


# MAIN
class r2d2Eye(object):

    def __init__(self, width=320, height=480):
        self.width = width
        self.height = height
        self.gap             = 0#self.width // 2

        displayWidth = 2 * self.width + self.gap
        displayHeight = self.height

        # Display must be created before the eyes or their draw() method throws...
        display = pi3d.Display.create(samples = 4, w = displayWidth, h = displayHeight)
        # make background green while debugging and refactoring so it is easier to see individual eye pieces
        display.set_background(0, 0, 0, 1) # r,g,b,alpha
        # A 2D camera is used, mostly to allow for pixel-accurate eye placement,
        # but also because perspective isn't really helpful or needed here, and
        # also this allows eyelids to be handled somewhat easily as 2D planes.
        # Line of sight is down Z axis, allowing conventional X/Y cartesion
        # coords for 2D positions.
        cam    = pi3d.Camera(is_3d=False, at=(0,0,0), eye=(0,0,-1000))
        light  = pi3d.Light(lightpos=(0, -500, -500), lightamb=(0.2, 0.2, 0.2))

        # eyeRadius is the size, in pixels, at which the whole eye will be rendered
        # onscreen.  eyePosition, also pixels, is the offset (left or right) from
        # the center point of the screen to the center of each eye.
        eyePosition = self.width // 2 + self.gap // 2
        eyeRadius   = self.width / 2.1

        rightEye = eye.Eye(eyeRadius, -eyePosition, 0, True);
        leftEye = eye.Eye(eyeRadius, eyePosition, 0, False);

        self.eyesModel = model.TwoEyesModel()

        self.renderer = renderer.Renderer(display, [leftEye, rightEye], self.eyesModel)

    def start(self, width=320, height=480):
        thread.start_new_thread(controlThread, (self.renderer, self.eyesModel))
        self.renderer.run()

if __name__ == "__main__":
    eyepi = r2d2Eye()
    eyepi.start()
   