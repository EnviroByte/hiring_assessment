# Facility Compliance Projection System - Frontend

This directory is where you'll create the frontend component of the Facility Compliance Projection System case study.

## Getting Started

1. Create a new Next.js application in this directory:
```bash
# Make sure you're in the frontend directory
npx create-next-app@latest .

# When prompted for options, you can use:
# - TypeScript: Yes (recommended)
# - ESLint: Yes
# - Tailwind CSS: Yes (recommended for styling)
# - src/ directory: No (for simplicity)
# - App Router: Yes
```

2. Install the necessary dependencies:
```bash
npm install chart.js react-chartjs-2 axios
```

3. Run the development server:
```bash
npm run dev
```

## Requirements

Your task is to build a simple, functional frontend for the Facility Compliance Projection System. Focus on implementing these essential features:

### Core Features (Required)

1. **Facility Selection & Overview**:
   - Create a dropdown to select from available facilities
   - Display facility details (name, type, classification, location)
   - Show a summary of current compliance status

2. **Emissions Dashboard**:
   - Display historical emissions data in a table format
   - Create a line chart showing monthly emissions trends
   - Include annual totals and baseline comparisons

3. **Compliance Projection**:
   - Create a chart showing projected emissions vs compliance obligations
   - Calculate and display the compliance gap for each year
   - Visualize credit requirements based on the gap

### Implementation Guidelines

1. **Component Structure**:
   - Create reusable components for charts and data displays
   - Implement a clean, logical page structure
   - Use proper state management for API data

2. **Data Visualization**:
   - Use Chart.js for all visualizations
   - Implement appropriate chart types for different data:
     - Line charts for time-series emissions data
     - Bar charts for comparing actual vs target values
     - Consider using color coding for compliance status

3. **Responsive Design**:
   - Ensure the dashboard works on different screen sizes
   - Use a simple, clean layout that prioritizes data visibility

### Optional Features (If Time Permits)

1. **Data Upload**:
   - Simple form to upload new emissions data
   - Basic validation of uploaded data

2. **Scenario Comparison**:
   - Allow toggling between different projection scenarios

## API Integration

The backend provides several API endpoints that you'll need to consume in your frontend application. Here's how to interact with each endpoint:

### API Endpoints Reference

| Endpoint | Method | Purpose | Example Usage |
|----------|--------|---------|--------------|
| `/api/facilities` | GET | Get list of all facilities | Display facility selection dropdown |
| `/api/facilities/{id}` | GET | Get details for a specific facility | Show facility information dashboard |
| `/api/facilities/{id}/emissions` | GET | Get emissions data for a facility | Display historical emissions chart |
| `/api/facilities/{id}/compliance` | GET | Get compliance status | Show compliance indicators |
| `/api/compliance/calculate` | POST | Calculate compliance obligation | Determine current compliance status |
| `/api/compliance/project` | POST | Generate future projections | Display future compliance chart |
| `/api/compliance/credits` | POST | Calculate credit requirements | Show credit needs visualization |

### API Integration Guidelines

1. **Base URL**: All API endpoints are available at `http://localhost:8000`
2. **Data Format**: All endpoints return JSON data
3. **Error Handling**: Implement proper error handling for all API requests
4. **Loading States**: Show loading indicators while waiting for API responses
5. **Data Transformation**: Transform API response data as needed for chart libraries
6. **CORS**: The backend is configured with CORS headers to allow requests from your frontend
7. **HTTP Methods**: Use appropriate HTTP methods (GET for retrieval, POST for calculations)

## Important Notes

- **No Authentication Required**: You don't need to implement user authentication
- **Focus on Functionality**: Prioritize working features over complex UI
- **Keep It Simple**: Don't overcomplicate the implementation - focus on meeting the core requirements

## Evaluation Criteria

Your frontend implementation will be evaluated based on:
- Functionality and correctness
- Code organization and quality
- Data visualization effectiveness
- UI/UX considerations (even with a simple interface)
- Integration with the backend
