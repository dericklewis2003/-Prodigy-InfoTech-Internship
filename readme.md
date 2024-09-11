# Markov Chain Sentence Autocomplete

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

