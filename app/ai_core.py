import os
from google.cloud import speech
import wave

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_secret_key.json"

# 필러 단어
FILLER_WORDS = ["음", "어", "그", "그러니까", "사실", "일단", "막", "이제"]

def get_audio_duration(file_path):
    with wave.open(file_path, "rb") as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration

def analyze_audio_with_google(file_path: str):
    client = speech.SpeechClient()

    # 파일 읽기
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    # 설정
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # WAV 형식
        language_code="ko-KR", # 한국어
        enable_automatic_punctuation=True,
    )

    try:
        # 구글 서버로 전송
        response = client.recognize(config=config, audio=audio)
    except Exception as e:
        return {"error": f"Google STT 오류: {str(e)}"}

    # 결과 텍스트 합치기
    full_text = ""
    for result in response.results:
        full_text += result.alternatives[0].transcript + " "

    full_text = full_text.strip()

    if not full_text:
        return {"error": "음성이 인식되지 않았습니다."}

    # 분석 로직 (WPM, 필러)
    try:
        duration_sec = get_audio_duration(file_path)
    except:
        duration_sec = 0 # 길이를 못 구하면 0 처리

    # WPM 계산
    words = full_text.split()
    word_count = len(words)
    wpm = 0
    if duration_sec > 0:
        wpm = round((word_count / duration_sec) * 60)

    # 필러 카운팅
    filler_count = 0
    detected_fillers = []
    for word in FILLER_WORDS:
        count = full_text.count(word)
        if count > 0:
            filler_count += count
            detected_fillers.append(f"{word}({count})")

    # 점수 계산 (일단 임시로 세팅)
    score = 100
    if wpm < 100 or wpm > 180: score -= 10
    score -= (filler_count * 3)
    score = max(0, score)

    return {
        "text": full_text,
        "duration": round(duration_sec, 1),
        "wpm": wpm,
        "filler_count": filler_count,
        "detected_fillers": detected_fillers,
        "score": score
    }