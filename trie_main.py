from completion_coordinator import CompletionCoordinator


END_PROMPT = "#"
END_PROGRAM = "exit"


def display_suggestions(suggestions: list) -> None:
    """Display the suggestions to the user."""
    if suggestions:
        print("\nAuto-complete suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
    else:
        print("\nNo suggestions available.")


class MainMenu:

    def __init__(self, dataset_dir: str):
        self.coordinator = CompletionCoordinator(dataset_dir)
        self.current_prompt = ""

    def boot_system(self) -> None:
        """Boot the system by building the trie."""
        print("System is booting. Please wait...\n")
        self.coordinator.build_trie()
        print("System is ready! Start entering your prompt. Press Enter for suggestions or '#' to reset.\n")

    def handle_suggestions(self) -> None:
        """Handle auto-complete suggestions."""
        if self.current_prompt.strip():
            suggestions = self.coordinator.get_suggestions(self.current_prompt.strip())
            display_suggestions([s.completed_sentence for s in suggestions])  # Display only the sentence part
        else:
            print("No prompt entered yet.")

    def run(self) -> None:
        """Run the main loop."""
        self.boot_system()

        while True:
            # Display the current prompt and take input
            print(f"\n{self.current_prompt}", end="")
            added = input()

            if added.strip() == END_PROMPT:
                self.current_prompt = ""
                print("\nPrompt reset. Start typing a new prompt.\n")

            elif added.strip() == END_PROGRAM:
                print("Exit...")
                break

            else:
                self.current_prompt += added + " "
                self.handle_suggestions()


if __name__ == "__main__":
    dataset_directory = "Dataset"
    menu = MainMenu(dataset_directory)
    menu.run()