from app.agent import SupportAgent


def main():

    agent = SupportAgent()

    questions = [
      "How long do I have to return an unused backpack?",
      "Do you ship to Canada?",
      "What is the warranty period?",
      "What is the CEO's favorite food?",
      ]

    for question in questions:

        print("\n" + "=" * 70)
        print("QUESTION:", question)
        print("=" * 70)

        result = agent.answer(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCE:")

        for source in result["sources"]:
            print(
                f"- {source['filename']} "
                f"| {source['heading']}"
            )


if __name__ == "__main__":
    main()