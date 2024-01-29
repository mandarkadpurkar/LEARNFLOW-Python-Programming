import random

class QuizGame:
    def __init__(self, subject):
        self.subject = subject
        self.points = 0

    def present_question(self, query, choices, correct_choice):
        # Display the question and answer choices to the user
        print(query)
        for i, option in enumerate(choices, 1):
            print(f"{i}. {option}")

        # Get the user's answer
        user_choice = input("Your answer (enter the corresponding number): ")

        # Validate the user's input and check correctness
        if user_choice.isdigit() and 1 <= int(user_choice) <= len(choices):
            user_choice_index = int(user_choice) - 1
            if choices[user_choice_index] == correct_choice:
                print("That's right! Good job.\n")
                self.points += 1
            else:
                print(f"Sorry, the correct answer is {correct_choice}. Keep trying!\n")
        else:
            print("Invalid input. Please enter a valid option.\n")

    def initiate_quiz(self):
        print(f"Welcome to the {self.subject} Quiz!\n")

        # Define difficulty levels for the quiz
        difficulty_levels = {
            'easy': range(1, 11),
            'medium': range(11, 21),
            'hard': range(21, 31)
        }

        # Get user input for the desired difficulty level
        level = input("Choose difficulty (easy, medium, hard): ").lower()

        # Check if the chosen difficulty level is valid
        if level in difficulty_levels:
            # Generate and present 5 random math questions to the user
            for _ in range(5):
                num1 = random.choice(difficulty_levels[level])
                num2 = random.choice(difficulty_levels[level])
                correct_ans = num1 + num2
                question = f"What is the sum of {num1} and {num2}?"
                choices = [correct_ans, random.randint(1, 30), random.randint(1, 30)]
                random.shuffle(choices)

                # Ask the question and update user's score
                self.present_question(question, choices, correct_ans)

            # Display the final score after completing the quiz
            print(f"Quiz completed! Your score is: {self.points}/5")
        else:
            print("Invalid difficulty level. Please choose from easy, medium, or hard.")

if __name__ == "__main__":
    subject = "Mathematics"
    quiz_game = QuizGame(subject)
    quiz_game.initiate_quiz()
