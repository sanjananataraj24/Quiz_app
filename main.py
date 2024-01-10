import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quiz_data import quiz_data

def show_question():
    question = quiz_data[current_question]
    qs_label.config(text=question["question"])

    choices = question["choices"]
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal")  # Reset button state

    feedback_label.config(text="")
    next_btn.config(state="disabled")

    progress_var.set((current_question + 1) / len(quiz_data) * 100)

def check_answer(choice):
    question = quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    if selected_choice == question["answer"]:
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(quiz_data)))
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

def next_question():
    global current_question

    current_question += 1

    if current_question < len(quiz_data):
        show_question()
    else:
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed!\nFinal score: {}/{}\n".format(
                                score, len(quiz_data)))
        save_high_score()
        root.destroy()

def save_high_score():
    high_scores.append(score)
    high_scores.sort(reverse=True)
    if len(high_scores) > 5:
        high_scores.pop()

root = tk.Tk()
root.title("Quiz App")
root.geometry("600x600")
style = Style(theme="flatly")

style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

qs_label = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

feedback_label = ttk.Label(
    root,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)

score = 0

score_label = ttk.Label(
    root,
    text="Score: 0/{}".format(len(quiz_data)),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=500,
    variable=progress_var,
    mode="determinate"
)
progress_bar.pack(pady=10)

current_question = 0

show_question()

high_scores = []

root.mainloop()
