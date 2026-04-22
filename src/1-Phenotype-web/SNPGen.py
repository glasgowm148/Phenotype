import requests

from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
SNPEDIA_API_URL = "https://bots.snpedia.com/api.php"

class GrabSNPs:
    """GrabSNPs(crawllimit, target, snpofinterest) ->
    crawls and attains a list of SNPedia compatible SNPs found within the snps of interest array
    """

    def __init__(self, crawllimit=5000, snpsofinterest=None, target=50):
        self.cmcontinue = ""
        self.snps = []
        self.limit = crawllimit
        self.target = target
        if self.lastsessionexists():
            cmcontinue = self.importlast()
        else:
            cmcontinue = None

        if snpsofinterest:
            self.crawl(snpsofinterest=snpsofinterest, cmcontinue=cmcontinue, target=target)
        else:
            self.crawl(target=target, cmcontinue=cmcontinue)
        self.export()


    def crawl(self, snpsofinterest=None, cmcontinue=None, target=100):
        snpsofinterest = {snp.lower() for snp in snpsofinterest or []}
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
            jd = response.json()

            members = [item["title"] for item in jd.get("query", {}).get("categorymembers", [])]
            if snpsofinterest:
                members = [snp for snp in members if snp.lower() in snpsofinterest]
            self.snps.extend(members)

            continuation = jd.get("continue", {})
            cmcontinue = continuation.get("cmcontinue")
            if len(self.snps) >= target or not cmcontinue:
                break

            params["cmcontinue"] = cmcontinue
            params["continue"] = continuation.get("continue", "")
            count += 1

        if snpsofinterest:
            print(len(self.snps))

        self.cmcontinue = cmcontinue or ""

    def lastsessionexists(self):
        filepath = DATA_DIR / 'last_session.txt'
        return filepath.is_file()

    def importlast(self):
        filepath = DATA_DIR / 'last_session.txt'
        lines = filepath.read_text(encoding="utf-8").splitlines()
        lastsessionvalue = lines[0] if lines else ""
        print("Last Session Value")
        print(lastsessionvalue)
        return lastsessionvalue or None

    def export(self):
        DATA_DIR.mkdir(exist_ok=True)
        filepath = DATA_DIR / 'last_session.txt'
        filepath.write_text(self.cmcontinue, encoding="utf-8")



