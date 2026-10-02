import io
import os
import numpy as np
from PIL import Image

VOCAB = "0123456789abcdefghijklmnopqrstuvwxyz"
BLANK_IDX = 0


class CaptchaSolver:
    def __init__(self, model_path: str = None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "model", "captcha_crnn.onnx")
        self.model_path = model_path
        self.session = None
        if os.path.exists(self.model_path):
            try:
                import onnxruntime as ort
                # Suppress onnxruntime log spam
                opts = ort.SessionOptions()
                opts.log_severity_level = 3
                self.session = ort.InferenceSession(self.model_path, sess_options=opts, providers=["CPUExecutionProvider"])
                print(f"  -> [OCR] Built-in ONNX Captcha Solver loaded from {self.model_path}", flush=True)
            except Exception as e:
                print(f"  -> [OCR] Warning: Could not initialize ONNX session: {e}", flush=True)

    def is_available(self) -> bool:
        return self.session is not None

    def solve(self, image_bytes: bytes) -> str | None:
        if not self.session:
            return None
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("L")
            img = img.resize((175, 45))
            arr = np.asarray(img, dtype=np.float32) / 255.0
            arr = (arr - 0.5) / 0.5
            tensor = np.expand_dims(np.expand_dims(arr, axis=0), axis=0)

            logits = self.session.run(["logits"], {"image": tensor})[0]
            preds = logits.argmax(axis=2)[0]

            idx_to_char = {i + 1: c for i, c in enumerate(VOCAB)}
            collapsed = []
            prev = BLANK_IDX
            for idx in preds:
                if idx != prev:
                    collapsed.append(idx)
                prev = idx
            text = "".join(idx_to_char[i] for i in collapsed if i != BLANK_IDX)
            return text if text else None
        except Exception as e:
            print(f"  -> [OCR] Error during inference: {e}", flush=True)
            return None


solver = CaptchaSolver()
