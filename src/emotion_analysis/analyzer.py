import cv2
import numpy as np
import os


def analyze_emotion_from_image(image_path: str) -> dict:
    """
    Analyze emotion from an image file
    Input:  image path
    Output: emotion results dict
    """
    try:
        from deepface import DeepFace
        result = DeepFace.analyze(
            img_path=image_path,
            actions=['emotion'],
            enforce_detection=False
        )
        if isinstance(result, list):
            result = result[0]

        emotions = result.get('emotion', {})
        dominant = result.get('dominant_emotion', 'neutral')

        return {
            'dominant_emotion': dominant,
            'emotions': emotions,
            'confidence_score': calculate_confidence(emotions)
        }
    except Exception as e:
        print(f"Emotion analysis error: {e}")
        return {
            'dominant_emotion': 'neutral',
            'emotions': {},
            'confidence_score': 50
        }


def capture_webcam_frame() -> str:
    """
    Capture a single frame from webcam
    Output: path to saved image
    """
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    # Save frame
    img_path = "data/raw/emotion_frame.jpg"
    os.makedirs("data/raw", exist_ok=True)
    cv2.imwrite(img_path, frame)
    return img_path


def analyze_live_emotion() -> dict:
    """
    Capture webcam and analyze emotion in one step
    Output: emotion results dict
    """
    img_path = capture_webcam_frame()
    if not img_path:
        return {'dominant_emotion': 'neutral', 'confidence_score': 50}
    return analyze_emotion_from_image(img_path)


def calculate_confidence(emotions: dict) -> int:
    """
    Calculate confidence score from emotions
    Happy + Neutral = confident
    Nervous + Sad + Angry = not confident
    """
    if not emotions:
        return 50

    positive = emotions.get('happy', 0) + emotions.get('neutral', 0)
    negative = emotions.get('fear', 0) + emotions.get('sad', 0) + emotions.get('angry', 0)
    total = positive + negative

    if total == 0:
        return 50

    confidence = (positive / total) * 100
    return round(confidence)


def get_emotion_emoji(emotion: str) -> str:
    """Return emoji for emotion"""
    emojis = {
        'happy': '😊',
        'neutral': '😐',
        'sad': '😢',
        'angry': '😠',
        'fear': '😨',
        'surprise': '😲',
        'disgust': '🤢'
    }
    return emojis.get(emotion.lower(), '😐')


# ---------- TEST IT ----------
if __name__ == "__main__":
    print("Testing Emotion Analyzer...")
    print("Make sure your webcam is connected")
    result = analyze_live_emotion()
    print(f"Dominant Emotion: {result['dominant_emotion']}")
    print(f"Confidence Score: {result['confidence_score']}")