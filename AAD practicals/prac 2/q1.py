from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def home():
    list1 = [10, 50, 100, 200, 300, 400, 500]
    n = len(list1)
    list2 = []
    list3 = []
    list4 = []
    countForLoop = []
    countForFormula = []
    countForRecursion = []

    # Looping method
    for i in range(n):
        summ = 0
        count = 0
        for j in range(list1[i] + 1):
            summ += j
            count += 1
        list2.append(summ)
        countForLoop.append(count)

    # Equation method
    for x in list1:
        summ = (x * (x + 1)) // 2
        list3.append(summ)
        countForFormula.append(1)

    # Recursive method
    def recursive_sum(x, count=0):
        if x == 0:
            return 0, count
        else:
            sum_recursive, count_recursive = recursive_sum(x - 1, count + 1)
            return x + sum_recursive, count_recursive

    for x in list1:
        summ, count = recursive_sum(x)
        countForRecursion.append(count)

    trace1 = go.Line(x=list1, y=countForLoop, mode='lines+markers', name='Looping Method')
    trace2 = go.Line(x=list1, y=countForFormula, mode='lines+markers', name='Equation Method')
    trace3 = go.Line(x=list1, y=countForRecursion, mode='lines+markers', name='Recursive Method')

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title='Complexity Analysis of Summing Methods',
        xaxis=dict(title='n'),
        yaxis=dict(title='Number of Iterations'),
        legend=dict(x=0, y=1)
    )

    fig = go.Figure(data=data, layout=layout)
    graph_div = pio.to_html(fig, full_html=False)

    return render_template(
        'prac2_1.html',
        graph_div=graph_div,
        list1=list1,
        countForLoop=countForLoop,
        countForFormula=countForFormula,
        countForRecursion=countForRecursion
    )

if __name__ == '__main__':
    app.run(debug=True)
