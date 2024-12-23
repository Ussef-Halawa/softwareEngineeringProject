import random
import tkinter as tk
from tkinter import ttk, messagebox

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz Application")

        # Set window size and center it
        window_width, window_height = 500, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int((screen_height / 2) - (window_height / 2))
        position_right = int((screen_width / 2) - (window_width / 2))
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.root.resizable(False, False)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 14), padding=10)
        self.style.configure("TLabel", font=("Arial", 16))
        self.style.configure("TEntry", font=("Arial", 14))
        self.style.configure("TFrame", background="#f2f2f2")
        self.root.configure(bg="#f2f2f2")

        # Initialize variables
        self.num_questions = 0
        self.difficulty = ""
        self.current_question = 0
        self.score = 0
        self.question_timer = 10
        self.timer_id = None

        # Main Menu
        self.main_menu()

    def main_menu(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Math Quiz Application", font=("Arial", 24, "bold")).pack(pady=20)

        ttk.Label(main_frame, text="Number of Questions:").pack()
        self.num_questions_entry = ttk.Entry(main_frame)
        self.num_questions_entry.pack(pady=10)

        ttk.Label(main_frame, text="Select Difficulty:").pack()
        self.difficulty_var = tk.StringVar(value="")
        ttk.Radiobutton(main_frame, text="Easy", variable=self.difficulty_var, value="Easy").pack(pady=5)
        ttk.Radiobutton(main_frame, text="Hard", variable=self.difficulty_var, value="Hard").pack(pady=5)

        ttk.Button(main_frame, text="Start Quiz", command=self.start_quiz).pack(pady=20)

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

        # Set timer based on difficulty
        if self.difficulty == "Easy":
            self.question_timer = 10  # 10 seconds for Easy
        elif self.difficulty == "Hard":
            self.question_timer = 20  # 20 seconds for Hard

        self.current_question = 0
        self.score = 0

        self.show_question()

    def generate_question(self):
        if self.difficulty == "Easy":
            num1, num2 = random.randint(1, 12), random.randint(1, 12)
        else:
            num1, num2 = random.randint(13, 50), random.randint(50,100)

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

        question_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        question_frame.pack(fill="both", expand=True)

        self.current_question += 1
        self.question, self.correct_answer, self.choices = self.generate_question()

        ttk.Label(question_frame, text=f"Question {self.current_question}/{self.num_questions}", font=("Arial", 18, "bold")).pack(pady=10)
        ttk.Label(question_frame, text=self.question, font=("Arial", 20)).pack(pady=10)

        self.timer_label = ttk.Label(question_frame, text=f"Time left: {self.question_timer}s")
        self.timer_label.pack(pady=10)

        self.progress = ttk.Progressbar(question_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["maximum"] = self.question_timer

        # Create answer buttons
        for choice in self.choices:
            ttk.Button(
                question_frame, 
                text=str(choice), 
                command=lambda c=choice: self.validate_answer_from_button(c)
            ).pack(pady=5, ipadx=20)

        self.start_timer()

    def validate_answer_from_button(self, user_choice):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if user_choice == self.correct_answer:
            self.score += 1
            messagebox.showinfo("Feedback", "Correct!")
        else:
            messagebox.showinfo("Feedback", f"Incorrect! Correct answer: {self.correct_answer}")

        self.show_question()

    def show_report(self):
        self.clear_window()

        report_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        report_frame.pack(fill="both", expand=True)

        ttk.Label(report_frame, text="Quiz Completed!", font=("Arial", 24, "bold")).pack(pady=20)
        ttk.Label(report_frame, text=f"Your Score: {self.score}/{self.num_questions}", font=("Arial", 18)).pack(pady=10)

        # Calculate percentage and show pass/fail message
        percentage = (self.score / self.num_questions) * 100
        if percentage >= 50:
            result_text = "Congratulations! You Passed!"
            result_color = "green"
        else:
            result_text = "Sorry, You Failed."
            result_color = "red"

        ttk.Label(
            report_frame,
            text=result_text,
            font=("Arial", 18, "bold"),
            foreground=result_color
        ).pack(pady=10)

        ttk.Button(report_frame, text="Restart Quiz", command=self.main_menu).pack(pady=10)
        ttk.Button(report_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_timer(self):
        self.remaining_time = self.question_timer
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=f"Time left: {self.remaining_time}s")
            self.progress["value"] = self.question_timer - self.remaining_time
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.progress["value"] = self.question_timer
            messagebox.showinfo("Time's Up!", f"Time is up! The correct answer was: {self.correct_answer}")
            self.show_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
