import pyzed.sl as sl

# Constants
NUM_ITERATIONS = 3
DETECTION_CONFIDENCE_THRESHOLD = 60
OBJECT_CLASS_TO_DETECT = sl.OBJECT_CLASS.PERSON
CAMERA_RESOLUTION = sl.RESOLUTION.HD720
CAMERA_FPS = 15

def initialize_camera():
    print("Initializing camera...")
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.camera_resolution = CAMERA_RESOLUTION
    init_params.camera_fps = CAMERA_FPS
    init_params.coordinate_units = sl.UNIT.FOOT
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print("Failed to open camera.")
        exit()
    print("Camera initialized successfully.")
    return zed

def initialize_object_detection(zed):
    print("Enabling object detection...")
    obj_param = sl.ObjectDetectionParameters()
    obj_param.detection_model = sl.DETECTION_MODEL.MULTI_CLASS_BOX
    obj_param.enable_tracking = True
    zed.enable_object_detection(obj_param)
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = DETECTION_CONFIDENCE_THRESHOLD
    obj_runtime_param.object_class_filter = [OBJECT_CLASS_TO_DETECT]
    obj_runtime_param.object_class_detection_confidence_threshold = {OBJECT_CLASS_TO_DETECT: DETECTION_CONFIDENCE_THRESHOLD}
    print("Object detection enabled successfully.")
    return obj_runtime_param

def initialize_positional_tracking(zed):
    print("Enabling positional tracking...")
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    positional_tracking_parameters.set_as_static = False
    positional_tracking_parameters.set_floor_as_origin = False
    print("Positional tracking enabled successfully.")
    return positional_tracking_parameters

def main():
    print("Running object detection... Press 'Esc' to quit")

    zed = initialize_camera()
    obj_runtime_param = initialize_object_detection(zed)
    positional_tracking_parameters = initialize_positional_tracking(zed)

    for iteration in range(NUM_ITERATIONS):
        print(f"Iteration {iteration + 1}...")
        if zed.grab(obj_runtime_param) == sl.ERROR_CODE.SUCCESS:
            objects = sl.Objects()
            zed.retrieve_objects(objects, obj_runtime_param)
            if objects.is_new:
                # Retrieve data...
                # Save data...
                print("Data saved successfully.")

    # Clean up resources
    zed.disable_object_detection()
    zed.disable_positional_tracking()
    zed.close()

if __name__ == "__main__":
    main()