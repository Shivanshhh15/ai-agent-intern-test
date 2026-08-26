from app.agent import SupportAgent


def make_agent(results):
    agent = SupportAgent.__new__(SupportAgent)

    class FakeRetriever:
        def search(self, question, n_results=5):
            return results

    agent.retriever = FakeRetriever()
    return agent


def test_return_policy_prioritizes_current_policy():
    results = [
        {
            "text": "Aster & Row bags and backpacks: 2 years.",
            "metadata": {
                "filename": "07-warranty.md",
                "heading": "Warranty periods",
            },
            "distance": 0.9,
        },
        {
            "text": (
                "Customers on the standard plan may request "
                "a return within 30 calendar days of delivery."
            ),
            "metadata": {
                "filename": "01-returns-policy-current.md",
                "heading": "Standard return window",
            },
            "distance": 1.1,
        },
    ]

    agent = make_agent(results)

    response = agent.answer(
        "How long do I have to return an unused backpack?"
    )

    assert "30 calendar days" in response["answer"]
    assert (
        response["sources"][0]["filename"]
        == "01-returns-policy-current.md"
    )


def test_shipping_policy_is_selected():
    results = [
        {
            "text": "Some unrelated information.",
            "metadata": {
                "filename": "07-warranty.md",
                "heading": "Warranty periods",
            },
            "distance": 0.8,
        },
        {
            "text": (
                "Aster & Row currently ships internationally "
                "only to Canada."
            ),
            "metadata": {
                "filename": "06-international-shipping.md",
                "heading": "Supported destinations",
            },
            "distance": 1.0,
        },
    ]

    agent = make_agent(results)

    response = agent.answer("Do you ship to Canada?")

    assert "Canada" in response["answer"]
    assert (
        response["sources"][0]["filename"]
        == "06-international-shipping.md"
    )


def test_warranty_policy_is_selected():
    results = [
        {
            "text": (
                "Aster & Row bags and backpacks: "
                "2 years from the purchase date."
            ),
            "metadata": {
                "filename": "07-warranty.md",
                "heading": "Warranty periods",
            },
            "distance": 1.0,
        }
    ]

    agent = make_agent(results)

    response = agent.answer("What is the warranty period?")

    assert "2 years" in response["answer"]
    assert (
        response["sources"][0]["filename"]
        == "07-warranty.md"
    )


def test_unknown_question_abstains_when_no_results():
    agent = make_agent([])

    response = agent.answer(
        "What is the CEO's favorite food?"
    )

    assert (
        response["answer"]
        == "I couldn't find a relevant answer "
        "in the knowledge base."
    )
    assert response["sources"] == []
    assert response["confidence"] == 0.0


def test_low_confidence_result_is_rejected():
    results = [
        {
            "text": "Unrelated knowledge-base content.",
            "metadata": {
                "filename": "random.md",
                "heading": "Random",
            },
            "distance": 1.8,
        }
    ]

    agent = make_agent(results)

    response = agent.answer(
        "What is the CEO's favorite food?"
    )

    assert (
        "couldn't find a reliable answer"
        in response["answer"]
    )
    assert response["sources"] == []
    assert response["confidence"] == 0.0