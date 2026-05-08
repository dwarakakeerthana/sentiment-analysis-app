import gradio as gr
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="keerthi1515/roberta-sentiment-rotten-tomatoes"
)

def predict(text):
    result = classifier(text)[0]
    return f"{result['label']} ({result['score']:.2f})"

demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(
        lines=3,
        placeholder="Enter a movie review..."
    ),
    outputs="text",
    title="AI Sentiment Analyzer",
    description="RoBERTa-based movie review sentiment classification"
)

demo.launch()