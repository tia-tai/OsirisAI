import numpy as np
from transformers import AutoProcessor
import evaluate

transformer = AutoProcessor.from_pretrained("facebook/wav2vec2-base")


def compute_metrics(results):
    wer = evaluate.load("wer")
    result_logits = results.predictions
    result_ids = np.argmax(result_logits, axis=-1)

    results.label_ids[results.label_ids == -100] = transformer.tokenizer.pad_token_id

    result_str = transformer.batch_decode(result_ids)
    label_str = transformer.batch_decode(results.label_ids, group_tokens=False)

    wer = wer.compute(predictions=result_str, references=label_str)

    return {"wer": wer}
