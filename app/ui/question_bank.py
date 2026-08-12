"""
question_bank.py

Centralized question bank for the Olist AI Analytics Assistant.

The UI should import questions from this module instead of
hardcoding questions directly inside the Streamlit application.
"""

from typing import Dict, List


QUESTION_BANK: Dict[str, List[str]] = {

    "Sales & Revenue": [
        "What is the total revenue generated?",
        "What are the top 10 product categories by revenue?",
        "Which product categories generated the least revenue?",
        "What is the average order value?",
        "What is the average order item price?",
        "Which sellers generated the highest revenue?",
        "What are the top 10 sellers by revenue?",
        "What is the total freight cost?",
        "What is the total product sales value?",
        "What are the monthly sales for 2018?",
        "How much revenue was generated in each year?",
        "Which month had the highest revenue?",
        "Which product categories have revenue above 100000?",
        "What percentage of orders were canceled?",
    ],

    "Customers": [
        "How many unique customers have placed orders?",
        "How many customers are there in each state?",
        "Which states have the most customers?",
        "What is the average order value for each customer state?",
        "Which customer states generated the most revenue?",
        "How many orders does each customer have?",
        "Who are the customers with the highest number of orders?",
        "What is the average number of orders per customer?",
        "Which cities have the most customers?",
        "How many unique customers placed orders in 2018?",
    ],

    "Products": [
        "How many products are in each category?",
        "What are the top 10 product categories by number of products?",
        "Which product categories have the most products?",
        "Which product categories have the fewest products?",
        "What is the average product weight by category?",
        "What is the average number of photos per product category?",
        "Which product categories have the highest average product price?",
        "What are the most expensive product categories?",
        "Which products have the highest freight cost?",
        "How many products belong to each category?",
    ],

    "Sellers": [
        "How many sellers are there?",
        "How many sellers are there in each state?",
        "Which states have the most sellers?",
        "Which sellers generated the highest revenue?",
        "What are the top 10 sellers by revenue?",
        "Which sellers generated more than 10000 in revenue?",
        "What is the average revenue per seller?",
        "Which sellers sold the most items?",
        "Which seller states generated the most revenue?",
        "Which cities have the most sellers?",
    ],

    "Orders": [
        "How many orders were placed?",
        "How many orders were placed in 2017?",
        "How many orders were placed in 2018?",
        "How many orders were placed in each year?",
        "How many orders were placed in each month of 2018?",
        "What is the distribution of order statuses?",
        "How many orders were delivered?",
        "How many orders were canceled?",
        "What percentage of orders were delivered?",
        "Which customer states placed the most orders?",
        "Which month had the highest number of orders?",
        "How many orders were approved?",
    ],

    "Reviews": [
        "What is the average review score?",
        "What is the distribution of review scores?",
        "How many reviews received a score of 5?",
        "How many reviews received a score of 1?",
        "What is the average review score for each customer state?",
        "What is the average review score for each order status?",
        "Which customer states have the highest average review score?",
        "Which customer states have the lowest average review score?",
        "How many reviews were submitted for each score?",
        "What percentage of reviews received a score of 5?",
    ],

    "Payments": [
        "Which payment type was used most often?",
        "What is the distribution of payment types?",
        "How much was paid using each payment type?",
        "What is the average payment value for each payment type?",
        "Which payment type generated the highest payment value?",
        "What is the average number of installments?",
        "Which payment type has the highest average installments?",
        "How many payments were made using credit cards?",
        "How many payments were made using vouchers?",
        "What is the total payment value?",
    ],

    "Delivery & Logistics": [
        "What is the average delivery time?",
        "What is the average delivery time by customer state?",
        "Which customer states have the longest delivery time?",
        "Which customer states have the shortest delivery time?",
        "What is the average time between purchase and carrier delivery?",
        "What is the average time between carrier delivery and customer delivery?",
        "Which orders took the longest to deliver?",
        "How many orders were delivered after the estimated delivery date?",
        "What percentage of orders were delivered on time?",
    ],

    "Geography": [
        "Which customer states have the most orders?",
        "Which customer states generated the most revenue?",
        "Which customer states have the highest average order value?",
        "Which seller states have the most sellers?",
        "Which seller states generated the most revenue?",
        "Which cities have the most customers?",
        "Which cities have the most sellers?",
        "What is the revenue by customer state?",
        "What is the order count by customer state?",
    ],

    "Advanced Analysis": [
        "What are the top 10 product categories by revenue?",
        "Which sellers generated the highest revenue?",
        "What is the average review score for each customer state?",
        "What is the revenue trend by year?",
        "What is the monthly order trend for 2018?",
        "Which customer states have both high order volume and high revenue?",
        "Which product categories have high revenue but few products?",
        "Which sellers have high revenue and high order volume?",
        "What are the top 10 categories by average order item price?",
        "Which payment types have the highest average payment value?",
    ],
}


def get_categories() -> List[str]:
    """
    Return all available question categories.
    """
    return list(QUESTION_BANK.keys())


def get_questions(category: str) -> List[str]:
    """
    Return questions belonging to a category.
    """
    return QUESTION_BANK.get(category, [])


def get_all_questions() -> List[str]:
    """
    Return every question in the question bank.
    """
    questions = []

    for category_questions in QUESTION_BANK.values():
        questions.extend(category_questions)

    return questions


def get_question_count() -> int:
    """
    Return the total number of available questions.
    """
    return len(get_all_questions())


if __name__ == "__main__":

    print("=" * 70)
    print("OLIST AI ANALYTICS — QUESTION BANK")
    print("=" * 70)

    for category, questions in QUESTION_BANK.items():

        print(f"\n{category}")
        print("-" * len(category))

        for question in questions:
            print(f"  • {question}")

    print("\n" + "=" * 70)
    print(f"TOTAL QUESTIONS: {get_question_count()}")
    print("=" * 70)