import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_concerns(self, email_text):
        prompt_extract = PromptTemplate.from_template(
             """
                ### email from a customer:
                {email_text}
                ### INSTRUCTION:
                The text is an email from a customer. Your task is to extract the concern, intention, tone, and summary 
                from the client's email, and return them in JSON format with the following keys: concern, intention, tone, and summary
                Only return the valid JSON.
                ### VALID JSON:    
                """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"email_text": email_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, concern, links):
        prompt_email = PromptTemplate.from_template(
           """ 
            ### Concern:
            {concern}
            ### INSTRUCTION:
             You are Paul Emerson, a Customer Care Executive at DXC Insurance Company, 
            which provides property, casualty, and general claims insurance. 
            Your task is to draft a reply email addressing a client's concerns. 
            Ensure the tone is calm and reassuring. 
            Include the most relevant documents related to their concerns. 
            Here are the links to assist with their inquiries: {link_list}. 
            Remember, you are a Claims Customer Care Representative at DXC Insurance Company.
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"concern": str(concern), "link_list": links})
        return res.content ,concern['tone'],concern['summary']
   


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
