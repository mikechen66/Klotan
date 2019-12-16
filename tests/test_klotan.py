import klotan.criteria as criteria
import klotan.match as match
import klotan.store as store

import json


def test_that_match_simple_dict():
    pattern = {"a": criteria.equals(3) | criteria.equals(4)}
    tree = {"a": 3}
    tree2 = {"a": 4}
    assert match.match(pattern, tree).is_valid()
    assert match.match(pattern, tree2).is_valid()


def testi_match2():
    pattern = {
        "between_1_and_5": criteria.more(1, eq=True) & criteria.less(5),
        "between_1_and_5_auto": criteria.between(1, 5),
    }
    tree1 = {"between_1_and_5": 2, "between_1_and_5_auto": 3}
    assert match.match(pattern, tree1).is_valid()


def test_json():
    js = ""
    with open("tests/payload.json") as payload:
        js = json.loads(payload.read())
    name_criteria = criteria.is_type(str) & ~criteria.empty()
    status = store.ValueStorage()
    modules_status = store.ListStorage()
    HEALTH_MODELS = {
        "version": criteria.regex(r"(\d+).(\d+)"),
        "status": criteria.is_in("UP", "DEGRADED", "DOWN") >> status,
        "comment": criteria.is_type(str),
        "az": [
            {
                "name": name_criteria,
                "status": criteria.is_in("UP", "DEGRADED", "DOWN"),
                "comment": criteria.is_type(str),
            }
        ],
        "modules": [
            {
                "name": name_criteria,
                "status": criteria.is_in("UP", "DEGRADED", "DOWN") >> modules_status,
                "comment": criteria.is_type(str),
                "az": [
                    {
                        "name": name_criteria,
                        "status": criteria.is_in("UP", "DEGRADED", "DOWN"),
                        "comment": criteria.is_type(str),
                    },
                ],
            },
        ],
    }
    res = match.match(HEALTH_MODELS, js)
    print("PAYLOAD =")
    print(res.to_string())
    print("Status :", status.value)
    for stat in modules_status.values:
        print(stat.value)
        assert stat.value == "UP"
    assert res.is_valid()
