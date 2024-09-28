import sqlparse
from graphviz import Digraph
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

def parse_sql_to_erd_schema(parsed_sql):
    tables = {}
    relationships = []

    for statement in parsed_sql:
        if statement.get_type() == 'CREATE':
            tokens = [token for token in statement.tokens if not token.is_whitespace]
            if tokens[0].value.lower() == 'create' and tokens[1].value.lower() == 'table':
                table_name = tokens[2].value
                columns = []
                foreign_keys = []
                for token in tokens[3:]:
                    if token.value.startswith('('):
                        column_defs = token.value.strip('()').split(',')
                        for col_def in column_defs:
                            col_parts = col_def.strip().split()

                            if not col_parts:
                                continue

                            col_name = col_parts[0].strip()  # Column name is always the first part

                            # Ignore data types like 'varchar' and other constraints
                            if len(col_parts) > 1 and col_parts[1].lower() in ['varchar', 'numeric', 'int', 'char']:
                                # It's a data type, so we proceed to process the column correctly
                                pass

                            # Handling foreign key relationships
                            if 'foreign' in col_def.lower() and 'references' in col_def.lower():
                                ref_parts = col_def.lower().split('references ')
                                if len(ref_parts) > 1:
                                    ref_info = ref_parts[1].split(' ')
                                    if len(ref_info) >= 2:
                                        ref_table = ref_info[0]
                                        ref_column = ref_info[1].strip('()')
                                        foreign_keys.append((col_name, ref_table, ref_column))
                                    else:
                                        print(f"Warning: Could not parse foreign key reference in column definition: {col_def}")
                            else:
                                # Add valid columns (ignoring constraints like PRIMARY KEY, NOT NULL, etc.)
                                if 'check' not in col_def.lower() and 'primary key' not in col_def.lower() and 'not null' not in col_def.lower():
                                    columns.append(col_name)
                        break
                tables[table_name] = (columns, foreign_keys)

    schema = []
    for table, (columns, foreign_keys) in tables.items():
        col_defs = ' '.join(f'{col}' for col in columns)  # Only include column names
        schema.append(f"Table {table} {{\n  {col_defs}\n}}")

        for col, ref_table, ref_col in foreign_keys:
            relationships.append((table, col, ref_table, ref_col))

    return schema, relationships

def generate_erd(schema, relationships, output_file):
    dot = Digraph(comment='ER Diagram', format='png')

    # Create table nodes
    for line in schema:
        if line.startswith("Table"):
            table_name = line.split(' ')[1]
            columns = [col.strip() for col in line.split('{')[1].strip('}').split(' ') if col.strip()]
            
            # Create the table node
            dot.node(table_name, table_name, shape='box')

            # Create nodes for columns/attributes
            for col in columns:
                attr_name = f'{table_name}_{col}'
                dot.node(attr_name, col, shape='ellipse')
                dot.edge(attr_name, table_name)  # Link attribute to table

    # Create foreign key relationships
    for table1, col1, table2, col2 in relationships:
        dot.edge(table1, table2, label=f'{col1} -> {col2}')

    dot.render(filename=output_file, cleanup=True)

def on_generate_button_click():
    sql_query = sql_text.get("1.0", tk.END)
    parsed_sql = sqlparse.parse(sql_query)
    schema, relationships = parse_sql_to_erd_schema(parsed_sql)

    output_file = 'er_diagram'
    generate_erd(schema, relationships, output_file)
    
    messagebox.showinfo("Success", "ER Diagram generated successfully!")
    os.system(f'start {output_file}.png')

# GUI window
root = tk.Tk()
root.title("ER Diagram Generator")

# Text area for SQL input
tk.Label(root, text="Enter your SQL query:").pack(pady=10)
sql_text = scrolledtext.ScrolledText(root, width=80, height=20)
sql_text.pack(padx=10, pady=10)

# Generate button
generate_button = tk.Button(root, text="Generate ER Diagram", command=on_generate_button_click)
generate_button.pack(pady=10)

root.mainloop()
