import imaging
import servo
import time

def main():
    cam_ctrl = imaging.CameraControl()
    servo_ctrl = servo.ServoControl()

    cam_ctrl.set_exposure(100)
    cam_ctrl.set_focus(20)
    cam_ctrl.start_camera()

    SERVO_DUTY_CYCLE = 30

    TOTAL_IMAGES = 100
    #servo_ctrl.start(SERVO_DUTY_CYCLE)
    for i in range(TOTAL_IMAGES):
        print("Acquiring image: " +str(i))
        cam_ctrl.take_picture('./data/image_{:03d}.png'.format(i))
        servo_ctrl.start(SERVO_DUTY_CYCLE)
        time.sleep(2)
        servo_ctrl.stop()
        time.sleep(1)

if __name__== "__main__":
    main()
