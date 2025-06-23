# 🤖 RoboSense Track 1: Driving with Language

<div align="center">

**Official Baseline Implementation for Track 1**

*Based on DriveBench -- "An Empirical Study from the Reliability, Data, and Metric Perspectives"*<br>(https://github.com/drive-bench/toolkit)

[![RoboSense Challenge](https://img.shields.io/badge/RoboSense-2025-blue)](https://robosense2025.github.io/)
[![Track](https://img.shields.io/badge/Track-Drive%20with%20Language-green)](https://robosense2025.github.io/track1)
[![IROS 2025](https://img.shields.io/badge/IROS-2025-red)](https://iros2025.org/)
[![EvalAI](https://img.shields.io/badge/CodaBench-Submit-purple)](https://www.codabench.org/competitions/9285/)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)](LICENSE)

**🏆 Prize Pool: $2,000 USD for Track 1 Winners**

<p align="center">
  <img src="docs/figures/track1.jpg" align="center" width="60%">
</p>

</div>

## Challenge Overview

**Track 1: Drive with Language** challenges participants to develop intelligent driving systems that can understand and act upon natural language instructions in dynamic driving environments. In an era where autonomous vehicles must interpret complex human commands, participants will design algorithms that bridge the gap between natural language understanding and driving actions. 

The challenge focuses on enabling autonomous agents to process commands involving perception, prediction, and planning. Submissions must address key challenges such as accurate scene perception, safe decision-making, and robustness against visual degradation in complex driving scenarios.


### 🎯 Objectives

This track evaluates the capability of VLMs to answer high-level driving questions in complex urban environments. Given questions including perception, prediction, and planning, and a multi-view camera input, participants are expected to answer the question given the visually corrupted images.

- **Perception**: Understand the scene and answer the question about the scene or objects in the scene.
- **Prediction**: Predict the future trajectory of objects in the scene.
- **Planning**: Plan the safe driving actions based on the objects in the scene.


## Competition Details

- **Venue**: IROS 2025, Hangzhou (Oct 19-25, 2025)
- **Registration**: [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSdwfvk-NHdQh9-REiBLCjHMcyLT-sPCOCzJU-ux5jbcZLTkBg/viewform) (Open until Aug 15)
- **Contact**: robosense2025@gmail.com


### 🏆 **Awards**

| Prize | Award |
|:-|:-|
| 🥇 1st Place | $1000 + Certificate |
| 🥈 2nd Place | $600 + Certificate |
| 🥉 3rd Place | $400 + Certificate |
| 🌟 Innovation Award | Cash Award + Certificate |
| Participation | Certificate |


## 📊 Official Dataset

This track uses the **RoboSense Track 1 Drive with Language Dataset**, which is based on the **DriveLM and DriveBench** benchmarks that includes:

- **Multi-view Camera Input**: The input is a multi-view camera input from the nuScenes dataset.
- **Language Instruction**: The instruction is a natural language instruction, including perception, prediction, and planning.
- **Object Localization**: The object is referred to by the center point of the object in the scene.


### Dataset Statistics

| Driving Tasks | Num. of Questions | Question Types                   |
|:-|:-|:-|
| **Perception** | 361 | MCQs, VQA |
| **Prediction** | 522 | MCQs |
| **Planning** | 513 | VQA |

We further distinguish the VQA questions into two types:
- VQA<sub>obj</sub>: The question is about the object in the scene.
- VQA<sub>scene</sub>: The question is about the general scene.


### Baseline Performance (Phase 1)

We use [`Qwen2.5-VL-7B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) as the baseline model. The baseline performance is as follows:

| Task | Question Type | Accuracy (%) |
|:-|:-|:-|
| **Perception** | MCQ | 75.5 |
| | VQA<sub>obj</sub> | 29.2 |
| | VQA<sub>scene</sub> | 22.2 |
| **Prediction** | MCQ | 59.2|
| **Planning** | VQA<sub>obj</sub> | 29.6 |
| | VQA<sub>scene</sub> | 31.2 |
| **Average** | All Types | **42.5** |

## 🚀 Quick Start

We provide a simple demo to run the baseline model.

### 1. **Preparing conda env**

Assuming you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed, let's prepare a conda env:
```
conda create -n drive python=3.10
pip install -r requirements.txt
```

### 2. **Prepare the dataset**
First, convert the data format by running:

```bash
python convert_format.py <input_file> <output_file> 
```

You can also include temporal frames by adding the `--use-temporal` flag with `--num-frames <num_frames>`.

### 3. **Deploy**

We deploy the model using vLLM:

```bash
bash service.sh <GPU_NUM>
```

### 4. Evaluation Baseline

Simply run:

```bash
bash inference.sh
```

#### 📦 Submission Packaging

TBA

#### ⏱ Evaluation Time

TBA

## 🎖️ Challenge Participation

### Submission Requirements
1. **Phase 1**: Submit results on clean test set with reproducible code
2. **Phase 2**: Submit results on corrupted test set with reproducible code
3. **Code**: Submit reproducible code with your final results
4. **Model**: Include trained model weights
5. **Report**: Technical report describing your approach

## 📏 Evaluation Metrics

Our benchmark uses the following metrics: **Accuracy** and **LLM Score**.

| Metric | Description |
|:-|:-|
| **Accuracy** | Used for all Multi-Choice Questions (MCQs) |
| **LLM Score** | Used for all Visual Question Answering (VQA), we prompt an LLM to score the answer given detailed rubrics. |


### Timeline
- **Registration**: [Google Form](https://forms.gle/robosense2025)
- **Phase 1 Deadline**: August 15th
- **Phase 2 Deadline**: September 15th
- **Awards Announcement**: IROS 2025


## 🔗 Resources

- **Challenge Website**: [robosense2025.github.io](https://robosense2025.github.io/)
- **Track Details**: [Track 1 Page](https://robosense2025.github.io/track1)
- **Track Dataset**: [HuggingFace Dataset](https://huggingface.co/datasets/robosense/datasets/tree/main/track1-driving-with-language)
- **Baseline Model**: [HuggingFace Dataset](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)
- **Related Paper**: [arXiv:2409.13244](https://arxiv.org/abs/2501.04003)


## 📧 Contact & Support

- **Email**: robosense2025@gmail.com
- **Official Website**: https://robosense2025.github.io
- **Issues**: Please use GitHub Issues for technical questions


## 📄 Citation

If you use the code and dataset in your research, please cite:

```bibtex
@article{xie2025drivebench,
  title = {Are VLMs Ready for Autonomous Driving? An Empirical Study from the Reliability, Data, and Metric Perspectives},
  author = {Xie, Shaoyuan and Kong, Lingdong and Dong, Yuhao and Sima, Chonghao and Zhang, Wenwei and Chen, Qi Alfred and Liu, Ziwei and Pan, Liang},
  journal = {arXiv preprint arXiv:2501.04003},
  year = {2025}
}
```
```bibtex
@inproceedings{sima2024drivelm,
  title = {DriveLM: Driving with graph visual question answering},
  author = {Sima, Chonghao and Renz, Katrin and Chitta, Kashyap and Chen, Li and Zhang, Hanxue and Xie, Chengen and Bei{\ss}wenger, Jens and Luo, Ping and Geiger, Andreas and Li, Hongyang},
  booktitle = {European Conference on Computer Vision},
  pages = {256-274},
  year = {2024},
  organization = {Springer}
}
```



## Acknowledgements

### RoboSense 2025 Challenge Organizers

<p align="center">
  <img src="docs/figures/organizers.jpg" align="center" width="99%">
</p>


### RoboSense 2025 Program Committee

<p align="center">
  <img src="docs/figures/organizers2.jpg" align="center" width="99%">
</p>



---

<div align="center">

**🤖 Ready to sense the world robustly? Register now and compete for $2,000!**

[**📝 Register Here**](https://docs.google.com/forms/d/e/1FAIpQLSdwfvk-NHdQh9-REiBLCjHMcyLT-sPCOCzJU-ux5jbcZLTkBg/viewform) | [**🌐 Challenge Website**](https://robosense2025.github.io/) | [**📧 Contact Us**](mailto:robosense2025@gmail.com)

Made with ❤️ by the RoboSense 2025 Team

</div>
