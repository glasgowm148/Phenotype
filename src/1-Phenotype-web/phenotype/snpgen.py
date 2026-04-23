from __future__ import annotations

from pathlib import Path

import requests

from phenotype.paths import DATA_DIR

SNPEDIA_API_URL = "https://bots.snpedia.com/api.php"


class GrabSNPs:
    def __init__(self, crawllimit: int = 5000, snpsofinterest: list[str] | None = None, target: int = 50):
        self.cmcontinue = self.importlast() if self.lastsessionexists() else None
        self.snps: list[str] = []
        self.limit = crawllimit
        self.target = target
        self.crawl(snpsofinterest=snpsofinterest, cmcontinue=self.cmcontinue, target=target)
        self.export()

    def crawl(self, snpsofinterest: list[str] | None = None, cmcontinue: str | None = None, target: int = 100) -> None:
        snpsofinterest_set = {snp.lower() for snp in snpsofinterest or []}
        count = 0
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": "Category:is_a_snp",
            "cmlimit": "500",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        while count <= self.limit:
            response = requests.get(SNPEDIA_API_URL, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()
            members = [item["title"] for item in payload.get("query", {}).get("categorymembers", [])]
            if snpsofinterest_set:
                members = [snp for snp in members if snp.lower() in snpsofinterest_set]
            self.snps.extend(members)

            continuation = payload.get("continue", {})
            cmcontinue = continuation.get("cmcontinue")
            if len(self.snps) >= target or not cmcontinue:
                break
            params["cmcontinue"] = cmcontinue
            params["continue"] = continuation.get("continue", "")
            count += 1

        self.cmcontinue = cmcontinue

    def lastsessionexists(self) -> bool:
        return _last_session_path().is_file()

    def importlast(self) -> str | None:
        lines = _last_session_path().read_text(encoding="utf-8").splitlines()
        return lines[0] if lines else None

    def export(self) -> None:
        _last_session_path().parent.mkdir(exist_ok=True)
        _last_session_path().write_text(self.cmcontinue or "", encoding="utf-8")


def _last_session_path() -> Path:
    return DATA_DIR / "last_session.txt"

