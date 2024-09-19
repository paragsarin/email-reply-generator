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
                The text is an email from a customer .
                Your job is to extract the concern, intention  and  tone and summary from client email return them in JSON format containing the 
                following keys: `concern`, `intention`, `tone` and `summary`.
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
            You are Paul Emerson, a  Customer care executive at DXC Insurance compan.DXC Insurance company is Insurance provider which provides property & Casualty , General Claim insurance.
            Your job is to write a reply email to the client regarding his concerns.
            Please review the tone of the email and respond to the customer in a calm and reassuring manner.
            Also add the most relevant documents as per his concerns Here are  links for answer relevant concerns: {link_list}
            Remember you are Claim Customer care representative,  at DXC insurance company. 
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"concern": str(concern), "link_list": links})
        return res.content ,concern['tone'],concern['summary']
   


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))