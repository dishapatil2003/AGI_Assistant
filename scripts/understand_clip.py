import os, json, cv2, pytesseract
from vosk import Model, KaldiRecognizer
import wave, subprocess

# === Paths ===
DATA_DIR = "data"
MODEL_PATH = "models/vosk-model-small-en-us-0.15"
VIDEO_PATH = os.path.join(DATA_DIR, "clip_001.mp4")
OUTPUT_JSON = os.path.join(DATA_DIR, "understood_actions.json")
SUMMARY_TXT = os.path.join(DATA_DIR, "summary.txt")

# === Check prerequisites ===
if not os.path.exists(VIDEO_PATH):
    print("❌ No clip_001.mp4 found. Run capture_dashcam.py first.")
    exit()

# === Step 1: Extract a few frames for OCR ===
cap = cv2.VideoCapture(VIDEO_PATH)
frame_texts = []
for i in range(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 30):  # 1 frame ≈ 1 sec
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    if text.strip():
        frame_texts.append(text.strip())
cap.release()

# === Step 2: Dummy transcription from microphone (placeholder) ===
# If you had audio.wav, you could load and run vosk here
transcribed_text = "open notepad and type daily report"  # Example static text

# === Step 3: Simple rule-based workflow understanding ===
actions = {
    "steps": []
}

if "excel" in transcribed_text.lower():
    actions["steps"].append({"action": "open_app", "details": {"app": "excel"}})
if "notepad" in transcribed_text.lower():
    actions["steps"].append({"action": "open_app", "details": {"app": "notepad"}})
if "type" in transcribed_text.lower():
    text_to_type = transcribed_text.split("type")[-1].strip()
    actions["steps"].append({"action": "type_text", "details": {"text": text_to_type}})
if "save" in transcribed_text.lower():
    actions["steps"].append({"action": "save_file", "details": {}})

# === Step 4: Save understanding outputs ===
with open(OUTPUT_JSON, "w") as f:
    json.dump(actions, f, indent=4)

summary = f"""
Observed text from frames:
{frame_texts}

Transcribed audio:
{transcribed_text}

Inferred workflow:
{json.dumps(actions, indent=4)}
"""
with open(SUMMARY_TXT, "w") as f:
    f.write(summary)

print("✅ Understanding complete!")
print(f"JSON saved to: {OUTPUT_JSON}")
print(f"Summary saved to: {SUMMARY_TXT}")
