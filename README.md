---
title: Senti Analyzer Demo
emoji: ⚡
colorFrom: pink
colorTo: indigo
sdk: gradio
sdk_version: 6.14.0
python_version: '3.13'
app_file: app.py
pinned: false
license: mit
short_description: AI-powered sentiment analysis app built using RoBERTa,Gradio
---

Check out the app: https://huggingface.co/spaces/keerthi1515/senti-analyzer-demo


🎬 RoBERTa Sentiment Analysis — Rotten Tomatoes
A fine-tuned RoBERTa-base model for binary sentiment classification of movie reviews. Upgraded from a DistilBERT baseline (82%) to achieve 88.5% test accuracy with balanced precision and recall.



<img width="494" height="364" alt="Screenshot 2026-05-08 123132" src="https://github.com/user-attachments/assets/b7a82d32-665f-4645-8119-466840d34069" />



**Model Description**
This model is a fine-tuned version of FacebookAI/roberta-base trained on the full Rotten Tomatoes movie review dataset for binary sentiment classification.

 •Architecture: RoBERTa-base (12-layer, 768-hidden, 12-heads, 124.6M parameters) with a sequence      classification head.
 •Task: Predicting whether a movie review expresses a positive or negative sentiment
  Output labels: POSITIVE (1) and NEGATIVE (0).
 •Primary use case: Analyzing sentiment in movie reviews and similar short-form text.
 
RoBERTa (Robustly optimized BERT approach) improves on BERT with dynamic masking, larger batches,  longer training, and no next-sentence prediction. These changes yield consistently better     downstream performance on classification tasks (Liu et al., 2019).

**Improvement Over Baseline**



<img width="667" height="151" alt="Screenshot 2026-05-08 122616" src="https://github.com/user-attachments/assets/246af421-acda-463e-ae4c-56d6445108c8" />



**Data Set**



<img width="455" height="314" alt="Screenshot 2026-05-08 122320" src="https://github.com/user-attachments/assets/a62583c2-4b98-4dc5-aee5-92b51cecc789" />



**Data Splits**



<img width="425" height="209" alt="Screenshot 2026-05-08 122205" src="https://github.com/user-attachments/assets/01c6c4b8-5cbb-48d2-b9b5-68e9f1219183" />




**Class Imbalance Assessment**
The dataset is perfectly balanced at 50/50 across all splits (4,265 per class in train). No class weighting, oversampling, or loss rebalancing is needed — standard cross-entropy loss works optimally.

**Preprocessing**
 ⅰ Tokenization: Byte-Pair Encoding (RoBERTa's default, 50,265 vocabulary).
 ⅱ Max sequence length: 128 tokens (with truncation).
ⅲ Padding: Dynamic padding via DataCollatorWithPadding (pads to longest in each batch).
ⅳ Training data: Full dataset used (8,530 training samples).
ⅴ No additional text cleaning — raw review text fed directly to the tokenizer.

**Training Details
Training Configuration**




<img width="581" height="893" alt="Screenshot 2026-05-08 121550" src="https://github.com/user-attachments/assets/5a48aee9-43a2-44c2-a382-dd0fcb99d227" />








**Training Method**

1.Full supervised fine-tuning using the Hugging Face Trainer API with advanced optimization:
Loaded pre-trained RoBERTa-base with a randomly initialized classification head (2 output classes).

2.Fine-tuned all 124.6M parameters (full fine-tuning, not LoRA/adapter-based).

3.Applied linear warmup over 100 steps followed by linear decay.

4.Gradient clipping at norm 1.0 to prevent exploding gradients.

5.Evaluated on validation set after each epoch.

6.Early stopping with patience=2 monitors accuracy to prevent overfitting.

7.Best model selected automatically via load_best_model_at_end=True.

**Training Progress**

<img width="731" height="310" alt="Screenshot 2026-05-08 121118" src="https://github.com/user-attachments/assets/fbef4413-76f7-40ed-b887-4aa372565396" />

Note: Validation loss increases steadily from epoch 1 onwards while training loss drops to 0.06, showing classic overfitting. Best validation accuracy was at epoch 3 (89.0%). Early stopping loaded the best checkpoint.

**Evaluation Results**
Test Set Performance (1,066 samples)
All metrics computed on the full test split (1,066 samples, perfectly balanced at 533 per class).


<img width="421" height="255" alt="Screenshot 2026-05-08 121000" src="https://github.com/user-attachments/assets/df06c01b-a356-4bf7-8820-f7a5c67d17bf" />









<img width="255" height="213" alt="Screenshot 2026-05-08 120931" src="https://github.com/user-attachments/assets/78d121d3-fb73-481b-9045-b7051e683c17" />









**Confusion Matrix**


<img width="496" height="162" alt="Screenshot 2026-05-08 120836" src="https://github.com/user-attachments/assets/ca463dda-816e-4b5f-8f5f-f2c79837927c" />


True Positives: 471 — correctly identified positive reviews
True Negatives: 472 — correctly identified negative reviews
False Positives: 61 — negative reviews misclassified as positive
False Negatives: 62 — positive reviews misclassified as negative
Total misclassified: 123 / 1,066 (11.5%)

**Error Analysis**
Error Patterns


<img width="448" height="200" alt="Screenshot 2026-05-08 115515" src="https://github.com/user-attachments/assets/65e86e47-ac5b-431b-82c8-a26d2d4238b4" />



The errors are nearly perfectly split between FP and FN, confirming the model has no class bias.

**Common Misclassification Patterns**

1.Irony / backhanded praise: "at its worst, the movie is pretty diverting; the pity is that it rarely achieves its best." (POSITIVE labeled, predicted NEGATIVE) — The negative framing masks the positive intent.

2.Mixed sentiment with negative language: "the film feels uncomfortably real, its language and locations bearing the unmistakable stamp of authority." (POSITIVE, predicted NEGATIVE) — "uncomfortably" triggers negative signal.

3.Understated or ambiguous reviews: "shiner can certainly go the distance, but isn't world championship material" (POSITIVE, predicted NEGATIVE) — Subtle conditional praise.
4.Sarcastic inversions: Reviews using negative vocabulary for ironic positive effect.

5.Short, cryptic reviews: Minimal context for inference.

**Results Analysis**
**What 88.5% Accuracy Means**

The model correctly classifies approximately 9 out of every 10 movie reviews — a 6.5 percentage point improvement over the DistilBERT baseline (82%). On a balanced binary task, this represents a 38.5 pp improvement over random chance (50%).

**Why RoBERTa Outperforms DistilBERT ?** 



<img width="674" height="311" alt="Screenshot 2026-05-08 115457" src="https://github.com/user-attachments/assets/aadeb578-367e-46da-898b-5b12a7ba5d36" />




**Limitations & Bias**

Dataset Bias: Domain-specific: Trained exclusively on Rotten Tomatoes — a particular style of English-language film criticism.

English only: No multilingual support.

Temporal bias: Reviews from a specific time period; may not capture evolving language.

Binary oversimplification: Neutral, mixed, or conditional sentiments forced into pos/neg.

**Model Limitations**

Max input length: 128 tokens (~50-70 words). Longer reviews are truncated.

No aspect-level analysis: Single overall sentiment, not per-aspect (acting, plot, etc.).

No explanation: Outputs label + confidence without reasoning.

Domain transfer: Performance degrades on non-movie-review text without adaptation.

**Ethical Considerations**

Not for high-stakes decisions without human review.
Potential for misuse: Review manipulation, surveillance, opinion filtering.
Representation gaps: Training data may not equally represent all demographics/dialects.
Feedback loops: Automated sentiment filtering can suppress legitimate negative opinions.

**Use Cases**

Recommended Applications
Movie review classification — Categorize user reviews as positive/negative.
Customer feedback triage — Route feedback by sentiment polarity.
Content analysis — Track sentiment trends in entertainment media.
Baseline model — Strong starting point before investing in larger models.
Educational tool — Demonstrate NLP fine-tuning and evaluation concepts.
Not Recommended For
Medical, legal, or financial sentiment analysis.
Real-time social media monitoring (without domain adaptation).
Multi-language or code-switched text.
Fine-grained sentiment (1-5 stars, emotion detection).

**Future Improvements**



<img width="771" height="418" alt="Screenshot 2026-05-08 115438" src="https://github.com/user-attachments/assets/cb0ea795-00c5-47e8-8b62-83d97b840adf" />



**Framework Versions**



<img width="201" height="311" alt="Screenshot 2026-05-08 115423" src="https://github.com/user-attachments/assets/62a51904-7d19-43a6-a71d-0ce001987091" />


Links
Model: keerthi1515/roberta-sentiment-rotten-tomatoes
Base model: FacebookAI/roberta-base
Dataset: cornell-movie-review-data/rotten_tomatoes
Baseline model: keerthi1515/distilbert-sentiment-rotten-tomatoes
