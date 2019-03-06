import cv2
import os
from threading import Thread

class CameraControl:
    def __init__(self, CAMERA_DEV_ID=0):
        '''
        Sets the environment for image acquisition using the Logitech C920
        camera.
            1) Set up a stream
            2) Disable auto exposure
        Commands related to setting the camera settings need to be run through
        CLI calls to v4l2-ctl as opencv cannot set camera settings properly.
        '''
        self.stream = cv2.VideoCapture(CAMERA_DEV_ID)
        print("Initialized camera id " + str(CAMERA_DEV_ID))

        self.current_frame = None # This is used in conjunction with
                                  # update_frame()
        self.stop_camera = False

        # Disable auto exposure - needs to be done while a stream
        # is open.
        os.system('v4l2-ctl --set-ctrl=exposure_auto=1')
        print("Disabled auto exposure.")

        os.system('v4l2-ctl --set-ctrl=focus_auto=0')
        print("Disabled auto focus.")

    def start_camera(self):
        '''
        Used in conjunction with update_frame()
        '''
        camera_thread = Thread(target=self.update_frame, args=())
        camera_thread.daemon = True
        camera_thread.start()
    
    def update_frame(self):
        '''
        Continually update the frame so the camera buffer stays in sync with
        reality.
        '''
        while(not self.stop_camera):
            ret, self.current_frame = self.stream.read()

            while (self.current_frame == None):
                ret, self.current_frame = self.stream.read()

    def set_exposure(self, exposure):
        '''
        OpenCv cannot set the exposure on the Logitech C920 camera therefore
        we will use the CLI call to v4l2-ctl app to set the exposure.

        Parameters
        ----------

        exposure: int
            Camera exposure min: 3 max: 2047
        '''
        # Use CLI and v4l2-ctl to set camera parameters before starting
        # acquisition.
        # read camera parameter values
        #call(['v4l2-ctl', '--list-ctrls'])

        # Set expsoure manually:
        os.system('v4l2-ctl --set-ctrl=exposure_absolute='+str(exposure))

    def set_focus(self, focus):
        '''
        Parameters
        ----------

        focus : int
            Camera focus min: 0 max: 255
        '''
        os.system('v4l2-ctl --set-ctrl=focus_absolute='+str(focus))

    def take_picture(self, filename):
        '''
        Acquires an image.

        Parameters
        ----------

        filename : str
            Filename where to save the file
        '''
        cv2.imwrite(filename, self.current_frame)

    def close(self):
        '''
        Time to shutdown. Close all open handlers, etc.
        '''
        self.stream.release()
        self.stop_camera = True

    def __enter__(self):
        '''
        Makes the class a context manager.
        '''
        return self

    def __exit__(self, *args):
        '''
        Makes the class a context manager.
        '''
        self.close()
