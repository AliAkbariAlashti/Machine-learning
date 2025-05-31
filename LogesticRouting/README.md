Sure! Here's a clean, well-formatted, and professional-looking **README** in English for your GitHub or documentation:

---

# 🚚 Vehicle Routing and Order Assignment System

This is a **Python-based optimization system** designed to assign customer orders to vehicles efficiently based on **weight**, **volume**, **location**, and **vehicle type** constraints. The system supports multiple vehicle types and uses **Google OR-Tools** for solving the bin-packing problem, with destination prioritization based on **Euclidean distance** from a central warehouse.

---

## 📦 Features

* **Order Assignment**
  Efficiently assigns orders to vehicles based on weight and volume, maximizing vehicle utilization.

* **Cluster-Based Allocation**
  Groups orders by clusters to streamline routing and assignment.

* **Mixed Order Handling**
  Supports orders requiring multiple vehicle types (e.g., normal + coolbox, freezer + coolbox).

* **Destination Prioritization**
  Orders are sorted using a **greedy algorithm** to minimize travel distance from the warehouse:

* **Robust to Empty Inputs**
  Handles empty DataFrames gracefully to avoid crashes.

* **JSON Output**
  Generates detailed, structured JSON output with assignment summaries and Persian character support.

---

## ✅ Prerequisites

* **Python**: 3.8 or higher
* **Dependencies**:

  * `pandas`
  * `numpy`
  * `ortools`
  * `scipy`

---

## 💻 Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-folder>

# Create and activate virtual environment (optional but recommended)
python -m venv venv
# For macOS/Linux:
source venv/bin/activate
# For Windows:
venv\Scripts\activate

# Install dependencies
pip install pandas numpy ortools scipy
```

---

## 📂 Input Data Structure

Place the following CSV files in the project directory (or prepare them as DataFrames):

### 🚚 Vehicle Files

| File Name      | Description             |
| -------------- | ----------------------- |
| `usl_car.csv`  | Normal vehicle details  |
| `col_box.csv`  | Coolbox vehicle details |
| `friz_car.csv` | Freezer vehicle details |

### 📦 Order Files

| File Name        | Description                                    |
| ---------------- | ---------------------------------------------- |
| `usl_table.csv`  | Orders for normal/mixed normal-coolbox types   |
| `friz_table.csv` | Orders for freezer/mixed freezer-coolbox types |

### 📑 Order Columns

All order tables should include:

* `AccountOrderShopResellerID`: Unique order ID
* `BuyerName`: Customer name
* `CategoryType`: Order category
* `TotalWeight`, `TotalVolume`
* `NormalWeight`, `NormalVolume`, `CoolBoxWeight`, `CoolBoxVolume`, `FreezerWeight`, `FreezerVolume` (for mixed orders)
* `Latitude`, `Longitude`: Delivery location
* `Cluster`: Cluster ID for grouping

---

## 🚀 Usage

```bash
# Run the main script
python main.py
```

### 📤 Output

* Printed to console as JSON (UTF-8, Persian supported)
* Output structure includes:

```json
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
  ]
}
```

---

## 🧠 Notes

* **Empty DataFrames**: Returns empty assignments with warning logs.
* **Distance Calculation**: Uses simple Euclidean formula. For realistic distances, consider Google Maps API.
* **Greedy Algorithm**: Prioritization is fast but not always optimal for large datasets.
* **Data Validation**: Ensure input files have valid coordinates and values.

---

## 🔮 Future Improvements

* Integrate real-world distance APIs (e.g., Google Distance Matrix)
* Use advanced routing algorithms (e.g., VRP via OR-Tools)
* Add input validation and error handling
* Support time windows, driver shifts, and other real-world logistics constraints

---

## 📬 Contact

For questions, bug reports, or contributions, please contact:

**\[Ali Akbari Alashti]**
✉️ \[ali.akbari.alashti84@gmail.com]

