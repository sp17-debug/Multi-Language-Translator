import torch
import gradio as gr
import json
from transformers import pipeline

model_path= ("../Models/models--facebook--nllb-200-distilled-600M/snapshots"
             "/f8d333a098d19b4fd9a8b18f94170487ad3f821d")

text_translator = pipeline("translation", model="facebook/nllb-200-distilled-600M",
                           torch_dtype=torch.bfloat16)

with open('language.json', 'r') as file:
    language_data = json.load(file)

def get_FLORES_code_from_language(language):
    for entry in language_data:
        if entry['Language'].lower() == language.lower():
            return entry['FLORES-200 code']
    return None


def translate_text(text, destination_language):
    
    dest_code= get_FLORES_code_from_language(destination_language)
    translation = text_translator(text,
                                  src_lang="eng_Latn",
                                  tgt_lang=dest_code)
    return translation[0]["translation_text"]

gr.close_all()


demo = gr.Interface(fn=translate_text,
                    inputs=[gr.Textbox(label="Input text to translate",lines=6), gr.Dropdown(["German","French", "Hindi", "Romanian	"], label="Select Destination Language")],
                    outputs=[gr.Textbox(label="Translated text",lines=4)],
                    title="@GenAILearniverse Project 4: Multi language translator",
                    description="THIS APPLICATION WILL BE USED TO TRNSLATE ANY ENGLIST TEXT TO MULTIPLE LANGUAGES.")
demo.launch()
