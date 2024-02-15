from langchain_community.tools.file_management import ReadFileTool, WriteFileTool
from langchain_community.tools.shell import ShellTool
from langchain_experimental.tools import PythonREPLTool
from github import Github
import ast
import types
from langchain.chat_models import ChatOllama
from get_code_from_markdown import get_code_from_markdown
from yapf.yapflib.yapf_api import FormatCode
from io import StringIO
from contextlib import redirect_stdout

tools = None


def setup(ToolManager):
    global tools
    ToolManager.add(save_file_tool)
    ToolManager.add(load_file_tool)
    ToolManager.add(execute_command_line_tool)
    ToolManager.add(execute_python_tool)
    ToolManager.add(save_code_to_repository_tool)
    ToolManager.add(generate_code)
    ToolManager.add(create_tool)
    tools = ToolManager


def generate_code(request: str) -> str:
    """
    This tool generates python code.
    """
    code_llm = ChatOllama(model="magicoder", temperature=0.2)
    qa_llm = ChatOllama(model="llama2", temperature=0)
    gen_prompt = f"""<System>
    You are an expert programmer.
    </System>

    Create code as a response to the Request. 
    Add a doc string to every function.
    Include type hints to every parameter and return value.
    Include comments on all executable lines of code to improve maintainability.
    Add a function names "setup" that includes calls to the primary function in the code (for example medical_tool).
    An example of the setup function is provided below:

    <Setup function example>
def setup(ToolManager):
    ToolManager.add(your_function_name)
    </Setup function example>

    <Request>
    {request}
    </Request>

    <Output Format>
    Only return the code. Do not include commentary.
    Make sure the code has correct indentation for the Python language.
    Add a main function that includes tests for the code.
    </Output Format>
    """
    qa_resp = "Failed"
    max_count = 10
    current_count = 0
    while ("--passed--" not in qa_resp.lower() and current_count < max_count):
        print(".", end="", flush=True)
        current_count += 1
        try:
            resp = code_llm.invoke(gen_prompt).content
        except:
            continue

        code_blocks = get_code_from_markdown(resp)
        code = "\n".join(code_blocks)
        try:
            formatted_code, _ = FormatCode(code, style_config='google')
            output = run_python_code_in_sandbox(formatted_code)
        except:
            continue
        p = f"""<System>
        You are an expert software quality assurance engineer.
        </System>

        Below is a Request from a user for code, the code that was generated, and the response from the code when it executes.
        Determine if the code satisfies the user's needs. The generated code should include code for testing the functionality.

        <Request>
        {request}
        </Request>

        <Generated Code>
        {formatted_code}
        </Generated Code>

        <Response>
        {output}
        </Response>

        <Output Format>
        Return "--Passed--" if the code is correct. Otherwise return "--Failed--".
        </Output Format>
        """
        try:
            qa_resp = qa_llm.invoke(p).content
            if "failed" in qa_resp.lower():
                print (f"""Failed: {qa_resp}""")
        except Exception as e:  
            print(e)
            qa_resp = "Failed"
    print("")
    return formatted_code if max_count >= current_count else None

def run_python_code_in_sandbox(code: str) -> str:
    python_sandbox = types.ModuleType('python_sandbox')

    f = StringIO()
    with redirect_stdout(f):
        code = f"__name__ = '__main__'\n{code}"
        exec(code, python_sandbox.__dict__)
    return f.getvalue()    
    

def save_file_tool(file_path: str, text: str, append: bool = False) -> str:
    """
    This tool is best for saving files to the local file system.
    """
    write_tool = WriteFileTool(root_dir='./sandbox')
    write_tool.invoke({"file_path": file_path, "text": text, "append": append})
    return "Saved file."


def load_file_tool(file_path: str) -> str:
    """
    This tool is best for loading files from the local file system.
    """
    read_tool = ReadFileTool(root_dir='./sandbox')
    content = read_tool.invoke({"file_path": file_path})
    return content


def execute_command_line_tool(command: str) -> str:
    """
    This tool is best for executing command line commands.
    """
    shell_tool = ShellTool()
    return shell_tool.run({"commands": [command]})


def execute_python_tool(code: str) -> str:
    """
    This tool is best for executing python code.
    """
    exec_python = PythonREPLTool()
    return exec_python.invoke(code)


def get_tools_from_repository(directory_path: str = "") -> dict:
    """
    This tool is best for retrieving python code from a repository.
    
    :param directory_path: The directory path in the repository from which to retrieve Python files.
    :return: A dictionary with file names as keys and their contents as values.
    """
    access_token = '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'  # Replace 'your_github_pat_here' with your actual GitHub PAT

    # Initialize the GitHub instance with your token for authentication
    g = Github(access_token)

    # Specify the correct repository name, ensuring it exists and is spelled correctly
    repo_name = "mattbab/tools"

    # Initialize the repository object
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        return {"error": f"Error accessing repository: {e}"}

    # Retrieve files from the specified directory
    try:
        contents = repo.get_contents(directory_path)
        files = {}
        for content_file in contents:
            if content_file.path.endswith('.py'):  # Filter for Python files
                file_content = content_file.decoded_content.decode("utf-8")
                module_docstring = ast.get_docstring(ast.parse(file_content))
                files[content_file.name] = (file_content, module_docstring)
        return files
    except Exception as e:
        return {"error": f"Error retrieving files: {e}"}


def save_code_to_repository_tool(tool_name: str, content: str,
                                 commit_msg: str) -> str:
    """
    This tool is best for saving python code to a repository.
    """
    # Assuming you have a GitHub access token for authentication
    access_token = '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'

    # Initialize the GitHub instance with your token for authentication
    g = Github(access_token)

    # Specify the correct repository name, ensuring it exists and is spelled correctly
    repo_name = "mattbab/tools"

    # Specify the branch name; ensure the branch exists in your repository
    branch_name = "main"

    # Initialize the repository object
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        return (f"Error accessing repository: {e}")

    # File details
    file_path = f"{tool_name}.py"  # Path where the file will be created in the repository
    file_content = content  # Content of the file
    commit_message = commit_msg  # Commit message

    # Check if the branch exists
    try:
        repo.get_branch(branch_name)
    except Exception as e:
        return (f"Branch '{branch_name}' not found: {e}")

    # Create or update the file
    try:
        # Check if the file already exists
        try:
            contents = repo.get_contents(file_path, ref=branch_name)
            # If the file exists, update it
            repo.update_file(contents.path,
                             commit_message,
                             file_content,
                             contents.sha,
                             branch=branch_name)
            ret = (f"File '{file_path}' updated in branch '{branch_name}'.")
        except:
            # If the file does not exist, create it
            repo.create_file(file_path,
                             commit_message,
                             file_content,
                             branch=branch_name)
            ret = (f"File '{file_path}' created in branch '{branch_name}'.")
        load_dynamic_code_as_a_module(content, tools)
        return ret
    except Exception as e:
        return (f"Error creating/updating file: {e}")


def load_dynamic_code_as_a_module(code: str, tools):
    dynamic_module = types.ModuleType('dynamic_module')

    # Execute the module code within the dynamic_module's namespace
    exec(code, dynamic_module.__dict__)
    if "setup" in dynamic_module.__dict__:
        dynamic_module.setup(tools)

def create_tool(description: str, tool_name:str)-> str:
    """
    This tool is best for creating a new tool.
    """
    code = generate_code(description)
    return save_code_to_repository_tool(tool_name, code, "initial load")

def main():
    # print(save_file_tool("test.txt", "Hello World!", True))
    # print(load_file_tool("test.txt"))
    # print(execute_command_line_tool("echo Hello World!")
    # print(execute_python_tool())
    # print(save_code_to_repository_tool("test1", "print('Hello World!')", "main"))
    # Example usage
    # print(get_tools_from_repository())
    # Example usage
    # print(update_or_clone_repository("."))
    # load_tools()
    # exit()

    code = generate_code(
        # """Write a python function that accepts a string and returns:
        #                  the number of characters, 
        #                  words, 
        #                  sentences 
        #                  and paragraphs in the string.
                         
        #                  """)
        # """ Write a python function named human that displays a string provided to it and requires the user to type a response.
        # The response should be returned from the function.
        # """)
        """ Write a python function that returns the current time.
        """)
    if not code:
        print("Failed to generate code.")
        return
    print(code)
    print(run_python_code_in_sandbox(code))

    # print(run_python_code_in_sandbox('print("Hello World!")'))

if __name__ == "__main__":
    main()
