from logging import raiseExceptions
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os

class SentimentAnalysis():
    def __init__(self):
        path = self.checkpath() #".services/api/src/my_sst2_tuned_model/"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained(path,local_files_only=True)
    
    def run(self, text):
        text = list(text)
        tokenized = self.tokenizer((text), truncation=True, padding='longest', max_length=256, return_tensors='pt')
        tokenized = tokenized.to(self.device)
        outputs = self.model(input_ids = tokenized["input_ids"], attention_mask = tokenized["attention_mask"])
        sentiment_scores = torch.tanh((outputs[0][:, 1] - outputs[0][:, 0]) / 2)
        sentiment_scores = [sentiment_scores[i].item() for i in range(sentiment_scores.shape[0])]
        #refer to confidences score: https://huggingface.co/transformers/task_summary.html?highlight=confidence%20score#sequence-classification
        int_predictions = torch.argmax(outputs[0],dim=1)
        confidences = torch.softmax(outputs[0], dim=1).tolist()
        if sentiment_scores[0] > 0: # if its positive get the confidences in index 1
            confidence_score = confidences[0][1]
        else:
            confidence_score = confidences[0][0]
        return round(sentiment_scores[0],2), round(confidence_score,2)

    def checkpath(self):
        model_name = "my_sst2_tuned_model"
        model_dir = ""
        MODEL_PATH = os.path.join(model_dir, model_name)
        if os.path.isfile(MODEL_PATH):
            return MODEL_PATH
        else:
            raise Exception(f"{model_name} does not exist")
