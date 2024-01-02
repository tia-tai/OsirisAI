import torch
from transformers import AutoProcessor
from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class DataCollatorCTCWithPadding:
    transformer: AutoProcessor
    padding: Union[bool, str] = "longest"

    def __call__(
        self, features: List[Dict[str, Union[List[int], torch.Tensor]]]
    ) -> Dict[str, torch.Tensor]:
        input_features = [
            {"input_values": feature["input_values"][0]} for feature in features
        ]
        label_features = [{"input_ids": feature["labels"]} for feature in features]

        batch = self.transformer.pad(
            input_features, padding=self.padding, return_tensors="pt"
        )

        labels_batch = self.transformer.pad(
            labels=label_features, padding=self.padding, return_tensors="pt"
        )

        # replace padding with -100 to ignore loss correctly
        labels = labels_batch["input_ids"].masked_fill(
            labels_batch.attention_mask.ne(1), -100
        )

        batch["labels"] = labels

        return batch
