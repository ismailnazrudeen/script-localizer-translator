import streamlit as st
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import openai
import random
import os
import base64

# Set the OpenAI API key
openai.api_key = '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'

# Load a pre-trained NER model
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# Prepare lists of names for each country
first_names_india = ['Rahul', 'Priya', 'Vijay', 'Anita']
last_names_india = ['Sharma', 'Kumar', 'Singh', 'Desai']

first_names_china = ['Li', 'Wang', 'Zhang', 'Liu', 'Chen']
last_names_china = ['Li', 'Wang', 'Zhang', 'Liu', 'Chen']

first_names_usa = ['James', 'Mary', 'John', 'Patricia']
last_names_usa = ['Smith', 'Johnson', 'Williams', 'Brown']

# Streamlit UI
st.title('Demo Script Localization')

# User inputs
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    script = uploaded_file.read().decode()

else:
    script= st.text_area("if file not uploaded, PASTE YOUR SCRIPT HERE")


target_language = st.selectbox('Select target language:', ['Spanish', 'French', 'German'])
target_country = st.selectbox('Select target country for names:', ['India', 'China', 'USA'])

# Button to start localization process
if st.button('Localize'):
    # Prepare the translation prompt with examples and the script to translate
    prompt = f"""
    Translate the following English text to {target_language}:
    "{script}"
    """

    # Generate text in the target language using OpenAI
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      temperature=0.5,
      max_tokens=2800
    )
    translated_script = response.choices[0].text.strip()

    # Process the translated script with the NER model
    ner_results = nlp(translated_script)

    # Identify the names in the translated script
    names = [ent['word'] for ent in ner_results if ent['entity'] == 'I-PER']

    # Prepare dictionaries for first and last name replacements
    first_name_replacements = {}
    last_name_replacements = {}

    # Replace each first and last name with a name from the target country
    localized_script = translated_script
    for name in names:
        name_parts = name.split()
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        if target_country == 'India':
            first_names = first_names_india
            last_names = last_names_india
        elif target_country == 'China':
            first_names = first_names_china
            last_names = last_names_china
        elif target_country == 'USA':
            first_names = first_names_usa
            last_names = last_names_usa
        else:
            first_names = []
            last_names = []

        replacement_first_name = first_name_replacements.get(first_name)
        if not replacement_first_name and first_names:
            replacement_first_name = random.choice(first_names)
            first_names.remove(replacement_first_name)  # Remove the chosen name from the list
            first_name_replacements[first_name] = replacement_first_name

        replacement_last_name = last_name_replacements.get(last_name)
        if last_name and not replacement_last_name and last_names:
            replacement_last_name = random.choice(last_names)
            last_names.remove(replacement_last_name)  # Remove the chosen name from the list
            last_name_replacements[last_name] = replacement_last_name

        localized_script = localized_script.replace(first_name, replacement_first_name or first_name)
        if last_name:
            localized_script = localized_script.replace(last_name, replacement_last_name or last_name)

    # Display the localized script
    st.text_area('Localized Script:', value=localized_script)

    # Download link for localized script
    st.markdown(f'<a href="data:file/txt;base64,{base64.b64encode(localized_script.encode()).decode()}" download="localized_script.txt">Download Localized Script</a>', unsafe_allow_html=True)