from pathlib import Path

from novel_authoring.db.database import Database
from novel_authoring.progression.models import (
    ContractStatus,
    ExperiencePriority,
    PrimaryFamily,
    ReaderExperience,
    ReaderExperienceContract,
    SettingSkin,
)
from novel_authoring.progression.service import (
    ProgressionContractType,
    confirm_contract,
    create_contract_proposal,
    effective_contract_records,
)


def database_with_book(path: Path) -> Database:
    database = Database(path)
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO books(
                book_id, title, mode, source_root, workspace_root,
                created_at, updated_at
            ) VALUES ('contract-book', '合同测试', 'CONSTRAINED_INNOVATION', '', '', 'now', 'now')
            """
        )
    return database


def reader_contract() -> ReaderExperienceContract:
    return ReaderExperienceContract(
        contract_id="reader-contract",
        primary_family=PrimaryFamily.PROGRESSION_FANTASY,
        setting_skin=SettingSkin.NEAR_FUTURE,
        experience_priorities={
            ReaderExperience.PROGRESSION: ExperiencePriority.VERY_HIGH,
            ReaderExperience.WORLD_EXPANSION: ExperiencePriority.HIGH,
        },
        growth_centrality=ExperiencePriority.VERY_HIGH,
        world_expansion_centrality=ExperiencePriority.HIGH,
        mystery_centrality=ExperiencePriority.MEDIUM,
        team_centrality=ExperiencePriority.LOW,
        relationship_centrality=ExperiencePriority.MEDIUM,
        theme_centrality=ExperiencePriority.LOW,
        must_deliver=["成长持续改变行动可能性"],
        status=ContractStatus.NEEDS_REVIEW,
    )


def test_contract_proposal_requires_explicit_confirmation(tmp_path: Path) -> None:
    database = database_with_book(tmp_path / "contract.sqlite3")
    before = {
        "events": database.scalar("SELECT COUNT(*) FROM events"),
        "canon_commits": database.scalar("SELECT COUNT(*) FROM canon_commits"),
    }
    proposal = create_contract_proposal(
        database,
        book_id="contract-book",
        edition_id="base",
        contract_type=ProgressionContractType.READER_EXPERIENCE,
        payload=reader_contract(),
        source="ORIGINAL_READER_EXPERIENCE",
    )

    assert proposal.status is ContractStatus.NEEDS_REVIEW
    assert effective_contract_records(database, book_id="contract-book") == {}
    assert database.scalar("SELECT COUNT(*) FROM events") == before["events"]
    assert database.scalar("SELECT COUNT(*) FROM canon_commits") == before["canon_commits"]

    confirmed = confirm_contract(
        database,
        proposal.contract_record_id,
        effective_from_boundary=4,
    )
    assert confirmed.status is ContractStatus.EFFECTIVE
    assert confirmed.effective_from_boundary == 4
    assert confirmed.payload["status"] == "EFFECTIVE"
    assert database.scalar("SELECT COUNT(*) FROM events") == before["events"]
    assert database.scalar("SELECT COUNT(*) FROM canon_commits") == before["canon_commits"]
