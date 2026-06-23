# Project structure

`data/images/` holds original micrographs. `data/masks/` holds matching,
hand-painted PNG masks. Generated clean masks go in `data/validated_masks/`.

`src/` contains shared label, dataset, model, loss, and validation code.

# Flow

```text
paint masks
    -> validate_data.py
    -> train.py
    -> checkpoints/final.pt
    -> predict.py
    -> outputs/
```

Training uses image patches and produces a model checkpoint. Prediction loads
that checkpoint and produces a four-color mask plus an overlay.

# Important

Do not train until the masks are manually painted and validated.
The legacy `example-microg-processed/` folder is not used by the pipeline.
