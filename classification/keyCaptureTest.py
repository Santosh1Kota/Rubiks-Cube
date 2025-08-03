import cv2
import numpy as np

# Dummy image to show a window
dummy = np.zeros((300, 500, 3), dtype=np.uint8)
cv2.imshow("Press Any Key", dummy)

print("🧪 Press any key inside the window. ESC to exit.")

while True:
    key = cv2.waitKeyEx(0)
    print(f"🔑 Key code: {key}")
    if key == 27:  # ESC
        print("👋 Exiting.")
        break

cv2.destroyAllWindows()