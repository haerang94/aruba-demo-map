
# WA Visual Fix Pack

- `model/convert_to_wa.py` 는 `web/output/wa_events.json` 을 생성합니다 (Netlify에 `/web`만 올려도 WA에서 접근 가능).
- `web/maps/aruba.json` 은 아이콘용 이미지 레이어 4개(`icon_sleep`, `icon_meal`, `icon_toilet`, `icon_out`)를 포함하고, 기본은 모두 숨김입니다.
- `web/maps/plugins/aruba/plugin.js` 가 `wa_events.json`을 읽어 해당 레이어만 표시합니다.

배포/실행:
1) 기존 파이프라인대로 `train_gru.py`, `predict.py`, `convert_to_wa.py` 실행
2) 생긴 `web/output/wa_events.json` 포함하여 `/web` 폴더를 Netlify에 배포
3) WA에서 `https://play.workadventu.re/_/global/adventuretestfordemo.netlify.app/web/maps/aruba.json?nocache=1` 열기

# Aruba Timeline Animated (GRU-based)

## Run locally
pip install torch pandas numpy scikit-learn joblib pillow
python model/train_gru.py
python model/predict.py
python model/convert_to_wa.py   # writes web/output/wa_events.json

## Deploy
Upload the /web folder to Netlify.
Open:
https://play.workadventu.re/_/global/adventuretestfordemo.netlify.app/web/maps/aruba.json?nocache=300

## Notes
- Icons must exist at /web/assets/icons/{sleep,meal,toilet,out}.png
- The plugin cycles through timeline every 10s and shows probabilities in an overlay.
- The plugin re-fetches timeline every 60s to pick up new predictions.
