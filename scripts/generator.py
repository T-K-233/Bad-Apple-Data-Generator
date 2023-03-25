
import numpy as np
import cv2

INPUT_FILENAME = "./data/bad_apple_original_1080p.mp4"
OUTPUT_FILENAME = "./output/badapple_data.h"


def convert(input_file,
            out_resolution=(10, 8),
            filter_size=45,
            frame_start=0,
            frame_end=10000,
            visualize=False):
    # read in the original video
    cap = cv2.VideoCapture(input_file)

    # trim frames before frame_start
    for i in range(frame_start):
        ret, frame = cap.read()

    frames_data = []
    
    for frame_idx in range(frame_start, frame_end):
        ret, frame = cap.read()

        if not ret:
            break
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (filter_size, filter_size), 0)
        frame = cv2.resize(frame, out_resolution, interpolation=cv2.INTER_CUBIC)

        # generate frame data
        one_frame_data = []
        
        '''
        # row convertion       
        for y in range(frame.shape[0]): # iterate height
            row_data = 0
            for x in range(frame.shape[1]): # iterate width
                row_data |= 0b1 << x
            one_frame_data.append(row_data)
        ''' 
        # column convertion
        for x in range(frame.shape[1]): # iterate width
            col_data = 0
            for y in range(frame.shape[0]): # iterate height
                if frame[y, x]:
                    col_data |= 0b1 << y
            one_frame_data.append(col_data)

        frames_data.append(one_frame_data)
       
        if visualize:
            display_frame = cv2.resize(frame, (out_resolution[0]*10, out_resolution[1]*10), interpolation=cv2.INTER_NEAREST)
            ret, display_frame = cv2.threshold(display_frame, 127, 255, cv2.THRESH_BINARY)
            cv2.imshow("frame", display_frame)
            
        if frame_idx % 20 == 0:
            print(frame_idx)
        
    print(frame_idx)
    return frames_data


def writeResult(output_file, frames_data):
    out_str = ""
    out_str += "const uint8_t frames[{0}][10] = {{".format(len(frames_data))
    
    for frame in frames_data:
        data = 0

        out_str += "{"
        for entry in frame:
            out_str += str(entry)
            out_str += ", "
        out_str += "},\n"

    out_str += "};"
    
    out_file = open(output_file, "w")
    out_file.write(out_str)
    out_file.close()


if __name__ == "__main__":    
    frames_data = convert(INPUT_FILENAME, visualize=False)
    writeResult(OUTPUT_FILENAME, frames_data)


