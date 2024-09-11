# -Prodigy-InfoTech-Internship

# AI Image Generator ------- GA_02

## Description

AI Image Generator is a Python-based desktop application that leverages the power of Hugging Face's Stable Diffusion model to generate images from text prompts. This user-friendly tool allows users to input text descriptions and receive AI-generated images based on those descriptions.

## Features

- Simple and intuitive graphical user interface
- Text-to-image generation using advanced AI models
- Support for multiple aspect ratios (1:1, 16:9, 4:3, 3:2)
- Option to save generated images
- Error handling and retry mechanism for API requests

## Technologies Used

- Python
- Tkinter (for GUI)
- Hugging Face API (Stable Diffusion model)
- Pillow (PIL) for image processing
- Requests library for API communication

# Markov Chain Sentence Autocomplete ------GA_03

This Python script implements a basic sentence autocomplete feature using Markov chains.

## Key Components

1. **MarkovChain Class**: The main class that handles training and autocomplete functionality.

2. **train() Method**: 
   - Input: List of complete sentences
   - Builds a Markov chain based on word transitions in the input sentences

3. **autocomplete() Method**:
   - Input: Start phrase, number of suggestions, maximum words to add
   - Output: List of possible sentence completions

## How It Works

1. The script trains on a set of example sentences.
2. It then generates autocomplete suggestions for given start phrases.
3. The Markov chain model predicts likely word sequences based on the training data.



