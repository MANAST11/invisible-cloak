import cv2
import numpy as np
import time

def empty(a):
    pass

def create_invisible_cloak():
    print("**********************************************")
    print("   Welcome to the Invisible Cloak Project!   ")
    print("**********************************************")
    print("Initializing camera... Prepare any solid colored towel/cloth!")
    
    # Start the webcam
    cap = cv2.VideoCapture(0)
    
    # We give the camera some time to warm up and adjust its white-balance
    time.sleep(3)
    
    # --- SETUP COLOR SLIDERS ---
    # Create a separate window for color adjustment sliders
    cv2.namedWindow("Color Adjustments")
    cv2.resizeWindow("Color Adjustments", 500, 250)
    
    # Defaulting to Blue values as a starting point
    cv2.createTrackbar("Hue Min", "Color Adjustments", 90, 179, empty) 
    cv2.createTrackbar("Hue Max", "Color Adjustments", 130, 179, empty)
    cv2.createTrackbar("Sat Min", "Color Adjustments", 80, 255, empty)
    cv2.createTrackbar("Sat Max", "Color Adjustments", 255, 255, empty)
    cv2.createTrackbar("Val Min", "Color Adjustments", 80, 255, empty)
    cv2.createTrackbar("Val Max", "Color Adjustments", 255, 255, empty)
    
    # 1. CAPTURE THE BACKGROUND
    print("\n[STEP 1] Capturing background in 3 seconds... Please step OUT of the frame!")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
        
    background = None
    # Read multiple frames to let the camera adjust to the lighting of the empty background
    for i in range(60):
        success, background = cap.read()
        if not success:
            continue
    
    print("\n[SUCCESS] Background captured! ")
    print("You can now step into the frame with your cloth.")
    print("Adjust the sliders in the 'Color Adjustments' window until ONLY your cloth disappears!")
    print("To quit, click on any video window and press 'q'.")
    
    # 2. THE MAIN LOOP
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # Optional: Mirror the frame
        frame = cv2.flip(frame, 1)
        background_flipped = cv2.flip(background, 1) # Flip background to match
        
        # Convert the frame from BGR to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 3. GET DYNAMIC VALUES FROM SLIDERS
        h_min = cv2.getTrackbarPos("Hue Min", "Color Adjustments")
        h_max = cv2.getTrackbarPos("Hue Max", "Color Adjustments")
        s_min = cv2.getTrackbarPos("Sat Min", "Color Adjustments")
        s_max = cv2.getTrackbarPos("Sat Max", "Color Adjustments")
        v_min = cv2.getTrackbarPos("Val Min", "Color Adjustments")
        v_max = cv2.getTrackbarPos("Val Max", "Color Adjustments")
        
        lower_bound = np.array([h_min, s_min, v_min])
        upper_bound = np.array([h_max, s_max, v_max])
        
        # 4. CREATE THE MASK
        # This mask will be WHITE (255) where the selected color is found, and BLACK (0) elsewhere
        mask1 = cv2.inRange(hsv, lower_bound, upper_bound)
        
        # We perform morphological operations to clean up the mask
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8), iterations=2)
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((7, 7), np.uint8), iterations=3)
        
        # Show exactly what the computer considers to be the "cloak" (White areas)
        # This makes it super easy to debug and adjust your sliders!
        cv2.imshow("Mask (White = Disappearing Area)", mask1)
        
        # 5. INVERT THE MASK
        mask2 = cv2.bitwise_not(mask1)
        
        # 6. COMPOSITING THE FINAL IMAGE
        # res1 extracts the static background pixels where the mask is detected
        res1 = cv2.bitwise_and(background_flipped, background_flipped, mask=mask1)
        
        # res2 extracts the live camera pixels for the person/room, hiding the cloak
        res2 = cv2.bitwise_and(frame, frame, mask=mask2)
        
        # Combine the magically altered background fragment with the live person feed
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
        
        # Display the final magic result
        cv2.imshow("Invisible Cloak Magic", final_output)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    create_invisible_cloak()
