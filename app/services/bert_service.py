import numpy as np
import onnxruntime as ort
import torch
from transformers import AutoTokenizer


class BertClassifier:

    def __init__(self, model_path, tokenizer_path):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.ort_session = ort.InferenceSession(model_path)
    def get_sentiment_onnx(self, text, return_type='label'):
        """
        Определение тональности текста с помощью ONNX-модели.
        return_type может быть 'label', 'score' или 'proba'.
        """
        # Токенизация текста
        inputs = self.tokenizer(text, return_tensors='np', truncation=True, padding=True, max_length=128)
        input_ids = inputs["input_ids"].astype(np.int64)
        attention_mask = inputs["attention_mask"].astype(np.int64)

        # Выполнение предсказания
        ort_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }
        logits = self.ort_session.run(None, ort_inputs)[0]
        proba = torch.sigmoid(torch.tensor(logits)).cpu().numpy()[0]

        # Интерпретация результатов
        if return_type == 'label':
            return np.argmax(proba)
        elif return_type == 'score':
            return proba.dot([-1, 0, 1])
        return proba
