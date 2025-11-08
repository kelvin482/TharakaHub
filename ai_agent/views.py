import io
import base64
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib
matplotlib.use('Agg')  # non-GUI backend for server
import matplotlib.pyplot as plt

# Simple AI evaluation function
def evaluate_sales(s):
    if s > 50:
        return "Good"
    return "Needs Improvement"

def upload_view(request):
    """
    Displays the CSV upload form.
    """
    return render(request, 'agent/upload.html')

def plot_view(request):
    """
    Handles CSV upload, evaluates data, generates plot and HTML table.
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return HttpResponse(f"Error reading CSV: {e}", status=400)

        # Require 'Sales' column
        if 'Sales' not in df.columns:
            return HttpResponse("CSV must include a 'Sales' column.", status=400)

        # Apply evaluation
        df['Evaluation'] = df['Sales'].apply(evaluate_sales)

        # Plotting
        fig, ax = plt.subplots(figsize=(8,5))
        ax.bar(df.index, df['Sales'], color='skyblue')
        ax.set_xticks(df.index)
        if 'Month' in df.columns:
            ax.set_xticklabels(df['Month'], rotation=45)
        ax.set_ylabel('Sales')
        ax.set_title('Sales Performance')

        # Annotate bars with evaluation
        for i, val in enumerate(df['Sales']):
            ax.text(i, val + max(df['Sales'])*0.02, df['Evaluation'].iloc[i],
                    ha='center', fontsize=9, fontweight='bold')

        # Save plot to in-memory PNG
        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        graph_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        context = {
            'graph': graph_base64,
            'table': df.to_html(classes='table table-striped', index=False)
        }
        return render(request, 'agent/result.html', context)

    return HttpResponse("Upload a CSV file via POST.", status=400)
