class GraphQLFilter:
    """
    A class to build GraphQL filters for Weaviate.
    
    Attributes:
        ALLOWED_OPERATORS (list): List of allowed operators.
        ALLOWED_VALUE_TYPES (list): List of allowed value types.
        conditions (list): List of conditions added.
        operands (list): List of operands added.
    """

    ALLOWED_OPERATORS = [
        "And", "Or", "Equal", "NotEqual",
        "GreaterThan", "GreaterThanEqual", "LessThan",
        "LessThanEqual", "Like", "WithinGeoRange", "IsNull",
        "ContainsAny", "ContainsAll"
    ]

    ALLOWED_VALUE_TYPES = [
        "valueInt", "valueBoolean", "valueString",
        "valueText", "valueNumber", "valueDate"
    ]

    def __init__(self):
        """Initializes an instance of the GraphQLFilter class."""
        self.conditions = []
        self.operands = []

    def add_condition(self, path, operator, value_type, value):
        """
        Adds a condition to the filter.

        Parameters:
            path (str): The path of the property.
            operator (str): The operator to use for the condition.
            value_type (str): The type of the value.
            value (str, int, bool): The value for the condition.
        
        Raises:
            ValueError: If the operator or value type is not allowed.
        """
        if operator not in self.ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator. Allowed operators are: {', '.join(self.ALLOWED_OPERATORS)}")
        if value_type not in self.ALLOWED_VALUE_TYPES:
            raise ValueError(f"Invalid value type. Allowed value types are: {', '.join(self.ALLOWED_VALUE_TYPES)}")
        self.conditions.append({
            "path": path,
            "operator": operator,
            value_type: value
        })

    def add_operands(self, operator, *operands):
        """
        Adds operands to the filter.

        Parameters:
            operator (str): The operator to use for the operands.
            operands (list): The operands to add.
        
        Raises:
            ValueError: If the operator is not 'And' or 'Or'.
        """
        if operator not in ["And", "Or"]:
            raise ValueError("Invalid operator. Operator must be 'And' or 'Or'")
        self.operands.append({
            "operator": operator,
            "operands": operands
        })

    def add_list_conditions_as_operands(self, path, operator, value_type, values_list, condition_operator="Or"):
        """
        Adds a list of conditions as operands to the filter.

        Parameters:
            path (str): The path of the property.
            operator (str): The operator to use for the conditions.
            value_type (str): The type of the values.
            values_list (list): The list of values for the conditions.
            condition_operator (str, optional): The operator to use for the operands. Defaults to 'Or'.
        
        Raises:
            ValueError: If the operator, value type, or condition operator is not allowed.
        """
        if operator not in self.ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator. Allowed operators are: {', '.join(self.ALLOWED_OPERATORS)}")
        if value_type not in self.ALLOWED_VALUE_TYPES:
            raise ValueError(f"Invalid value type. Allowed value types are: {', '.join(self.ALLOWED_VALUE_TYPES)}")
        if condition_operator not in ["And", "Or"]:
            raise ValueError("Invalid condition operator. Operator must be 'And' or 'Or'")
        operands = [{"path": path, "operator": operator, value_type: value} for value in values_list]
        self.add_operands(condition_operator, *operands)

    def add_conditions_for_multiple_paths(self, paths, operator, value_type, value, condition_operator="Or"):
        """
        Adds conditions for multiple paths as operands to the filter.

        Parameters:
            paths (list): The paths of the properties.
            operator (str): The operator to use for the conditions.
            value_type (str): The type of the value.
            value (str, int, bool): The value for the conditions.
            condition_operator (str, optional): The operator to use for the operands. Defaults to 'Or'.
        
        Raises:
            ValueError: If the operator, value type, or condition operator is not allowed.
        """
        if operator not in self.ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator. Allowed operators are: {', '.join(self.ALLOWED_OPERATORS)}")
        if value_type not in self.ALLOWED_VALUE_TYPES:
            raise ValueError(f"Invalid value type. Allowed value types are: {', '.join(self.ALLOWED_VALUE_TYPES)}")
        if condition_operator not in ["And", "Or"]:
            raise ValueError("Invalid condition operator. Operator must be 'And' or 'Or'")
        operands = [{"path": [path], "operator": operator, value_type: value} for path in paths]
        self.add_operands(condition_operator, *operands)

    def get_filter(self, operator="And"):
        """
        Returns the final filter object.

        Parameters:
            operator (str, optional): The operator for the filter. Defaults to 'And'.
        
        Returns:
            dict: The final filter object.
        
        Raises:
            ValueError: If the operator is not 'And' or 'Or'.
        """
        if operator not in ["And", "Or"]:
            raise ValueError("Invalid operator. Operator must be 'And' or 'Or'")
        if self.operands:
            return {"operator": operator, "operands": self.operands}
        else:
            return {"operator": operator, "operands": self.conditions}
