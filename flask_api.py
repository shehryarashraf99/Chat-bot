from flask import Flask, request, jsonify
import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Set OpenAI API Key
OPENAI_API_KEY = "my_api_key"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Flask app initialization
app = Flask(__name__)

class SQLQueryLogger(SQLDatabase):
    """Custom SQLDatabase to log and capture the last executed SQL query."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_executed_query = None  # Store the last executed query

    def run(self, input_text: str, *args, **kwargs):
        # Log the SQL query
        print(f"Captured SQL Query: {input_text}")
        # Store the last executed query
        self.last_executed_query = input_text
        # Call the original `run` method from SQLDatabase to execute the query
        return super().run(input_text, *args, **kwargs)

    def get_last_query(self):
        """Get the last executed SQL query."""
        return self.last_executed_query
    


mysql_uri = 'mysql+mysqlconnector://root:user_name@localhost:your_port/your_database'
db = SQLQueryLogger.from_uri(mysql_uri)


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
def process_user_query(query):
    # Create a new instance of the database connection

    # Initialize ChatOpenAI model
    
    
    # Create the SQL agent
    agent_executor = create_sql_agent(
        llm,
        db=db,
        agent_type="openai-tools",
        verbose=False
    )
    
    # Execute the query through the agent
    agent_executor.invoke(query)
    
    # After the query is processed, retrieve the final correct SQL query
    final_query = db.get_last_query()

    # Save the correct SQL query in a variable for response
    return final_query

@app.route('/process_query', methods=['POST'])
def process_query():
    try:
        # Get the user query from the request
        
        user_query = request.headers.get('query', '')

        if not user_query:
            return jsonify({"error": "No query provided."}), 400

        # Process the query and generate the SQL query
        sql_query = process_user_query(user_query)

        # Return the result
        return jsonify({"sql_query": sql_query}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
