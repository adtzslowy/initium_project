from initium.app import InitiumApp

def main():
    app = InitiumApp()
    tools = app.list_tools()

    print("Available tools:\n")
    for i, key in enumerate(tools, start=1):
        info = app.get_tool_info(key)
        print(f"{i}. {info['name']}-{info['description']}")

    choice = input("\nSelect tool number to install: ")

    try:
        index = int(choice) - 1
        tool_key = tools[index]
    except (ValueError, IndexError):
        print("Invalid selection")
        return

    print(f"\nInstalling {tool_key}... \n")
    success = app.install_tool(tool_key)

    if success:
        print("Installation complete successfully")
    else:
        print("Installation failed")


if __name__ == "__main__":
    main()
