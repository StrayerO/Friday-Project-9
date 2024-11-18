from dotenv import load_dotenv
import os
import openai
import tkinter as tk
from tkinter import scrolledtext

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def get_response(prompt):
    chat_completion = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-2024-08-06",
    )
    return chat_completion.choices[0].message.content.strip()

def send_message(event=None):
    user_input = entry.get("1.0", tk.END).strip()
    if user_input:
        conversation_area.insert(tk.END, "You: " + user_input + "\n", "user")
        response = get_response(user_input)
        conversation_area.insert(tk.END, "Assistant: " + response + "\n", "assistant")
        entry.delete("1.0", tk.END)
        entry.config(height=1)  # Reset height after submission

def exit_program():
    window.destroy()

def update_entry_height(event=None):
    entry_lines = entry.get("1.0", "end-1c").split("\n")
    line_count = sum((len(line) // 50 + 1) for line in entry_lines)  # Adjust based on the width of the entry
    if line_count > 3:
        line_count = 3
    entry.config(height=line_count)

# Create the main window
window = tk.Tk()
window.title("ChatGPT Interface")

# Create a scrolled text area for the conversation
conversation_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20)
conversation_area.pack(padx=10, pady=10)

# Tag configuration for different text styles
conversation_area.tag_configure("user", foreground="black")
conversation_area.tag_configure("assistant", foreground="green")

# Create a text widget for user input with scroll
entry_frame = tk.Frame(window)
entry_frame.pack(padx=10, pady=10)
entry_scroll = tk.Scrollbar(entry_frame)
entry_scroll.pack(side=tk.RIGHT, fill=tk.Y)
entry = tk.Text(entry_frame, wrap=tk.WORD, width=50, height=1, yscrollcommand=entry_scroll.set)
entry.pack(side=tk.LEFT)
entry_scroll.config(command=entry.yview)
entry.bind("<Return>", send_message)
entry.bind("<KeyRelease>", update_entry_height)

# Create a button to send the message
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)

# Create an exit button to close the program
exit_button = tk.Button(window, text="Exit", command=exit_program)
exit_button.pack(padx=10, pady=5)

# Run the Tkinter main loop
window.mainloop()
