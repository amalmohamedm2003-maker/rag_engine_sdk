import os
import sys
import json
import tkinter as tk
from tkinter import messagebox

DEFAULT_PROMPTS = {
    "RAG_ANSWER_PROMPT": 'You are a precise question-answering assistant.\n\nUsing ONLY the context provided below, answer the user\'s question faithfully and directly.\nDo NOT make up any information. Do NOT add anything not found in the context.\nIf the context does not contain the answer, say exactly: "The context does not contain sufficient information to answer this question."\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nRespond in this EXACT JSON format (no markdown, no code fences, just raw JSON):\n{\n  "answer": "<your direct answer based solely on the context>",\n  "answerable": true or false\n}\n',
    "SIMPLE_ANSWER_PROMPT": 'You are a precise question-answering assistant.\n\nUsing ONLY the context provided below, answer the user\'s question directly.\nDo NOT make up any information. Do NOT add anything not found in the context.\nIf the context does not contain the answer, say exactly: "The context does not contain sufficient information to answer this question."\n\nContext:\n{context}\n\nQuestion:\n{question}\n'
}

def get_prompts_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "prompts.json")

class PromptEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prompt Editor")
        self.geometry("800x600")
        self.prompts_path = get_prompts_path()
        self.current_prompts = self.load_prompts()
        
        self.create_widgets()
        
    def load_prompts(self):
        if os.path.exists(self.prompts_path):
            try:
                with open(self.prompts_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load prompts: {e}")
        
        return DEFAULT_PROMPTS.copy()

    def create_widgets(self):
        lbl_rag = tk.Label(self, text="RAG_ANSWER_PROMPT:", font=("Helvetica", 10, "bold"))
        lbl_rag.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.txt_rag = tk.Text(self, height=12, width=80)
        self.txt_rag.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.txt_rag.insert(tk.END, self.current_prompts.get("RAG_ANSWER_PROMPT", ""))
        
        lbl_simple = tk.Label(self, text="SIMPLE_ANSWER_PROMPT:", font=("Helvetica", 10, "bold"))
        lbl_simple.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.txt_simple = tk.Text(self, height=12, width=80)
        self.txt_simple.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.txt_simple.insert(tk.END, self.current_prompts.get("SIMPLE_ANSWER_PROMPT", ""))
        
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)
        
        btn_revert = tk.Button(frame_btns, text="Revert to Default", command=self.revert_default, width=20, bg="#f8d7da")
        btn_revert.pack(side=tk.LEFT, padx=10)
        
        btn_save = tk.Button(frame_btns, text="Save as New", command=self.save_new, width=20, bg="#d4edda")
        btn_save.pack(side=tk.LEFT, padx=10)
        
    def revert_default(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to revert to the default prompts?"):
            self.txt_rag.delete("1.0", tk.END)
            self.txt_rag.insert(tk.END, DEFAULT_PROMPTS["RAG_ANSWER_PROMPT"])
            
            self.txt_simple.delete("1.0", tk.END)
            self.txt_simple.insert(tk.END, DEFAULT_PROMPTS["SIMPLE_ANSWER_PROMPT"])
            
            try:
                with open(self.prompts_path, 'w', encoding='utf-8') as f:
                    json.dump(DEFAULT_PROMPTS, f, indent=2)
                messagebox.showinfo("Success", f"Reverted and saved to {os.path.basename(self.prompts_path)} successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")

    def save_new(self):
        new_prompts = {
            "RAG_ANSWER_PROMPT": self.txt_rag.get("1.0", tk.END).strip(),
            "SIMPLE_ANSWER_PROMPT": self.txt_simple.get("1.0", tk.END).strip()
        }
        try:
            with open(self.prompts_path, 'w', encoding='utf-8') as f:
                json.dump(new_prompts, f, indent=2)
            messagebox.showinfo("Success", f"New prompts saved successfully to {os.path.basename(self.prompts_path)}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

if __name__ == "__main__":
    app = PromptEditor()
    app.mainloop()
