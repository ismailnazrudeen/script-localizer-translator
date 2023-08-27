# script-localizer-translator
The assignment uses Streamlit to create a user interface where users can upload or input a script, choose a target language and target country for name replacement, and then perform the localization. The script leverages OpenAI for translation and Hugging Face's Transformers for NER and token classification.

# tools required
Libraries to be Imported:
Libraries like streamlit, transformers, openai, and other utilities are imported.

API Key Setup:
OpenAI API key is set using the provided key.

Pre-trained NER Model Setup:
A pre-trained NER model from Hugging Face is loaded using AutoTokenizer and
AutoModelForTokenClassification.
A pipeline for Named Entity Recognition (NER) is created using the loaded model and tokenizer.

# command for running the project
on Terminal:
from project location give the following command for running the project

streamlit run ner-bert.py
