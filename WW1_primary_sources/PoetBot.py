import openai
import gradio as gr

title = "Welcome to Poet Bot"


# Intfc 1
def api_key(key):
    openai.api_key = key
    return "API KEY: ["+ key + "] SET"

# Completion
def complete(prmpt):
    completion = openai.Completion.create(
        model = "davinci:ft-personal-2023-01-17-15-52-37",
        prompt = prmpt,
        max_tokens = 250,
        top_p= 1,
        frequency_penalty=1,
        presence_penalty=1
    )
    for choice in completion.choices:
            output = choice.text.split()
            output_poem = ' '.join(output)
    return output_poem
# Intfc 2
def text_prompt(ModelPrompt):
    poem = complete(ModelPrompt)
    return poem

intfc1 = gr.Interface(fn = api_key, inputs="text", outputs="text")
intfc2 = gr.Interface(fn = text_prompt, inputs ='text', outputs = 'text')

demo = gr.TabbedInterface([intfc1,intfc2], "API KEY", "POET BOT")

demo.launch()






#print(completion)
print(output_poem)
