from langchain import PromptTemplate
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.llms.openai import OpenAI
from dotenv import load_dotenv,find_dotenv
import argparse
from pathlib import Path



def build_prompt_template(requirement, license_file):
    """
    Builds the prompt template
    """
    common_implementation_strategy = """
    1. Include the following directories at the root of the repository: "docs", "tests", "code".
    2. Include the following files at the root of the repository: "setup.py", "requirements.txt", "README.md", "LICENSE". These files may be blank to start.
    3. Update the "LICENSE" file to include the content present inside of the file found locally at this path: "{license_file}"
    3. Update the repository files and directories to meet the specifications outlined in the requirement.
    """

    context = """
    You are to generate a python repository. 

    Here is a common implementation strategy:

        {common_implementation_strategy}
    """

    instruction = """
    Requirement:

        {requirement}

    Generate code for a repository following the guidance mentioned above.
    Save all repository directories and files underneath the "./output" directory. 
    """

    prompt_text = f"""
    {context}

    {instruction}
    """

    prompt= PromptTemplate(
    input_variables=["common_implementation_strategy",
                     "requirement", "license_file"],
    template=prompt_text,
    )
    return prompt.format(common_implementation_strategy=common_implementation_strategy,
                         requirement=requirement,
                         license_file=license_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a Python Repository", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-b','--requirement_file', help='Prompt File Containing Requirements Description', default='prompt-examples/requirement.txt')
    parser.add_argument('-l','--license_file', help='Prompt File Containing License Information', default='prompt-examples/license.txt')
    parser.add_argument('-m', '--openai_model_name', help='OpenAI Model to use', default='text-davinci-003')
    parser.add_argument('-r', '--run', help='Specify if an actual run should be performed (Send requests to OpenAI). If not specified, will only generate prompt.', dest='run', action='store_true')
    parser.set_defaults(run=False)
    args = parser.parse_args()

    requirement = Path(args.requirement_file).read_text()
    license_file = Path(args.license_file).read_text()

    load_dotenv(find_dotenv(filename='.env'))
    # Build prompt
    prompt = build_prompt_template(requirement=requirement)
    
    if args.run:
        print("Creating Agent and sending requests to OpenAI ...")
        agent_executor = create_python_agent(
                        llm=OpenAI(temperature=0, max_tokens=1000),
                        tool=PythonREPLTool(),
                        verbose=True
                    )
        # Execute against Python agent
        agent_executor.run(prompt)
    else:
        # Return information on prompt and target ouput filename for sandbox
        print("Entering Dry Run. Requests will not be sent to OpenAI ...")
        print("Displaying Generated Prompt ...")
        print(prompt)
