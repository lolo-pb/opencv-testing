# Fiberglass micrograph segmentation

This project trains a neural network to color each micrograph pixel as fiber,
resin, pore, or unidentified.

## Data

Original images belong in `data/images/`. Paint a same-size PNG mask for each
image and save it in `data/masks/` with the same basename:

```text
data/images/micrography-example-0.jpg
data/masks/micrography-example-0.png
```

Masks must use solid colors:

| Class | RGB color |
| --- | --- |
| Fiber | `(255, 0, 0)` red |
| Resin | `(0, 255, 0)` green |
| Pore | `(0, 0, 255)` blue |
| Unidentified/artifact | `(0, 0, 0)` black |

Other colors are reported and snapped to black in `data/validated_masks/`.

## Setup

```bash
source .ven/bin/activate
pip install -r requirements.txt
```

## Commands

Check all masks before training:

```bash
python validate_data.py
```

Train only after the masks have been reviewed:

```bash
python train.py
```

The first run downloads pretrained MobileNetV2 weights. Training automatically
uses a CUDA GPU when available and otherwise uses the CPU.

Segment a new image:

```bash
python predict.py path/to/image.jpg --checkpoint checkpoints/final.pt
```

This writes an exact-color mask and a visual overlay to `outputs/`.

Run tests:

```bash
python -m unittest discover -s tests
```

The legacy `example-microg-processed/` folder is not read by validation or
training.
