from pathlib import Path

from atas_generator.generator import export_api_seed, generate_thread, merge_mailbox
from atas_generator.io import read_json
from atas_generator.providers import MockProvider
from atas_generator.scenario import Scenario

SCENARIO_DIR = Path(__file__).resolve().parents[1] / "scenario"


def test_mock_generation_and_partial_merge(tmp_path: Path):
    scenario = Scenario.load(SCENARIO_DIR)
    messages = scenario.thread_messages("ATAS-001")
    generate_thread(scenario, "ATAS-001", MockProvider(messages), tmp_path)
    result = merge_mailbox(scenario, tmp_path, tmp_path / "emails.json", allow_incomplete=True)
    assert result["message_count"] == 4
    assert (tmp_path / "emails.json").exists()

    api_seed = export_api_seed(scenario, tmp_path, tmp_path / "api-seed.json", allow_incomplete=True)
    assert api_seed["message_count"] == 4
    assert (tmp_path / "api-seed.json").exists()

    api_messages = read_json(tmp_path / "api-seed.json")
    assert all(message["id"].startswith("msg_") for message in api_messages)
    assert all("conversation_id" not in message["metadata"] for message in api_messages)
    assert all("thread_index" not in message["metadata"] for message in api_messages)
