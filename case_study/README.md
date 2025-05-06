# Case Study: Facility Compliance Projection System

## Overview

In this case study, you will develop an end-to-end solution for a facility compliance projection system. This mini-project integrates both technical skills and domain knowledge to create a practical tool that could be used by facility operators to understand their compliance position and make informed decisions.

## Scenario

EnviroByte has been hired by a large industrial company to develop a system that helps them understand and manage their greenhouse gas emissions compliance obligations. The company operates several facilities across different sectors, each with unique regulatory requirements.

Your task is to create a simplified version of this system that:

1. Processes raw emissions data from facility operations
2. Calculates compliance obligations based on regulatory requirements
3. Projects future compliance positions
4. Provides a user interface to visualize and interact with the data

## Requirements

### 1. Backend (Django/Python)

Create API endpoints using Django Ninja for:

- `GET /api/facilities` - List all facilities (implement in facilities app)
- `GET /api/facilities/{facility_id}` - Get details for a specific facility (implement in facilities app)
- `GET /api/facilities/{facility_id}/emissions` - Get emissions data for a facility (implement in emissions_api app)
- `GET /api/facilities/{facility_id}/compliance` - Get compliance status for a facility (implement in regulatory app)
- `POST /api/compliance/calculate` - Calculate compliance obligation (implement in regulatory app)

You should design the request and response formats based on the sample data provided in the `resources/sample_emissions_data.json` file. There is no need to set up a database - all API endpoints should use this sample data directly. Focus on implementing the business logic for emissions calculations and compliance status.

### 2. Data Processing (Python)

Implement the core calculation logic to:

- Process raw activity data into emissions using appropriate emission factors
- Calculate compliance obligations based on facility type and regulatory requirements
- Determine if a facility is in compliance with its obligations

### 3. Frontend (Next.js/React)

Create a simple web interface that allows users to:

- View a list of facilities
- Select a facility to view its details
- Display emissions data for the selected facility
- Show the compliance status for the selected facility

You should use the API endpoints you've created to fetch the necessary data.

## Provided Resources

- Sample facility and emissions data in `resources/sample_emissions_data.json`
- Regulatory requirements and calculation parameters
- Basic project structure for both frontend and backend components

## Setup Instructions

### Backend Setup

We've already set up a Django project with Django Ninja for you. Your task is to implement the API endpoints.

1. Navigate to the backend directory:
```bash
cd case_study/backend
```

2. Create and activate a virtual environment:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
# Run the server
python manage.py runserver
```

6. Implement the API endpoints using the provided app structure:

The project is organized into three main apps:
- `facilities` - For facility-related models and endpoints
- `emissions_api` - For emissions data and calculation endpoints
- `regulatory` - For compliance and regulatory requirement endpoints

**Note:** The sample data is already loaded in the main `api.py` file and available as the `sample_data` variable. You should pass this data to your app-specific API implementations.

### Frontend Setup

1. Create a new Next.js app in the frontend directory:
```bash
# Navigate to the frontend directory
cd case_study/frontend

# Create a new Next.js app
npx create-next-app@latest .

# When prompted for options, you can use:
# - TypeScript: Yes (recommended)
# - ESLint: Yes
# - Tailwind CSS: Yes (recommended for styling)
# - src/ directory: No (for simplicity)
# - App Router: Yes
```

2. Install dependencies:
```bash
npm install chart.js react-chartjs-2 axios
```

3. Start the development server:
```bash
npm run dev
```

4. Access the application at http://localhost:3000

## Important Notes

- **Focus on Essential Features**: Implement only what's needed to complete the assessment
- **No Authentication Required**: You don't need to implement user authentication
- **Keep It Simple**: Don't overcomplicate the implementation

## Evaluation Criteria

Your solution will be evaluated based on:

1. **Technical Implementation**
   - Code quality and organization
   - Proper use of frameworks and libraries
   - API design and implementation
   - UI/UX implementation

2. **Business Logic**
   - Accuracy of emissions calculations
   - Correct application of regulatory requirements
   - Quality of projections and analysis
   - Handling of edge cases

3. **Documentation and Communication**
   - Code documentation
   - System architecture explanation
   - User guide for the application
   - Assumptions and limitations

## Submission Instructions

1. Implement both the backend and frontend components
2. Include a README with:
   - Setup instructions
   - System architecture overview
   - Key features and functionality
   - Assumptions and limitations
3. Provide screenshots of the working application
4. Push your code to your forked repository
