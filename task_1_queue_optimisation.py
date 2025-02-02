from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(
    print_jobs: List[PrintJob], constraints: PrinterConstraints
) -> Dict:
    """ "
    This function optimizes the printing process based on the given print jobs and printer constraints.

    Args:
        print_jobs (List[PrintJob]): A list of print jobs.
        constraints (PrinterConstraints): A printer constraints object.

    Returns:
        Dict: A dictionary containing the optimized print order and total time.
    """

    optimized_results = {"print_order": list(), "total_time": 0}

    print_jobs.sort(key=lambda x: x["priority"])

    concurrent_job_ids = []
    concurrent_volume = 0

    for i, job in enumerate(print_jobs):
        if job["volume"] <= constraints["max_volume"]:
            if (
                concurrent_volume + job["volume"] > constraints["max_volume"]
                or (len(concurrent_job_ids) + 1) > constraints["max_items"]
            ):
                # add accumulated data to resulting object
                optimized_results["print_order"].extend(concurrent_job_ids)
                optimized_results["total_time"] += max(
                    [
                        job["print_time"]
                        for job in print_jobs
                        if job["id"] in concurrent_job_ids
                    ]
                )

                # reset previous concurrent values with current job data
                concurrent_job_ids = [job["id"]]
                concurrent_volume = job["volume"]
            else:
                # add accumulated data to resulting object
                concurrent_job_ids.append(job["id"])
                concurrent_volume += job["volume"]

    # add rest of the data
    optimized_results["print_order"].extend(concurrent_job_ids)
    optimized_results["total_time"] += max(
        [job["print_time"] for job in print_jobs if job["id"] in concurrent_job_ids]
    )

    return optimized_results


# testing
def test_printing_optimization():
    # test 1: models with the same priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    # test 2: models with different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # homework
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # diplom project
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150,
        },  # personal project
    ]

    # test 3: models that exceed the max_volume constraint
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("-" * 100)
    print("Test 1 - equal priorities:")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("-" * 100)
    print("Test 2 - different priorities:")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("-" * 100)
    print("Test 3 - exceed max_volume:")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")
    print("-" * 100)


if __name__ == "__main__":
    test_printing_optimization()
