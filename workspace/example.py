# Example Python Code
# This file demonstrates the Python Code Editor features

def greet(name):
    """Greet a person with a friendly message"""
    return f"Hello, {name}! Welcome to the Python Code Editor!"

def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def main():
    """Main function to demonstrate the code"""
    print("=== Python Code Editor Demo ===")
    
    # Test greeting function
    message = greet("Developer")
    print(message)
    
    # Test Fibonacci function
    print("\nFibonacci numbers:")
    for i in range(10):
        fib = calculate_fibonacci(i)
        print(f"F({i}) = {fib}")
    
    # Demonstrate error handling
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"\nCaught error: {e}")
        print("This demonstrates error handling in Python!")

if __name__ == "__main__":
    main()
