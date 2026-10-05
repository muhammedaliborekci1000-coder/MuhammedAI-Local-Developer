from app.tools.file_reader import FileReader


def main():
    reader = FileReader()

    content = reader.read("agents/base_agent.py")

    print("=" * 60)
    print("DOSYA OKUNDU: agents/base_agent.py")
    print("=" * 60)
    print(content)


if __name__ == "__main__":
    main()