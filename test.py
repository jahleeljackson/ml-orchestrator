import argparse

def greet(name):
    """A function that greets a given name."""
    print(f"Hello, {name}!")

def farewell(name):
    """A function that says farewell to a given name."""
    print(f"Goodbye, {name}!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Call specific functions from the command line.")
    # Add a main argument to specify the function name
    parser.add_argument("function_name", type=str, help="The name of the function to call (greet or farewell).")
    # Add an argument for the name parameter
    parser.add_argument("--Nah", type=str, required=True, help="The name of the person to greet or say farewell to.")

    args = parser.parse_args()

    # Use an if/elif/else block or a dictionary to map the argument to the function
    if args.function_name == "greet":
        greet(args.Nah)

    elif args.function_name == "farewell":
        pass
    else:
        print(f"Error: Unknown function '{args.function_name}'. Use 'greet' or 'farewell'.")
        parser.print_help()

