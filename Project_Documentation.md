# Project Documentation


## 1. Project Overview

This project is a Python-based microservices application using **FastAPI**. It follows a distributed architecture pattern consisting of:
-   **Service Registry**: Central authority for service discovery.
-   **Core Services**: Business logic services (e.g., Route Optimization).
-   **API Gateways/Adapters**: Public-facing APIs that communicate with backend services.
-   **Legacy Adapters**: Interfaces for integrating with legacy systems.

## 2. Directory Structure

The project is organized efficiently to separate concerns:

```
Capstone_Project/
├── app/
│   ├── api/                # Public-facing API Endpoints (Gateways/Adapters)
│   │   └── ros_adapter/    # Example: Adapter for ROS Service
│   ├── core/               # Core configuration & config.py
│   ├── legacy/             # Legacy systems simulations (Mock services)
│   ├── models/             # Database models (SQLAlchemy)
│   └── services/           # Internal Microservices logic
│       └── service_registry/ # Service Discovery Service
├── requirements.txt        # Project dependencies
├── setup.py                # Installation script
└── ...
```

### Key Directories
-   **`app/api/`**: Contains the REST APIs that clients interact with. These often act as Gateways or Adapters to internal services.
-   **`app/services/`**: The heart of the application. Each subdirectory here should be a self-contained microservice.
-   **`app/services/service_registry/`**: A special service that tracks all active services.
-   **`app/legacy/`**: specific folder for legacy/mock services that we are adapting to.

## 3. Getting Started

### Prerequisites
-   Python 3.8+
-   `pip` (Python Package Installer)

### Installation

1.  **Clone the repository** (if you haven't already).
2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    OR install in editable mode:
    ```bash
    pip install -e .
    ```

## 4. How to Run the Project

Since this is a microservices architecture, you need to run each service process independently. You will need **separate terminal windows for each service and legacy system**.

**Note:** Ensure you actviate your virtual environment in each terminal.

### Step 1: Start the Service Registry
This must be started first so other services can register themselves.
**Port:** 8500

```bash
# Terminal 1
uvicorn app.services.service_registry.service_registry:app --port 8500 --reload
```

then you can start legacy services and other available service as shown in following example.


### Step 2: Start the Legacy Service (Mock)
This simulates the backend legacy system.
**Port:** 8001

```bash
# Terminal 2
uvicorn app.legacy.ros.legacy_ros_service:app --port 8001 --reload
```

### Step 3: Start the ROS Adapter API
This is the public API that talks to the Legacy Service.
**Port:** 8000

```bash
# Terminal 3
uvicorn app.api.ros_adapter.ros_adapter:app --port 8000 --reload
```

> **Important Note for Local Development**:
> If you see connection errors regarding `http://ros-service:8001`, check `app/api/ros_adapter/ros_adapter.py`. You may need to update the registration address to `http://localhost:8000` or `http://localhost:8001` depending on your network setup if not running in Docker.

## 5. How to Implement a New Service

The project follows a **Service-Repository** pattern where business logic and API definitions are separated.

### Phase 1: Create the Service Logic (`app/services/`)

This layer contains the core business logic. It should be implemented as a **class** that acts as a library or helper. It should be agnostic of the HTTP framework (FastAPI) as much as possible.

1.  **Create Directory**: `app/services/new_feature/`
2.  **Create File**: `app/services/new_feature/calculator_service.py`
3.  **Implement Class**:
    ```python
    class CalculatorService:
        def __init__(self, multiplier: int = 1):
            self.multiplier = multiplier

        def add(self, a: int, b: int) -> int:
            # Core business logic here
            return (a + b) * self.multiplier
    ```

### Phase 2: Create the API Layer (`app/api/`)

This layer handles the HTTP requests, validation (Pydantic), and response formatting. It imports and uses the service class from Phase 1.

1.  **Create Directory**: `app/api/new_feature/`
2.  **Create File**: `app/api/new_feature/routes.py` (or `api.py`)
3.  **Implement FastAPI**:
    ```python
    from fastapi import FastAPI, Depends
    from pydantic import BaseModel
    # Import your service class
    from app.services.new_feature.calculator_service import CalculatorService

    app = FastAPI()

    # Initialize the service (or use Dependency Injection)
    service_instance = CalculatorService(multiplier=2)

    class CalculationRequest(BaseModel):
        a: int
        b: int

    @app.post("/calculate")
    def calculate(req: CalculationRequest):
        # Delegate to the service
        result = service_instance.add(req.a, req.b)
        return {"result": result}
    ```

### Phase 3: Registration & Usage

1.  If this is a standalone microservice, you run this `routes.py` (or `main.py` in `app/api`) using uvicorn.
2.  If this is a module within the main monolith, include this router in the main `app/main.py`.

**Key Concept**:
-   **`app/services`**: "How" the work is done (Logic, Database calls, External API calls).
-   **`app/api`**: "When" the work is done (HTTP Endpoints, Request Parsing).

## 6. Troubleshooting

-   **Service Not Found**: Check if the Service Registry is running on port 8500.
-   **Connection Refused**: Ensure all required services (Legacy, etc.) are running in their respective terminals.
-   **Import Errors**: Make sure you are running `uvicorn` from the root `Capstone_Project` directory, so python can resolve `app.xxx`.
