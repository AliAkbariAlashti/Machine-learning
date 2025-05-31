Vehicle Routing and Order Assignment System
Overview
This project is a Python-based vehicle routing and order assignment system designed to optimize the allocation of orders to vehicles based on weight, volume, and location constraints. The system supports multiple types of vehicles (normal, coolbox, freezer) and handles mixed orders requiring multiple vehicle types. It uses the OR-Tools library for solving the bin-packing problem to assign orders to vehicles efficiently. Additionally, it includes a destination prioritization feature to minimize travel distance based on Euclidean distances from a central warehouse.
Features

Order Assignment: Assigns orders to vehicles based on weight and volume constraints, ensuring optimal use of vehicle capacities.
Cluster-Based Allocation: Groups orders by clusters to streamline vehicle assignments.
Mixed Order Handling: Supports mixed orders requiring both normal and coolbox or freezer and coolbox vehicles.
Destination Prioritization: Prioritizes delivery order based on minimizing travel distance from the warehouse (coordinates: 35.73822816917282, 51.05946023574787) using a greedy algorithm.
Empty DataFrame Handling: Gracefully handles empty input DataFrames to prevent errors.
JSON Output: Generates detailed JSON output summarizing assignments, unassigned orders, and unassignable orders due to capacity constraints.

Prerequisites

Python: Version 3.8 or higher
Dependencies:
pandas
numpy
ortools
scipy


Operating System: Compatible with Windows, macOS, or Linux.

Installation

Clone or Download the Repository:
git clone <repository-url>
cd <repository-folder>


Install Dependencies:Create a virtual environment (optional but recommended) and install the required packages:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas numpy ortools scipy


Prepare Input Data:Ensure you have the following CSV files or equivalent DataFrames:

usl_table.csv: Orders for normal and mixed normal-coolbox categories.
friz_table.csv: Orders for freezer and mixed freezer-coolbox categories.
usl_car.csv: Normal vehicle details (Name, Plaque, MaxWeight, Car_volume).
col_box.csv: Coolbox vehicle details.
friz_car.csv: Freezer vehicle details.

Each order DataFrame should include columns:

AccountOrderShopResellerID: Unique order ID.
BuyerName: Name of the buyer.
CategoryType: Type of order.
TotalWeight, TotalVolume: For normal orders.
NormalWeight, NormalVolume, CoolBoxWeight, CoolBoxVolume, FreezerWeight, FreezerVolume: For mixed orders.
Latitude, Longitude: Coordinates of the delivery location.
Cluster: Cluster ID for grouping orders.



Usage

Run the Script:Place the input CSV files in the project directory and run the main script:
python main.py


Output:The script generates a JSON output (result) containing:

allocation_summary: Summary of total orders, allocated orders, unassigned orders, unassignable orders, and processed clusters.
normal_assignments, coolbox_assignments, friz_assignments, coolbox_friz_assignments: Vehicle assignments with order details and delivery priority.
mixed_normal_coolbox_assignments, mixed_friz_coolbox_assignments: Assignments for mixed orders with priority.
unassignable_orders, unassigned_orders: Orders that could not be assigned due to capacity or availability constraints.

The output is printed to the console in JSON format with Persian characters supported.

Priority Assignment:

Orders are prioritized based on Euclidean distance from the warehouse (35.73822816917282, 51.05946023574787).
For each vehicle, orders are sorted using a greedy algorithm to minimize total travel distance.
A priority field is added to each order in the output, indicating the delivery sequence (starting from 1).



Example Output
{
  "allocation_summary": {
    "allocation_date": "2025-05-31",
    "total_orders": 100,
    "allocated_orders": 90,
    "unassigned_orders": 8,
    "unassignable_orders": 2,
    "clusters_processed": [1, 2, 3]
  },
  "normal_assignments": [
    {
      "vehicle": {
        "index": 1,
        "name": "Vehicle1",
        "plaque": "ABC123",
        "max_weight": 1000.0,
        "max_volume": 10.0,
        "remaining_weight": 200.0,
        "remaining_volume": 2.0
      },
      "orders": [
        {
          "order_id": 123,
          "weight": 50.0,
          "volume": 2.0,
          "buyer_name": "Customer1",
          "location": {
            "latitude": 35.74,
            "longitude": 51.06
          },
          "cluster": 1,
          "vehicle_name": "Vehicle1",
          "vehicle_plaque": "ABC123",
          "priority": 1
        }
      ]
    }
  ],
  ...
}

Notes

Empty DataFrames: The script handles empty input DataFrames gracefully, returning empty assignments and logging a message.
Distance Calculation: Uses Euclidean distance for prioritization. For real-world road distances, consider integrating an API like Google Maps Distance Matrix.
Optimization: The greedy algorithm for prioritization is simple and may not always yield the globally optimal route. For larger datasets, consider using OR-Tools' Vehicle Routing Problem solver.
Data Validation: Ensure input coordinates and weights/volumes are valid to avoid runtime errors.

Future Improvements

Integrate real-time road distance calculations using an external API.
Implement advanced routing algorithms (e.g., VRP) for optimal path planning.
Add validation for input data to handle missing or invalid values.
Support additional constraints like time windows or vehicle availability schedules.

Contact
For questions or contributions, please contact [Your Contact Information].
