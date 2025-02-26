import cv2
import numpy as np
import time

class TrackbarWindow():
    def __init__(self, title, variables_name, variables, variables_ranges):
        # Create a window
        cv2.namedWindow(title)

        self.title = title
        self.variables_name = variables_name
        self.variables = variables
        self.ranges = variables_ranges

        for index, (name, var, range_) in enumerate(zip(variables_name, variables, variables_ranges)):
            self.variables[index] = range_[0]
            cv2.createTrackbar(name, title, var - range_[0], range_[1] - range_[0], lambda value, idx=index, rg=range_[0]: self.on_trackbar(value, idx, rg))

        self.update_data()
    
    def on_trackbar(self, value, var_index, range):
        self.variables[var_index] = value + range
        self.update_data()

    def update_data(self):
        img = np.zeros((100, 400, 3), dtype=np.uint8)
        countc, countr = 0, 0

        for index, (name, val, range) in enumerate(zip(self.variables_name, self.variables, self.ranges)):
            text = f"{name}: {val} {range}"
            cv2.putText(
                img=img,
                text=text,
                org=((countr * 200) + 10, (countc * 18) + 18),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(255, 255, 255),
                thickness=1
            )

            countc += 1 if (index + 1) % 5 != 0 else -4
            countr += 1 if (index + 1) % 5 == 0 else 0
        
        cv2.imshow(self.title, img)
    
    def get_variable_data(self):
        return (var for var in self.variables)
    
    def destroy(self):
        cv2.destroyAllWindows()

"""
Example of using:
"""
if __name__ == "__main__":
    count = 10
    count1 = 15
    count2 = 10
    count3 = 15
    count4 = 10
    count5 = 15
    count6 = 10
    count7 = 15
    test = TrackbarWindow("Trackbar Example", ["count", "count1", "count2", "count3", "count4", "count5", "count6"], [count, count1, count2, count3, count4, count5, count6, count7], [(-10,20), (10,20), (-10,20), (10,20), (-10,20), (10,20), (-10,20)])

    # Main loop
    while True:
        start_time = time.time()
        count, count1, count2, count3, count4, count5, count6, count7 = test.get_variable_data()
        #print(count, count1)

        # Record the end time
        end_time = time.time()

        # Calculate the total elapsed time
        elapsed_time = (end_time - start_time) * 1000
        print("Elapsed time:", elapsed_time, "milliseconds")

        # Update window every 30 milliseconds
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    test.destroy()