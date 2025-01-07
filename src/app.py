import grpc
import sys
import numpy as np
import os
import logging
sys.path.append('/service/generated')
import hikrobot_cam_pb2
import hikrobot_cam_pb2_grpc
from ClientLoggerInterceptor import ClientRequestLogger

_logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
def run():
    # Connect to the gRPC server
    options=[('grpc.max_send_message_length', 10 * 1024 * 1024),  # 10 MB limit for send messages
             ('grpc.max_receive_message_length', 10 * 1024 * 1024)]  # 10 MB limit for receive messages
    
    camera_host = os.getenv("CAMERA_HOST", "localhost")    #change env var to set docker network
    _logger.info(f"connect to {camera_host}:50051")


    channel = grpc.insecure_channel(f"{camera_host}:50051",options=options)

    #add interceptor
    interceptor=ClientRequestLogger()
    channel=grpc.intercept_channel(channel, interceptor)
                           
    stub = hikrobot_cam_pb2_grpc.HikRobotCameraServiceStub(channel)

    # Connect to the camera
    serial_number = "J84088695"  # Replace with the actual serial number of the camera
    connect_request = hikrobot_cam_pb2.ConnectRequest(serial_number=serial_number)
    try:
        stub.Connect(connect_request)
        _logger.info(f"Connection successful")
    except grpc.RpcError as e:
        _logger.error(f"Failed to connect to camera: {e.details()}", exc_info=True)
        return

    # Request an image
    try:
        image_request = hikrobot_cam_pb2.GetImageRequest()
        image_response = stub.GetImage(image_request)

        # Process the image
        if image_response.image_data:
            # Convert image data to numpy array
            np_arr = np.frombuffer(image_response.image_data, dtype=np.uint8)
            img = np_arr.reshape((image_response.height, image_response.width, -1))  # Assuming a 3-channel image
            _logger.info(f"received image with {image_response.width} and {image_response.height}")
        else:
            _logger.error("Received image contains no data")
    except grpc.RpcError as e:
         _logger.error(f"Failed to aquire: {e.details()}", exc_info=True)


if __name__ == '__main__':
    run()
