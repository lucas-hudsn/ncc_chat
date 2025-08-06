from transformers import pipeline

model = pipeline('text-generation', model="Qwen/Qwen3-8B")

print(model("Hello, how are you?", max_length=50, num_return_sequences=1)[0]['generated_text']  )