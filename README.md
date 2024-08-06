# SQL DDL DATA PUSH
### Description: 

**CSV to SQL Database Importer**

This application processes a CSV dataset, automatically determines the correct data types based on the values, and generates the appropriate SQL Data Definition Language (DDL) statements. The user is then prompted to enter their database information, and the data is pushed to the specified database.

**Key Features**

Data Type Inference: The application analyzes the CSV file and infers the appropriate SQL data types.

Index Detection: The application detects whether an index is present in the CSV file. It prompts the user to add or remove an index if necessary.

Data Type Specification: For columns where the numeric type is ambiguous (e.g., NUMERIC vs. DOUBLE PRECISION or REAL), the application prompts the user to specify the desired type.

**Future Improvements**

Enhanced Error Handling: Although basic error handling is implemented, more robust error handling throughout the program could improve stability and usability.
Statistical Summary Feature: A planned feature is to generate a statistical summary of the numeric values in the dataset. This would provide a quick overview of the data when pushing it to a database.

**Learning and Development**

Object-Oriented Programming: Understanding and applying OOP principles.

Regular Expressions (Regex): Utilizing regex for data validation and formatting.

Data Structures: Exploring different data structures and their use cases.

Type Hinting: Implementing type hinting for better code clarity and error prevention.

Project Organization: Managing a multi-file Python project and creating flowcharts to keep track of functions and program flow.