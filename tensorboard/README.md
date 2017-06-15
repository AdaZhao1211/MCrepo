# Tensorboard Example
A quick example on tensorboard, a visualization of tensorflow machine learning performance
### Environment
- tensorflow 0.12
- python 3.5.3
### Demo
direct to the tensorboard directory and run
```sh
$ python tensorboard.py
```
Your directory will look like this:
```bash
├── tensorflow.py
├── logs
│   ├── train
│   │── test
└── input_data
```
run tensorboard using the following command
```sh
$ tensorboard --logdir=logs
```
### Credit
[credit to tensorboard](https://github.com/tensorflow/tensorflow/tree/r1.1/tensorflow/tensorboard)
