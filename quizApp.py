import random
import tkinter as tk
from tkinter import messagebox

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz Application")

        # Set window size and center it
        window_width, window_height = 400, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int((screen_height / 2) - (window_height / 2))
        position_right = int((screen_width / 2) - (window_width / 2))
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.root.resizable(False, False)

        # Initialize variables
        self.num_questions = 0
        self.difficulty = ""
        self.current_question = 0
        self.score = 0
        self.question_timer = 10  # Seconds per question
        self.timer_id = None

        # Main Menu
        self.main_menu()

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Math Quiz Application", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Number of Questions:").pack()
        self.num_questions_entry = tk.Entry(self.root)
        self.num_questions_entry.pack(pady=10)

        tk.Label(self.root, text="Select Difficulty:").pack()
        self.difficulty_var = tk.StringVar(value="")  # Default to empty
        tk.Radiobutton(self.root, text="Easy", variable=self.difficulty_var, value="Easy").pack(pady=5)
        tk.Radiobutton(self.root, text="Hard", variable=self.difficulty_var, value="Hard").pack(pady=5)

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=20)

    def start_quiz(self):
        try:
            self.num_questions = int(self.num_questions_entry.get())
            if self.num_questions <= 0:
                raise ValueError("Number of questions must be positive.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of questions.")
            return

        self.difficulty = self.difficulty_var.get()
        if not self.difficulty:
            messagebox.showerror("Invalid Input", "Please select a difficulty level.")
            return

        self.current_question = 0
        self.score = 0

        self.show_question()

    def generate_question(self):
        if self.difficulty == "Easy":
            num1, num2 = random.randint(1, 10), random.randint(1, 10)
        else:  # Hard difficulty
            num1, num2 = random.randint(10, 50), random.randint(10, 50)

        operation = random.choice(['+', '-', '*', '/'])
        if operation == '/':
            num1 *= num2  # Ensure divisibility

        question = f"{num1} {operation} {num2}"
        answer = eval(question)

        # Generate multiple choices
        correct_answer = round(answer, 2) if operation == '/' else int(answer)
        choices = [correct_answer]
        while len(choices) < 4:
            fake_answer = correct_answer + random.randint(-10, 10)
            if fake_answer not in choices:
                choices.append(fake_answer)
        random.shuffle(choices)

        return question, correct_answer, choices

    def show_question(self):
        if self.current_question >= self.num_questions:
            self.show_report()
            return

        self.clear_window()

        self.current_question += 1
        self.question, self.correct_answer, self.choices = self.generate_question()

        tk.Label(self.root, text=f"Question {self.current_question}/{self.num_questions}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=self.question, font=("Arial", 18)).pack(pady=10)

        self.answer_var = tk.StringVar(value="")  # Default to empty
        for choice in self.choices:
            tk.Radiobutton(self.root, text=str(choice), variable=self.answer_var, value=str(choice)).pack(anchor="w", padx=20, pady=5)

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.question_timer}s")
        self.timer_label.pack(pady=10)

        tk.Button(self.root, text="Submit Answer", command=self.validate_answer).pack(pady=20)

        self.start_timer()

    def start_timer(self):
        self.remaining_time = self.question_timer
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=f"Time left: {self.remaining_time}s")
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.validate_answer(timeout=True)

    def validate_answer(self, timeout=False):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        user_answer = self.answer_var.get()
        if timeout or user_answer == "":
            feedback = "Time's up!" if timeout else "No answer selected!"
            messagebox.showinfo("Feedback", f"{feedback} Correct answer: {self.correct_answer}")
        else:
            user_answer = float(user_answer)
            if user_answer == self.correct_answer:
                self.score += 1
                messagebox.showinfo("Feedback", "Correct!")
            else:
                messagebox.showinfo("Feedback", f"Incorrect! Correct answer: {self.correct_answer}")

        self.show_question()

    def show_report(self):
        self.clear_window()

        tk.Label(self.root, text="Quiz Completed!", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score}/{self.num_questions}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Restart Quiz", command=self.main_menu).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
