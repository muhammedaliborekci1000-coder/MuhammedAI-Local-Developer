from app.tools.code_search import CodeSearch


def main():
    searcher = CodeSearch()

    results = searcher.search("AgentExecutor")

    print("=" * 60)
    print("CODE SEARCH")
    print("=" * 60)

    print(searcher.format_results(results))


if __name__ == "__main__":
    main()