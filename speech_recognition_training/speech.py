# Run on Google Collab if you don't have a GPU

from datasets import load_dataset, Audio
from transformers import AutoProcessor, AutoModelForCTC, TrainingArguments, Trainer
from dataCollator import DataCollatorCTCWithPadding
from error import compute_metrics
from huggingface_hub import notebook_login

notebook_login()


# wav2vec2 is programmed to return results in uppercase
def to_Upper(datum):
    return {"text": datum["text"].upper()}


data = load_dataset("MLCommons/peoples_speech", name="clean", split="train[:1000]")
data = data.train_test_split(test_size=0.2)
data = data.cast_column("audio", Audio(sampling_rate=16000))
data = data.map(to_Upper)

transformer = AutoProcessor.from_pretrained("facebook/wav2vec2-base")


def prepare_dataset(batch):
    audio = batch["audio"]
    batch = transformer(
        audio["array"],
        sampling_rate=audio["sampling_rate"],
        text=batch["text"],
    )
    batch["input_length"] = len(batch["input_values"][0])
    return batch


encoded_data = data.map(
    prepare_dataset, remove_columns=data.column_names["train"], num_proc=4
)

data_collator = DataCollatorCTCWithPadding(transformer=transformer)

model = AutoModelForCTC.from_pretrained(
    "facebook/wav2vec2-base",
    ctc_loss_reduction="mean",
    pad_token_id=transformer.tokenizer.pad_token_id,
)

trainArgs = TrainingArguments(
    output_dir="Osiris_asr_model",
    per_device_train_batch_size=40,
    gradient_accumulation_steps=2,
    learning_rate=1e-5,
    warmup_steps=500,
    max_steps=2000,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    group_by_length=True,
    evaluation_strategy="steps",
    per_device_eval_batch_size=8,
    save_steps=1000,
    eval_steps=1000,
    logging_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model="wer",
    greater_is_better=False,
    push_to_hub=True,
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=trainArgs,
    train_dataset=encoded_data["train"],
    eval_dataset=encoded_data["test"],
    tokenizer=transformer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.push_to_hub()
