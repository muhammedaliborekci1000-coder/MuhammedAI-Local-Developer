from app.tools.project_scanner import ProjectScanner


def main():
    scanner = ProjectScanner()

    print(scanner.get_tree())


if __name__ == "__main__":
    main()