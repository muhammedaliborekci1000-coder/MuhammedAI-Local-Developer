from app.ai.developer_agent import DeveloperAgent


def main():
    agent = DeveloperAgent()

    print("=" * 70)
    print("MUHAMMED AI LOCAL DEVELOPER")
    print("=" * 70)

    print("\n[1] DOSYA ANALİZİ BAŞLIYOR...\n")

    response = agent.analyze_file(
        "agents/research_agent.py"
    )

    print(response)


if __name__ == "__main__":
    main()