
# 🏠 Aruba Behavior Prediction Demo (GRU)

CASAS Aruba 기반 스마트홈 행동 예측 데모.
GRU 모델로 지난 30분 센서 입력을 보고 다음 10분 행동(sleep/meal/toilet/out)을 예측.
결과를 WorkAdventure에서 시각화.

## 실행 방법
1️⃣ 패키지 설치:
```bash
pip install -r model/requirements.txt
```

2️⃣ 모델 학습:
```bash
python model/train_gru.py
```

3️⃣ 행동 예측:
```bash
python model/predict.py
```

4️⃣ WorkAdventure용 JSON 생성:
```bash
python model/convert_to_wa.py
```

5️⃣ Netlify 배포:
`/web` 폴더만 업로드

WorkAdventure 주소:
https://play.workadventu.re/_/global/adventuretestfordemo.netlify.app/web/maps/aruba.json
