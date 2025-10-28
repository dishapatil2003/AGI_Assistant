import cv2
import os
import time
import json

# 📁 Create output directory
os.makedirs("data", exist_ok=True)

# 🎥 Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not access the webcam.")
    exit()

# ⏱️ Record duration (in seconds)
duration = 10
start_time = time.time()
output_file = "data/clip_001.mp4"

# 🎬 Define video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = 20.0
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

print("🎥 Recording started... Press 'q' to stop early.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)
    cv2.imshow("Dashcam Recording", frame)

    # Stop if duration exceeded or 'q' pressed
    if (time.time() - start_time) > duration or cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ✅ Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()

# 🧾 Save metadata
metadata = {
    "filename": output_file,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "duration_sec": duration,
    "frame_width": frame_width,
    "frame_height": frame_height,
}
with open("data/metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print(f"✅ Recording saved to {output_file}")
print("🧠 Metadata saved to data/metadata.json")
