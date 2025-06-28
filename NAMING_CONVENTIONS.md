# FastAPI Project Naming Conventions

Adopting a consistent naming convention is crucial for the maintainability and readability of a FastAPI project. Based on a standard layered architecture, here are some widely-accepted and effective naming conventions for each component.

### General Principles
*   **Python Standard (PEP 8):**
    *   `snake_case` for functions, methods, variables, and filenames.
    *   `PascalCase` for classes.
*   **Clarity and Specificity:** Names should clearly indicate their purpose and scope.
*   **Consistency:** Apply the same patterns across all features.

---

### 1. Models (`src/features/*/models/`)
**Role:** Defines the database table structure (e.g., using SQLAlchemy).

*   **Class Name:** Use a singular noun in `PascalCase`. This represents a single entity in the database.
    *   **Example:** `Product`, `User`, `Organization`
*   **File Name:** Use the singular, `snake_case` version of the class name, suffixed with `_model.py`.
    *   **Example:** `product_model.py`, `user_model.py`

```python
# In: src/features/inventory/models/product_model.py
class Product(Base):
    # ... columns
```

### 2. Schemas (`src/features/*/schemas/`)
**Role:** Defines the data shape for API requests and responses (Pydantic models).

*   **Class Name:** Use the singular noun in `PascalCase` followed by a `Schema` suffix. Use prefixes like `Create`, `Update`, `Read` to distinguish between different data shapes for the same resource.
    *   **Base/Read:** `ProductSchema`
    *   **Creation:** `ProductCreateSchema`
    *   **Update:** `ProductUpdateSchema`
*   **File Name:** Use the singular, `snake_case` name of the resource, suffixed with `_schema.py`.
    *   **Example:** `product_schema.py`

```python
# In: src/features/inventory/schemas/product_schema.py
class ProductBaseSchema(BaseModel):
    name: str

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductSchema(ProductBaseSchema):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
```

### 3. Repository (`src/features/*/repository/`)
**Role:** Handles direct data access and manipulation (CRUD operations on the database).

*   **Class Name:** Use the resource name in `PascalCase` followed by `Repository`.
    *   **Example:** `ProductRepository`, `UserRepository`
*   **Method Names:** Use action verbs that clearly describe the database operation.
    *   `create(db: Session, ...)`
    *   `get(db: Session, id: int)`
    *   `get_by_name(db: Session, name: str)`
    *   `get_multi(db: Session, ...)` or `list(db: Session, ...)`
    *   `update(db: Session, ...)`
    *   `delete(db: Session, id: int)`
*   **File Name:** Use the singular, `snake_case` name of the resource, suffixed with `_repository.py`.
    *   **Example:** `product_repository.py`

### 4. Service (`src/features/*/service/`)
**Role:** Contains the business logic. It orchestrates calls to repositories and other services.

*   **Class Name:** Use the resource name in `PascalCase` followed by `Service`.
    *   **Example:** `ProductService`, `AuthenticationService`
*   **Method Names:** Use verbs that describe the business action. These are often higher-level than repository methods.
    *   `register_new_product(...)`
    *   `get_product_details(product_id: int)`
    *   `update_inventory_stock(...)`
    *   `deactivate_product(product_id: int)`
*   **File Name:** Use the singular, `snake_case` name of the resource, suffixed with `_service.py`.
    *   **Example:** `product_service.py`

### 5. Router (`src/features/*/api/`)
**Role:** Defines the API endpoints, handles HTTP requests, and calls services.

*   **Function Names:** Use a `verb_noun` format that describes the endpoint's action and the resource it handles.
    *   `read_product`
    *   `read_products` (plural for listing multiple items)
    *   `create_product`
    *   `update_product`
    *   `delete_product`
*   **File Name:** Use the plural, `snake_case` name of the resource, suffixed with `_router.py`.
    *   **Example:** `products_router.py`, `users_router.py`

```python
# In: src/features/inventory/api/products_router.py
router = APIRouter()

@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreateSchema, ...):
    # ...

@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, ...):
    # ...
```

### 6. Dependencies (`src/core/dependencies.py`)
**Role:** Provides injectable functions for use in routers (e.g., getting a DB session, authenticating a user).

*   **Function Names:** Use a `get_` prefix or a name that clearly states what it provides.
    *   `get_db_session`
    *   `get_current_user`
    *   `get_product_service`
    *   `paginator`

---

### Summary Table

| Layer Component | File Name Convention | Class Name Convention | Method/Function Name Convention |
| :--- | :--- | :--- | :--- |
| **Model** | `product_model.py` | `Product` | (N/A - attributes) |
| **Schema** | `product_schema.py` | `ProductSchema`, `ProductCreateSchema` | (N/A - attributes) |
| **Repository** | `product_repository.py` | `ProductRepository` | `get()`, `create()`, `get_by_<field>()` |
| **Service** | `product_service.py` | `ProductService` | `register_new_product()`, `get_details()` |
| **Router** | `products_router.py` | (N/A - uses APIRouter) | `read_product()`, `create_product()` |
| **Dependencies** | `dependencies.py` | (N/A) | `get_db_session()`, `get_current_user()` |
