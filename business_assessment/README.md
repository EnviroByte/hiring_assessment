# Business Logic Assessment

This section tests your understanding of greenhouse gas emissions concepts, regulatory compliance requirements, and data processing skills.

## Part 1: Emissions Concepts Quiz

Complete the multiple-choice quiz in `emissions_quiz.md`. This quiz covers:

- Global Warming Potential (GWP) concepts
- Direct vs. indirect emissions
- Compliance requirements and tightening rates
- Credit allocation and vintage concepts
- Regulatory frameworks

## Part 2: Data Processing Exercise

In this exercise, you'll work with sample emissions data to perform calculations and analysis similar to what you would encounter in a real-world scenario.

### Requirements:

1. Use the provided sample data in `resources/sample_emissions_data.json`
2. Complete the Jupyter notebook `data_processing_exercise.ipynb` with your solutions
3. Implement the following tasks:
   - Clean and transform the raw emissions data
   - Calculate facility-level emissions based on activity data
   - Generate compliance projections for future years
   - Visualize the results with appropriate charts
   - Determine credit requirements based on compliance obligations

### Setup Instructions:

1. Create a Python environment with the necessary packages:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install pandas numpy matplotlib seaborn jupyter
```

2. Start Jupyter Notebook:
```bash
jupyter notebook
```

3. Open the `data_processing_exercise.ipynb` file in the Jupyter interface

4. Complete the exercises in the notebook, adding your code and explanations in the designated cells

### Evaluation Criteria:

- Accuracy of calculations
- Code quality and documentation
- Data handling and transformation techniques
- Understanding of emissions calculation methodologies
- Visualization quality and insights

## Submission Instructions

1. Complete both parts of the assessment
2. Include a brief explanation of your approach for the data processing exercise
3. Ensure your code is well-commented and follows best practices
4. Push your solutions to your forked repository
