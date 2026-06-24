# Project structure

`data/images/` holds original micrographs. `data/masks/` holds matching,
hand-painted PNG masks. Generated clean masks go in `data/validated_masks/`.

`data/test/images/` holds images used for checking a trained model without
adding them to training. Prediction output normally goes to `outputs/`.

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

# Control scripts

`validate_data.py`

Checks that every training image has a same-name PNG mask, that image and mask
sizes match, and that masks use the expected label colors. It can write cleaned
masks to `data/validated_masks/`.

`train.py`

Validates the training data, trains the segmentation model, and writes
checkpoints into `checkpoints/`. It writes `latest.pt` every epoch and
`final.pt` at the end.

`predict.py`

Runs one image through a trained checkpoint. It writes a color mask and overlay
to `outputs/` unless another output folder is passed.

`predict-configurable.py`

Runs prediction on one image or every supported image directly inside a folder.
It uses the constants at the top of the file for checkpoint, output folder,
tile size, and overlap. Its default output folder is `outputs/test/`.

# Important

Do not train until the masks are manually painted and validated.
`python train.py` starts fresh by default. Use
`python train.py --resume checkpoints/latest.pt --epochs N` to continue, where
`N` is the final epoch number, not extra epochs.
The legacy `example-microg-processed/` folder is not used by the pipeline.
