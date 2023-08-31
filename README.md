# Weaviate Filter

![PyPI](https://img.shields.io/pypi/v/weaviate-filter)
![GitHub stars](https://img.shields.io/github/stars/wjbmattingly/weaviate-filter)
![PyPI - Downloads](https://img.shields.io/pypi/dm/weaviate-filter)

![weaviate filter logo](images/weaviate-filter-logo.png)

The `weaviate-filter` package provides a convenient way to build GraphQL filters for [Weaviate](https://weaviate.io/). The main class, `GraphQLFilter`, allows you to create complex filters by adding conditions and operands, and then retrieve the final filter object.

## Installation

To install the `weaviate-filter` package, you can use pip:



```
pip install weaviate-filter
```

## Usage

To use the `weaviate-filter` package, you first need to import the `GraphQLFilter` class and create an instance of it:

```python
from weaviate_filter import GraphQLFilter

filter = GraphQLFilter()
```

### Adding a Condition

You can add a condition to the filter by using the `add_condition` method:

```python
filter.add_condition(path="name", operator="Like", value_type="valueString", value="John")
```

- `path`: The path of the property (e.g., "name").
- `operator`: The operator to use for the condition (e.g., "Like").
- `value_type`: The type of the value (e.g., "valueString").
- `value`: The value for the condition (e.g., "John").

### Adding Operands

You can add operands to the filter by using the `add_operands` method:

```python
filter.add_operands(operator="And", operand1, operand2)
```

- `operator`: The operator to use for the operands (e.g., "And").
- `operands`: The operands to add.

### Adding List Conditions as Operands

You can add a list of conditions as operands to the filter by using the `add_list_conditions_as_operands` method:

```python
filter.add_list_conditions_as_operands(path="name", operator="Like", value_type="valueString", values_list=["John", "Doe"])
```

- `path`: The path of the property (e.g., "name").
- `operator`: The operator to use for the conditions (e.g., "Like").
- `value_type`: The type of the values (e.g., "valueString").
- `values_list`: The list of values for the conditions (e.g., ["John", "Doe"]).
- `condition_operator` (optional): The operator to use for the operands (e.g., "Or"). Defaults to "Or".

### Adding Conditions for Multiple Paths

You can add conditions for multiple paths as operands to the filter by using the `add_conditions_for_multiple_paths` method:

```python
filter.add_conditions_for_multiple_paths(paths=["name", "age"], operator="Equal", value_type="valueString", value="John")
```

- `paths`: The paths of the properties (e.g., ["name", "age"]).
- `operator`: The operator to use for the conditions (e.g., "Equal").
- `value_type`: The type of the value (e.g., "valueString").
- `value`: The value for the conditions (e.g., "John").
- `condition_operator` (optional): The operator to use for the operands (e.g., "Or"). Defaults to "Or".

### Getting the Filter

Once you have added all the conditions and operands, you can get the final filter object by using the `get_filter` method:

```python
final_filter = filter.get_filter(operator="And")
```

- `operator` (optional): The operator for the filter (e.g., "And"). Defaults to "And".

The `get_filter` method will return a dictionary with the final filter object.

## Example

Here is a complete example of using the `weaviate-filter` package:

```python
from weaviate_filter import GraphQLFilter

# Create a filter
filter = GraphQLFilter()

# Add a condition
filter.add_condition(path="name", operator="Like", value_type="valueString", value="John")

# Add operands
operand1 = {"path": "age", "operator": "GreaterThan", "valueInt": 30}
operand2 = {"path": "age", "operator": "LessThan", "valueInt": 50}
filter.add_operands(operator="And", operand1, operand2)

# Add list conditions as operands
filter.add_list_conditions_as_operands(path="name", operator="Like", value_type="valueString", values_list=["John", "Doe"])

# Add conditions for multiple paths
filter.add_conditions_for_multiple_paths(paths=["name", "age"], operator="Equal", value_type="valueString", value="John")

# Get the final filter object
final_filter = filter.get_filter(operator="And")

print(final_filter)
```

Output:

```
{'operator': 'And', 'operands': [{'operator': 'And', 'operands': [{'path': 'age', 'operator': 'GreaterThan', 'valueInt': 30}, {'path': 'age', 'operator': 'LessThan', 'valueInt': 50}]}, {'operator': 'Or', 'operands': [{'path': 'name', 'operator': 'Like', 'valueString': 'John'}, {'path': 'name', 'operator': 'Like', 'valueString': 'Doe'}]}, {'operator': 'Or', 'operands': [{'path': ['name'], 'operator': 'Equal', 'valueString': 'John'}, {'path': ['age'], 'operator': 'Equal', 'valueString': 'John'}]}]}
```

# Real Use Case Demo


1. **Import Required Modules**:
    ```python
    import weaviate
    from sentence_transformers import SentenceTransformer
    from weaviate_filter import GraphQLFilter
    ```
    Import the required modules. This includes the Weaviate client, the Sentence Transformers library for encoding the query, and the GraphQLFilter class for constructing the query filter.

2. **Initialize SentenceTransformer Model**:
    ```python
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    ```
    Initialize the SentenceTransformer model. This model is used to convert the text query into a vector.

3. **Setup Weaviate Client**:
    ```python
    WEAVIATE_URL = ""
    WEAVIATE_API_KEY = ""
    client = weaviate.Client(
        url=WEAVIATE_URL,  # Replace w/ your endpoint
        auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),  # Replace w/ your Weaviate instance API key
    )
    ```
    Set up the Weaviate client. You need to replace `WEAVIATE_URL` and `WEAVIATE_API_KEY` with your own Weaviate instance's URL and API key.

4. **Define Filters**:
    ```python
    genders = ["M", "F"]
    countries = ["Germany"]
    labels = ["dlf", "building"]
    ```
    Define the filters you want to apply. In this example, we are filtering for entries with gender "M" or "F", birth_country "Germany", and labels "dlf" or "building" with a value greater than or equal to 1.

5. **Create Filter**:
    ```python
    filter = GraphQLFilter()
    filter.add_list_conditions_as_operands(["gender"], "Equal", "valueText", genders, "Or")
    filter.add_list_conditions_as_operands(["birth_country"], "Equal", "valueText", countries, "Or")
    filter.add_conditions_for_multiple_paths(labels, "GreaterThanEqual", "valueNumber", 1, "Or")
    where_filter = filter.get_filter(operator="Or")
    ```
    Create the filter using the `GraphQLFilter` class. The `add_list_conditions_as_operands` method is used to add a list of conditions as operands with a specified operator ("And" or "Or"). The `add_conditions_for_multiple_paths` method is used to add conditions for multiple paths with a specified operator. Finally, the `get_filter` method is used to get the final filter with a specified operator.

6. **Define and Encode Query**:
    ```python
    query = "We were hungry"
    query_vector = model.encode(query)
    ```
    Define the query and encode it into a vector using the SentenceTransformer model.

7. **Create nearVector Dictionary**:
    ```python
    nearVector = {
    "vector": query_vector
            }
    ```
    Create the `nearVector` dictionary with the encoded query vector.

8. **Define Field Options**:
    ```python
    field_options = ["gender", "window_text", "birth_country", "dlf", "building"]
    ```
    Define the fields you want to retrieve in the query.

9. **Perform Query**:
    ```python
    result = client.query.get(
            "Window", field_options
        ).with_near_vector(
            nearVector
        ).with_limit(2).with_additional(['certainty']
        ).with_where(where_filter).do()
    ```
    Perform the query using the Weaviate client. The `with_near_vector` method is used to add the `nearVector` to the query. The `with_limit` method is used to limit the number of results. The `with_additional` method is used to add additional fields to the query. The `with_where` method is used to add the `where` filter to the query.

10. **Print Results**:
    ```python
    for r in result["data"]["Get"]["Window"]:
        print(r)
    ```
    Print the results of the query.