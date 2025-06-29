from dotenv import load_dotenv
import chromadb
load_dotenv()






# Step 1 : Dataset 
from langsmith import Client

client = Client()

examples = [
    {
        "inputs": {"question": "What does the 'Require Request Review Comments' setting do?"},
        "outputs": {"answer": "It forces a comments pop-up window while approving a request."},
    },
    {
        "inputs": {"question": "How does 'Role modification auto approve' behave?"},
        "outputs": {"answer": "It automates modifications made to an existing role. (Note: This setting is no longer available as of Release v24.4.)"},
    },
    {
        "inputs": {"question": "What is the function of 'Role Removal Workflow'?"},
        "outputs": {"answer": "It defines the workflow to be used for removing an existing role."},
    },
    {
        "inputs": {"question": "Why is the 'Role default approver' setting useful?"},
        "outputs": {"answer": "It defines a default approver when a specific role approver is not available."},
    },
    {
        "inputs": {"question": "What happens if 'Readonly Role' is enabled?"},
        "outputs": {"answer": "The role becomes available in read-only mode."},
    }
]

# Add metadata to tag your dataset
# dataset = client.create_dataset(
#     dataset_name="Saviant RAG Role Config Q&A",
#     description="Test dataset derived from Enterprise Identity Cloud Admin Guide – Roles section",
#     metadata={"tag": "SaviantTestSet", "source": "admin-guide-pdf"}
# )

# client.create_examples(
#     dataset_id=dataset.id,
#     examples=examples
# )





# CSV data set 
# csv_file = '/Users/shoeb/Desktop/clients_apps/saviant_app/tests/evaluation/rag_test_dataset.csv'

# # The CSV contains two columns: question and answer
# input_keys = ['question']
# output_keys = ['answer']

# dataset = client.upload_csv(
#     csv_file=csv_file,
#     input_keys=input_keys,
#     output_keys=output_keys,
#     name="Saviant RAG Test Dataset",
#     description="Test dataset created from role configuration PDF",
#     # metadata={"tag": "SaviantTestSet", "source": "csv-upload", "purpose": "evaluation"},
#     data_type="kv"
# )



