# https://python.langchain.com/docs/integrations/document_loaders/confluence/
import os
import dotenv

dotenv.load_dotenv()

from langchain_community.document_loaders import ConfluenceLoader

loader = ConfluenceLoader(url ="https://sysco-confluence.yellowdune-f7432194.eastus2.azurecontainerapps.io/", username=os.environ.get("CONF_USER_NAME"), api_key=os.environ.get("CONF_API_KEY"))
# Or see how to get token: https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html 
# loader = ConfluenceLoader(url ="https://sysco-confluence.yellowdune-f7432194.eastus2.azurecontainerapps.io/", token="")
docs = loader.load(
    space_key="ds", include_attachments=True, limit=50, max_pages=50
)

#print(documents)

for doc in docs:
    print("Content")
    print(doc.page_content)
    print("Metadata id:", doc.metadata["id"])
    print("      title:", doc.metadata["title"])
    print("     source:", doc.metadata["source"])