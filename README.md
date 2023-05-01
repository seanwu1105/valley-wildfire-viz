# Visualize Wildfire Spread Progress in Valley

CS530 Introduction to Scientific Visualization final project @Purdue.

![preview](https://github.com/seanwu1105/valley-wildfire-viz/releases/download/data-holder/preview.png)

![animation](https://github.com/seanwu1105/valley-wildfire-viz/releases/download/data-holder/all.gif)

## Dataset

A dataset provided by IEEE 2022 SciVis Contest is selected for the project.
Follow the instructions below to download the dataset.

## Getting Started

Install Python 3.11 or later.

Install Poetry **1.3.2 or later**. See
[Poetry's documentation](https://python-poetry.org/docs/) for details.

> Poetry earlier than 1.3 will not work.

Install the project's dependencies:

```sh
poetry install --no-root
```

Activate the virtual environment:

```sh
poetry shell
```

After the environment is setup, run the following command to download the
dataset:

```sh
python download.py
```

When the download is complete, run the following command to start the
preprocessing:

```sh
python extract.py
```

Start the application with:

```sh
python main.py
```

## References

- [IEEE 2022 SciVis Contest: Vorticity-driven Lateral Spread Ensemble Data Set](https://www.lanl.gov/projects/sciviscontest2022/)
- [Project Proposal](./proposal.pdf)
- [Project Report](./report.pdf)
- [Project Slides](./slides.pdf)
- [App Preview Video](./preview.webm)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
