from typing import Dict, List
from colorama import Fore, init, Style

init()


# function for finding optimal solution with memo
def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    # raise an error if the input data is invalid
    if (
        length <= 0
        or len(prices) == 0
        or len(prices) != length
        or any(price <= 0 for price in prices)
    ):
        raise ValueError("Invalid input")

    # memoization
    memo = {}

    # function for finding optimal solution with memo
    def _rod_cutting_memo(length: int):
        if length == 0:
            return 0, []
        if length in memo:
            return memo[length]

        max_profit = 0
        best_cuts = []

        for i in range(1, length + 1):
            if i <= len(prices):
                profit, cuts = _rod_cutting_memo(length - i)
                profit += prices[i - 1]

                if profit > max_profit:
                    max_profit = profit
                    best_cuts = cuts + [i]

        memo[length] = (max_profit, best_cuts)
        return memo[length]

    max_profit, best_cuts = _rod_cutting_memo(length)
    return {
        "max_profit": max_profit,
        "cuts": best_cuts,
        "number_of_cuts": len(best_cuts) - 1,
    }


# function for finding optimal solution with tabulation
def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    # raise an error if the input data is invalid
    if (
        length <= 0
        or len(prices) == 0
        or len(prices) != length
        or any(price <= 0 for price in prices)
    ):
        raise ValueError("Invalid input")

    # table to store results
    profit_table = [0] * (length + 1)
    cuts_table = [[] for _ in range(length + 1)]

    # fill table with results
    for n in range(1, length + 1):
        for i in range(1, n + 1):
            if i <= len(prices):
                new_profit = profit_table[n - i] + prices[i - 1]
                if new_profit > profit_table[n]:
                    profit_table[n] = new_profit
                    cuts_table[n] = cuts_table[n - i] + [i]

    return {
        "max_profit": profit_table[length],
        "cuts": cuts_table[length],
        "number_of_cuts": len(cuts_table[length]) - 1,
    }


# function for running tests
def run_tests():
    test_cases = [
        # Test 1: Base case
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Base case"},
        # Тест 2: Optimal not to cut
        {"length": 3, "prices": [1, 3, 8], "name": "Optimal not to cut"},
        # Тест 3: All cuts are equal to 1
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Equal cuts"},
    ]

    for test in test_cases:
        print("\n" + "-" * 100)
        print(f"\nTest: {test['name']}")
        print(f"Rod length: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print(Fore.BLUE + "\nMemoisation result:" + Style.RESET_ALL)
        print(f"Maximum profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of cuts: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test["length"], test["prices"])
        print(Fore.BLUE + "\nTabulation result:" + Style.RESET_ALL)
        print(f"Maximum profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of cuts: {table_result['number_of_cuts']}")

        print(Fore.YELLOW + "\nTest completed successfully." + Style.RESET_ALL)


if __name__ == "__main__":
    run_tests()
