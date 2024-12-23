from flask import Flask, render_template
import plotly.graph_objects as go

app = Flask(__name__)

def fibonacciRecursive(n, stepCount):
    if n <= 1:
        stepCount[0] += 1
        return n
    else:
        stepCount[0] += 1
        return fibonacciRecursive(n - 1, stepCount) + fibonacciRecursive(n - 2, stepCount)

def fibonacciIterative(n, stepCount):
    if n <= 1:
        stepCount[0] += 1
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        stepCount[0] += 1
        a, b = b, a + b
    return b

def get_performance_data(max_months):
    recursive_results = []
    iterative_results = []
    months = list(range(1, max_months + 1))

    for n in months:
        # Recursive Method
        steps = [0]
        fib_value = fibonacciRecursive(n, steps)
        recursive_results.append((n, fib_value, steps[0]))

        # Iterative Method
        steps = [0]
        fib_value = fibonacciIterative(n, steps)
        iterative_results.append((n, fib_value, steps[0]))

    return recursive_results, iterative_results

@app.route('/')
def index():
    max_months = 12
    recursive_results, iterative_results = get_performance_data(max_months)

    months = [result[0] for result in recursive_results]
    recursive_values = [result[1] for result in recursive_results]
    recursive_steps = [result[2] for result in recursive_results]

    iterative_values = [result[1] for result in iterative_results]
    iterative_steps = [result[2] for result in iterative_results]

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=recursive_steps, mode='lines+markers', name='Recursive Method'))
    fig.add_trace(go.Scatter(x=months, y=iterative_steps, mode='lines+markers', name='Iterative Method'))

    fig.update_layout(
        xaxis_title='Months',
        yaxis_title='Number of Steps',
        title='Recursive vs Iterative Fibonacci'
    )

    # Render the template with the Plotly graph
    return render_template('prac2_2.html', plot=fig.to_html(), 
                           months=months, 
                           recursive_values=recursive_values, 
                           recursive_steps=recursive_steps, 
                           iterative_values=iterative_values, 
                           iterative_steps=iterative_steps)

if __name__ == '__main__':
    app.run(debug=True)
