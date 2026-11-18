import re

def recognize_dialog_act(sentence):
    sentence = sentence.lower().strip()

    if re.search(r'\b(hello|hi|hey|good morning|good evening)\b', sentence):
        return "Greeting"

    elif re.search(r'\b(thank you|thanks)\b', sentence):
        return "Thanking"

    elif re.search(r'\b(bye|goodbye|see you)\b', sentence):
        return "Farewell"

    elif re.search(r'\b(please|could you|would you|can you)\b', sentence):
        return "Request"

    elif re.search(r'\b(what|where|when|why|who|how)\b', sentence) or sentence.endswith('?'):
        return "Question"

    elif re.search(r'\b(sorry|apologize)\b', sentence):
        return "Apology"

    elif re.search(r'\b(yes|yeah|sure|okay|ok)\b', sentence):
        return "Agreement"

    elif re.search(r'\b(no|never|don't|cannot|can't)\b', sentence):
        return "Disagreement"

    else:
        return "Statement"

print("Enter dialog messages. Type 'exit' to stop.")

while True:
    message = input("\nSpeaker: ")

    if message.lower() == "exit":
        break

    act = recognize_dialog_act(message)

    print("Dialog Act:", act)