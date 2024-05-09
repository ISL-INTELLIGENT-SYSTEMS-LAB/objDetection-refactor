import pyzed.sl as sl
import cv2
import numpy as np
import threading
import time
import signal

class CameraManager:
    def __init__(self):
        # Initialize camera-related variables
        self.zed_list = []
        self.left_list = []
        self.depth_list = []
        self.timestamp_list = []
        self.thread_list = []
        self.stop_signal = False

    def signal_handler(self, signal, frame):
        # Signal handler for graceful program termination
        self.stop_signal = True
        time.sleep(0.5)  # Allow time for threads to exit gracefully
        self.cleanup()

    def cleanup(self):
        # Cleanup resources (close cameras and destroy OpenCV windows)
        for zed in self.zed_list:
            if zed.is_opened():
                zed.close()
        cv2.destroyAllWindows()

    def grab_run(self, index):
        # Thread function to grab frames from cameras
        runtime = sl.RuntimeParameters()
        while not self.stop_signal:
            err = self.zed_list[index].grab(runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                self.zed_list[index].retrieve_image(self.left_list[index], sl.VIEW.LEFT)
                self.zed_list[index].retrieve_measure(self.depth_list[index], sl.MEASURE.DEPTH)
                self.timestamp_list[index] = self.zed_list[index].get_timestamp(sl.TIME_REFERENCE.CURRENT).data_ns
            time.sleep(0.001)  # Sleep for 1ms

    def main(self):
        # Main method to initialize cameras and start grabbing frames
        signal.signal(signal.SIGINT, self.signal_handler)

        print("Running...")
        init = sl.InitParameters()
        init.camera_resolution = sl.RESOLUTION.HD720
        init.camera_fps = 30

        cameras = sl.Camera.get_device_list()
        for cam in cameras:
            init.set_from_serial_number(cam.serial_number)
            zed = sl.Camera()
            status = zed.open(init)
            if status == sl.ERROR_CODE.SUCCESS:
                # Add opened cameras to lists and start corresponding threads
                self.zed_list.append(zed)
                self.left_list.append(sl.Mat())
                self.depth_list.append(sl.Mat())
                self.timestamp_list.append(0)
                self.thread_list.append(threading.Thread(target=self.grab_run, args=(len(self.zed_list) - 1,)))
                self.thread_list[-1].start()
            else:
                print(f"Failed to open camera {cam.serial_number}: {status}")

        key = ''
        while key != 'q':
            # Display camera frames and depth information
            for index, zed in enumerate(self.zed_list):
                if zed.is_opened() and self.timestamp_list[index] > 0:
                    cv2.imshow(f"ZED {cameras[index].serial_number}", self.left_list[index].get_data())
                    x = round(self.depth_list[index].get_width() / 2)
                    y = round(self.depth_list[index].get_height() / 2)
                    err, depth_value = self.depth_list[index].get_value(x, y)
                    if np.isfinite(depth_value):
                        print(f"ZED {cameras[index].serial_number} depth at center: {round(depth_value)}mm")
            key = chr(cv2.waitKey(10) & 255)

        self.cleanup()
        print("\nFINISH")

if __name__ == "__main__":
    # Initialize and run the camera manager
    cam_manager = CameraManager()
    cam_manager.main()
