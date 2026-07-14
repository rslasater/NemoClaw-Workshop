from pathlib import Path

from atas_generator.generator import generate_thread, merge_mailbox
from atas_generator.providers import MockProvider
from atas_generator.scenario import Scenario


def test_mock_generation_and_partial_merge(tmp_path: Path):
    scenario = Scenario.load(Path("scenario"))
    messages = scenario.thread_messages("ATAS-001")
    generate_thread(scenario, "ATAS-001", MockProvider(messages), tmp_path)
    result = merge_mailbox(scenario, tmp_path, tmp_path / "emails.json", allow_incomplete=True)
    assert result["message_count"] == 4
    assert (tmp_path / "emails.json").exists()
