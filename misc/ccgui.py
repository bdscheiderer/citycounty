import tkinter as tk


# Set width x height of window
WIDTH = 500
HEIGHT = 500

def main():

    # Create the main window (root window)
    root = tk.Tk()

    # Set the window title
    root.title("City County Search")

    # Set the window dimensions (width x height)
    root.geometry(f"{str(WIDTH)}x{str(HEIGHT)}")


    # Create an Entry widget for user input
    input_entry = tk.Entry(root, width=50)
    input_entry.pack(pady=10)


    display_button = tk.Button(root, text="Display Input", command=display_input)
    display_button.pack(pady=10)

    output_label = tk.Label(root, text="Enter something above and click the button.")
    output_label.pack(pady=10)


    # Start the Tkinter event loop
    # This keeps the window open and responsive to user interactions
    root.mainloop()


def display_input():
    user_input = input_entry.get() # Get the text from the Entry widget
    output_label.config(text=f"You entered: {user_input}") # Update the Label text

if __name__ == "__main__":
    main()