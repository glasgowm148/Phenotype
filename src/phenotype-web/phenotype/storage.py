from __future__ import annotations

import csv
import json
import re
import sqlite3
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from phenotype.models import (
    CLINICAL_SEVERITY_RULES,
    SNPRecord,
    normalize_clinical_significance,
    normalize_frequency_percent,
    normalize_risk_allele,
    normalize_rsid,
)
from phenotype.paths import DEFAULT_DB_PATH, DEFAULT_GENOTYPES_JSON, DEFAULT_SCRAPED_JSON
from phenotype.storage_helpers import (
    CLINVAR_INSERT_SQL,
    VEP_INSERT_SQL,
    _chunks,
    _classification_hash,
    _classification_source_date,
    _clinvar_insert_tuple,
    _clinvar_rows_to_records,
    _enrich_cached_snpedia_summary,
    _finding_freshness,
    _load_paged_rows,
    _merge_record_update,
    _severity_count_clause,
    _severity_search_clause,
    _unannotated_row,
    _unannotated_variant_row,
    _variant_metadata,
    _vep_best_impact,
    _vep_insert_tuple,
    utc_now,
)


class PhenotypeStore:
    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                create table if not exists snps (
                    rsid text primary key,
                    description text not null default '',
                    clinvar_json text not null default '[]',
                    clinical_significance_json text not null default '[]',
                    frequency text not null default '',
                    studies text not null default '',
                    citations text not null default '',
                    gene text not null default '',
                    risk text not null default '',
                    risk_allele text not null default '',
                    frequency_percent real,
                    variations_json text not null default '[]',
                    source_urls_json text not null default '{}',
                    first_seen_at text not null,
                    classification_hash text not null default '',
                    classification_updated_at text not null,
                    source_updated_at text not null
                );
                create index if not exists idx_snps_finding_candidates
                    on snps(rsid)
                    where variations_json != '[]'
                       or (risk_allele != '' and clinical_significance_json != '[]');
                create index if not exists idx_snps_gene_lower on snps(lower(gene));
                create index if not exists idx_snps_frequency_percent on snps(frequency_percent);
                create index if not exists idx_snps_classification_updated_at on snps(classification_updated_at);
                create index if not exists idx_snps_citations on snps(citations);
                create table if not exists genotypes (
                    rsid text primary key,
                    genotype text not null,
                    imported_at text not null
                );
                create index if not exists idx_genotypes_imported_at on genotypes(imported_at);
                create table if not exists genotype_variants (
                    rsid text primary key,
                    chromosome text not null default '',
                    position integer,
                    genotype text not null,
                    allele_a text not null default '',
                    allele_b text not null default '',
                    zygosity text not null default '',
                    assembly text not null default '',
                    annotation_release text not null default '',
                    imported_at text not null
                );
                create index if not exists idx_genotype_variants_zygosity on genotype_variants(zygosity);
                create index if not exists idx_genotype_variants_location
                    on genotype_variants(chromosome, position);
                create index if not exists idx_genotype_variants_imported_at on genotype_variants(imported_at);
                create table if not exists vep_consequences (
                    rsid text not null,
                    uploaded_variation text not null default '',
                    location text not null default '',
                    allele text not null default '',
                    gene text not null default '',
                    feature text not null default '',
                    feature_type text not null default '',
                    consequence text not null default '',
                    impact text not null default '',
                    symbol text not null default '',
                    hgvsc text not null default '',
                    hgvsp text not null default '',
                    existing_variation text not null default '',
                    extra_json text not null default '{}',
                    imported_at text not null,
                    primary key (
                        rsid, uploaded_variation, allele, gene, feature, consequence, hgvsc, hgvsp
                    )
                );
                create index if not exists idx_vep_consequences_rsid on vep_consequences(rsid);
                create index if not exists idx_vep_consequences_impact on vep_consequences(impact);
                create index if not exists idx_vep_consequences_consequence on vep_consequences(consequence);
                create index if not exists idx_vep_consequences_symbol on vep_consequences(symbol);
                create table if not exists scrape_runs (
                    id integer primary key autoincrement,
                    status text not null,
                    total integer not null default 0,
                    completed integer not null default 0,
                    failed integer not null default 0,
                    message text not null default '',
                    started_at text not null,
                    ended_at text,
                    requested_status text
                );
                create table if not exists scrape_run_items (
                    run_id integer not null,
                    rsid text not null,
                    status text not null default 'pending',
                    message text not null default '',
                    updated_at text not null,
                    primary key (run_id, rsid),
                    foreign key (run_id) references scrape_runs(id)
                );
                create table if not exists clinvar_variants (
                    rsid text not null,
                    allele_id text not null default '',
                    variation_id text not null default '',
                    type text not null default '',
                    name text not null default '',
                    gene text not null default '',
                    clinical_significance text not null default '',
                    clinsig_simple integer not null default 0,
                    last_evaluated text not null default '',
                    rcv_accession text not null default '',
                    phenotype_list text not null default '',
                    review_status text not null default '',
                    assembly text not null default '',
                    reference_allele text not null default '',
                    alternate_allele text not null default '',
                    source_updated_at text not null default '',
                    primary key (
                        rsid, allele_id, variation_id, assembly, clinical_significance,
                        phenotype_list, reference_allele, alternate_allele
                    )
                );
                create index if not exists idx_clinvar_variants_rsid on clinvar_variants(rsid);
                create index if not exists idx_clinvar_variants_rsid_significance
                    on clinvar_variants(rsid, clinical_significance);
                create index if not exists idx_clinvar_variants_significance
                    on clinvar_variants(clinical_significance);
                create table if not exists reference_stats (
                    key text primary key,
                    value integer not null default 0,
                    updated_at text not null default ''
                );
                create table if not exists summary_counts_cache (
                    key text primary key,
                    payload_json text not null default '{}',
                    updated_at text not null default ''
                );
                """
            )
            self._ensure_column(conn, "snps", "clinical_significance_json", "text not null default '[]'")
            self._ensure_column(conn, "snps", "source_urls_json", "text not null default '{}'")
            self._ensure_column(conn, "snps", "risk_allele", "text not null default ''")
            self._ensure_column(conn, "snps", "frequency_percent", "real")
            self._ensure_column(conn, "snps", "first_seen_at", "text not null default ''")
            self._ensure_column(conn, "snps", "classification_hash", "text not null default ''")
            self._ensure_column(conn, "snps", "classification_updated_at", "text not null default ''")
            self._ensure_column(conn, "scrape_runs", "requested_status", "text")
            try:
                self._backfill_normalized_fields(conn)
                self._backfill_metadata(conn)
            except sqlite3.OperationalError as exc:
                if "readonly" not in str(exc).lower():
                    raise

    def mark_interrupted_runs(self) -> None:
        now = utc_now()
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    update scrape_runs
                    set status='failed', requested_status=null, message='interrupted on app restart', ended_at=?
                    where status='running'
                    """,
                    [now],
                )
                conn.execute(
                    """
                    update scrape_run_items
                    set status='failed', message='interrupted on app restart', updated_at=?
                    where status='running'
                    """,
                    [now],
                )
        except sqlite3.OperationalError as exc:
            if "readonly" not in str(exc).lower():
                raise

    def _ensure_column(self, conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        columns = {row["name"] for row in conn.execute(f"pragma table_info({table})")}
        if column not in columns:
            conn.execute(f"alter table {table} add column {column} {definition}")

    def _backfill_normalized_fields(self, conn: sqlite3.Connection) -> None:
        rows = conn.execute(
            """
            select rsid, clinvar_json, risk, frequency
            from snps
            where (clinvar_json != '[]' and clinical_significance_json = '[]')
               or (risk != '' and risk_allele = '')
               or (
                    frequency != ''
                    and (frequency_percent is null or frequency_percent <= 0 or frequency_percent > 100)
               )
            """
        ).fetchall()
        conn.executemany(
            """
            update snps
            set clinical_significance_json = ?,
                risk_allele = coalesce(nullif(risk_allele, ''), ?),
                frequency_percent = case
                    when frequency_percent is null or frequency_percent <= 0 or frequency_percent > 100 then ?
                    else frequency_percent
                end
            where rsid = ?
            """,
            [
                (
                    json.dumps(normalize_clinical_significance(json.loads(row["clinvar_json"] or "[]"))),
                    normalize_risk_allele(row["risk"]),
                    normalize_frequency_percent(row["frequency"]),
                    row["rsid"],
                )
                for row in rows
            ],
        )

    def _backfill_metadata(self, conn: sqlite3.Connection) -> None:
        rows = conn.execute(
            """
            select rsid, clinvar_json, clinical_significance_json, source_updated_at,
                   first_seen_at, classification_hash, classification_updated_at
            from snps
            where first_seen_at = ''
               or classification_hash = ''
               or classification_updated_at = ''
               or classification_updated_at = source_updated_at
            """
        ).fetchall()
        conn.executemany(
            """
            update snps
            set first_seen_at = ?,
                classification_hash = ?,
                classification_updated_at = ?
            where rsid = ?
            """,
            [
                (
                    row["first_seen_at"] or row["source_updated_at"],
                    _classification_hash(
                        json.loads(row["clinvar_json"] or "[]"),
                        json.loads(row["clinical_significance_json"] or "[]"),
                    ),
                    _classification_source_date(json.loads(row["clinvar_json"] or "[]")),
                    row["rsid"],
                )
                for row in rows
            ],
        )

    def seed_from_legacy_files(
        self,
        scraped_path: Path | str = DEFAULT_SCRAPED_JSON,
        genotypes_path: Path | str = DEFAULT_GENOTYPES_JSON,
    ) -> None:
        scraped_path = Path(scraped_path)
        genotypes_path = Path(genotypes_path)
        if scraped_path.is_file() and self.count_snps() == 0:
            records = json.loads(scraped_path.read_text(encoding="utf-8"))
            self.upsert_snps(SNPRecord.from_legacy(rsid, payload) for rsid, payload in records.items())
        if genotypes_path.is_file() and self.count_genotypes() == 0:
            genotypes = json.loads(genotypes_path.read_text(encoding="utf-8"))
            self.upsert_genotypes(genotypes)

    def count_snps(self) -> int:
        with self.connect() as conn:
            return int(conn.execute("select count(*) from snps").fetchone()[0])

    def count_genotypes(self) -> int:
        with self.connect() as conn:
            return int(conn.execute("select count(*) from genotypes").fetchone()[0])

    def annotation_stats(self) -> dict[str, int]:
        with self.connect() as conn:
            row = conn.execute(
                """
                select
                    (select count(*) from genotypes) as imported_genotypes,
                    (select count(*) from genotype_variants) as normalized_variants,
                    (select count(*) from genotype_variants where zygosity = 'heterozygous') as heterozygous_variants,
                    (select count(*) from genotype_variants where zygosity = 'homozygous') as homozygous_variants,
                    (select count(*) from genotype_variants where zygosity = 'no-call') as no_call_variants,
                    (select count(*) from snps) as cached_snps,
                    (select count(*) from genotypes g join snps s on s.rsid = g.rsid) as annotated_genotypes,
                    (select count(*) from genotypes g left join snps s on s.rsid = g.rsid where s.rsid is null) as unannotated_genotypes,
                    (select count(*) from snps where clinvar_json != '[]') as cached_with_clinvar,
                    (select count(*) from snps where classification_updated_at != '') as cached_with_finding_dates,
                    coalesce((select value from reference_stats where key = 'vep_consequence_rows'), 0)
                        as vep_consequence_rows,
                    coalesce((select value from reference_stats where key = 'vep_consequence_rsids'), 0)
                        as vep_consequence_rsids,
                    coalesce((select value from reference_stats where key = 'vep_high_rsids'), 0)
                        as vep_high_rsids,
                    coalesce((select value from reference_stats where key = 'vep_moderate_rsids'), 0)
                        as vep_moderate_rsids,
                    coalesce((select value from reference_stats where key = 'clinvar_reference_rows'), 0)
                        as clinvar_reference_rows,
                    coalesce((select value from reference_stats where key = 'clinvar_reference_rsids'), 0)
                        as clinvar_reference_rsids,
                    coalesce((select value from reference_stats where key = 'clinvar_genotype_matches'), 0)
                        as clinvar_genotype_matches,
                    coalesce((select value from reference_stats where key = 'clinvar_heterozygous_matches'), 0)
                        as clinvar_heterozygous_matches,
                    coalesce((select value from reference_stats where key = 'clinvar_target_matches'), 0)
                        as clinvar_target_matches
                """
            ).fetchone()
        return {key: int(row[key]) for key in row.keys()}

    def refresh_summary_counts_cache(self) -> dict[str, dict[str, int]]:
        now = utc_now()
        presets = {
            "findings": dict(
                search="",
                has_genotype=False,
                mutated_only=False,
                clinical_match_only=False,
                promethease_only=True,
                new_since_import_only=False,
                summary_only=True,
            ),
            "new": dict(
                search="",
                has_genotype=False,
                mutated_only=False,
                clinical_match_only=False,
                promethease_only=True,
                new_since_import_only=True,
                summary_only=True,
            ),
            "clinical": dict(
                search="",
                has_genotype=False,
                mutated_only=False,
                clinical_match_only=True,
                promethease_only=False,
                new_since_import_only=False,
                summary_only=True,
            ),
            "all": dict(
                search="",
                has_genotype=True,
                mutated_only=False,
                clinical_match_only=False,
                promethease_only=False,
                new_since_import_only=False,
                summary_only=True,
            ),
        }
        cache: dict[str, dict[str, int]] = {}
        with self.connect() as conn:
            for key, kwargs in presets.items():
                cache[key] = self.snp_summary_counts(**kwargs)
                conn.execute(
                    """
                    insert into summary_counts_cache (key, payload_json, updated_at)
                    values (?, ?, ?)
                    on conflict(key) do update set
                        payload_json=excluded.payload_json,
                        updated_at=excluded.updated_at
                    """,
                    (key, json.dumps(cache[key], sort_keys=True), now),
                )
        return cache

    def cached_summary_counts(self, key: str) -> dict[str, int] | None:
        with self.connect() as conn:
            row = conn.execute(
                "select payload_json from summary_counts_cache where key = ?",
                [key],
            ).fetchone()
        if not row:
            return None
        try:
            payload = json.loads(row["payload_json"] or "{}")
        except json.JSONDecodeError:
            return None
        return {str(k): int(v or 0) for k, v in payload.items()}

    def refresh_clinvar_reference_stats(self) -> dict[str, int]:
        now = utc_now()
        with self.connect() as conn:
            return self._refresh_clinvar_reference_stats(conn, now)

    def replace_clinvar_variants(self, rows: Iterable[dict[str, str | int]], batch_size: int = 5000) -> int:
        now = utc_now()
        count = 0
        batch = []
        with self.connect() as conn:
            conn.execute("delete from clinvar_variants")
            for row in rows:
                batch.append(_clinvar_insert_tuple(row, now))
                if len(batch) >= batch_size:
                    conn.executemany(CLINVAR_INSERT_SQL, batch)
                    count += len(batch)
                    batch.clear()
            if batch:
                conn.executemany(CLINVAR_INSERT_SQL, batch)
                count += len(batch)
            self._refresh_clinvar_reference_stats(conn, now)
        return count

    def replace_vep_consequences(self, rows: Iterable[dict[str, Any]], batch_size: int = 5000) -> int:
        now = utc_now()
        count = 0
        batch = []
        with self.connect() as conn:
            conn.execute("delete from vep_consequences")
            for row in rows:
                rsid = normalize_rsid(str(row.get("rsid", "") or ""))
                if not rsid:
                    continue
                batch.append(_vep_insert_tuple(row, now))
                if len(batch) >= batch_size:
                    conn.executemany(VEP_INSERT_SQL, batch)
                    count += len(batch)
                    batch.clear()
            if batch:
                conn.executemany(VEP_INSERT_SQL, batch)
                count += len(batch)
            self._refresh_vep_stats(conn, now)
        return count

    def _refresh_clinvar_reference_stats(self, conn: sqlite3.Connection, updated_at: str) -> dict[str, int]:
        stats = {
            "clinvar_reference_rows": int(conn.execute("select count(*) from clinvar_variants").fetchone()[0]),
            "clinvar_reference_rsids": int(
                conn.execute("select count(distinct rsid) from clinvar_variants").fetchone()[0]
            ),
            "clinvar_genotype_matches": int(
                conn.execute(
                    """
                    select count(*) from genotypes g
                    where exists (select 1 from clinvar_variants cv where cv.rsid = g.rsid)
                    """
                ).fetchone()[0]
            ),
            "clinvar_heterozygous_matches": int(
                conn.execute(
                    f"""
                    select count(*) from genotypes g
                    where {_heterozygous_genotype_sql('g')}
                      and exists (select 1 from clinvar_variants cv where cv.rsid = g.rsid)
                    """
                ).fetchone()[0]
            ),
            "clinvar_target_matches": int(
                conn.execute(
                    f"""
                    select count(*) from genotypes g
                    where exists (
                        select 1 from clinvar_variants cv
                        where cv.rsid = g.rsid and {_clinvar_target_sql('cv')}
                    )
                    """
                ).fetchone()[0]
            ),
        }
        conn.executemany(
            """
            insert into reference_stats (key, value, updated_at)
            values (?, ?, ?)
            on conflict(key) do update set value=excluded.value, updated_at=excluded.updated_at
            """,
            [(key, value, updated_at) for key, value in stats.items()],
        )
        return stats

    def _refresh_vep_stats(self, conn: sqlite3.Connection, updated_at: str) -> dict[str, int]:
        stats = {
            "vep_consequence_rows": int(conn.execute("select count(*) from vep_consequences").fetchone()[0]),
            "vep_consequence_rsids": int(
                conn.execute("select count(distinct rsid) from vep_consequences").fetchone()[0]
            ),
            "vep_high_rsids": int(
                conn.execute(
                    "select count(distinct rsid) from vep_consequences where upper(impact) = 'HIGH'"
                ).fetchone()[0]
            ),
            "vep_moderate_rsids": int(
                conn.execute(
                    "select count(distinct rsid) from vep_consequences where upper(impact) = 'MODERATE'"
                ).fetchone()[0]
            ),
        }
        conn.executemany(
            """
            insert into reference_stats (key, value, updated_at)
            values (?, ?, ?)
            on conflict(key) do update set value=excluded.value, updated_at=excluded.updated_at
            """,
            [(key, value, updated_at) for key, value in stats.items()],
        )
        return stats

    def list_unannotated_genotypes(self, search: str = "", limit: int = 1000, offset: int = 0) -> list[dict[str, Any]]:
        params: list[Any] = []
        where = ["s.rsid is null"]
        if search:
            where.append("lower(g.rsid) like ?")
            params.append(f"%{search.lower()}%")
        params.extend([limit, offset])
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                select g.rsid, g.genotype, g.imported_at
                from genotypes g
                left join snps s on s.rsid = g.rsid
                where {' and '.join(where)}
                order by g.rsid
                limit ? offset ?
                """,
                params,
            )
            return [_unannotated_row(row) for row in rows]

    def clinvar_matched_rsids(
        self,
        targeted_only: bool = True,
        heterozygous_only: bool = False,
        missing_only: bool = False,
        limit: int = 5000,
    ) -> list[str]:
        where = ["g.rsid is not null"]
        if targeted_only:
            where.append(_clinvar_target_sql("cv"))
        if heterozygous_only:
            where.append(_heterozygous_genotype_sql("g"))
        if missing_only:
            where.append("s.rsid is null")
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                select cv.rsid, max(cv.last_evaluated) as latest_date,
                       max(case
                            when lower(cv.clinical_significance) like '%pathogenic%' then 100
                            when lower(cv.clinical_significance) like '%drug%' then 60
                            when lower(cv.clinical_significance) like '%risk%' then 50
                            when lower(cv.clinical_significance) like '%uncertain%' then 20
                            else 1
                       end) as priority
                from clinvar_variants cv
                join genotypes g on g.rsid = cv.rsid
                left join snps s on s.rsid = cv.rsid
                where {' and '.join(where)}
                group by cv.rsid
                order by priority desc, latest_date desc, cv.rsid
                limit ?
                """,
                [limit],
            )
            return [row["rsid"] for row in rows]

    def clinvar_records_for_rsids(self, rsids: list[str]) -> list[SNPRecord]:
        rsids = [normalize_rsid(rsid) for rsid in rsids]
        if not rsids:
            return []
        records = []
        for chunk in _chunks(rsids, 500):
            placeholders = ",".join("?" for _ in chunk)
            with self.connect() as conn:
                rows = conn.execute(
                    f"""
                    select *
                    from clinvar_variants
                    where rsid in ({placeholders})
                    order by rsid, last_evaluated desc, clinical_significance
                    """,
                    chunk,
                ).fetchall()
            records.extend(_clinvar_rows_to_records(rows))
        return records

    def genotype_map(self) -> dict[str, str]:
        with self.connect() as conn:
            rows = conn.execute("select rsid, genotype from genotypes where genotype is not null").fetchall()
        return {row["rsid"]: row["genotype"] for row in rows}

    def upsert_snps(self, records: Any) -> None:
        now = utc_now()
        rows = [
            (
                record.rsid,
                record.description,
                json.dumps(record.clinvar),
                json.dumps(record.clinical_significance),
                record.frequency,
                record.studies,
                record.citations,
                record.gene,
                record.risk,
                record.risk_allele or normalize_risk_allele(record.risk),
                record.frequency_percent
                if record.frequency_percent is not None
                else normalize_frequency_percent(record.frequency),
                json.dumps(record.variations),
                json.dumps(record.source_urls),
                now,
                _classification_hash(record.clinvar, record.clinical_significance),
                record.classification_updated_at,
                now,
            )
            for record in records
        ]
        with self.connect() as conn:
            conn.executemany(
                """
                insert into snps (
                    rsid, description, clinvar_json, clinical_significance_json, frequency, studies,
                    citations, gene, risk, risk_allele, frequency_percent, variations_json,
                    source_urls_json, first_seen_at, classification_hash, classification_updated_at,
                    source_updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(rsid) do update set
                    description=excluded.description,
                    clinvar_json=excluded.clinvar_json,
                    clinical_significance_json=excluded.clinical_significance_json,
                    frequency=excluded.frequency,
                    studies=excluded.studies,
                    citations=excluded.citations,
                    gene=excluded.gene,
                    risk=excluded.risk,
                    risk_allele=excluded.risk_allele,
                    frequency_percent=excluded.frequency_percent,
                    variations_json=excluded.variations_json,
                    source_urls_json=excluded.source_urls_json,
                    first_seen_at=snps.first_seen_at,
                    classification_updated_at=case
                        when excluded.classification_updated_at != '' then excluded.classification_updated_at
                        when snps.classification_hash != excluded.classification_hash then ''
                        else snps.classification_updated_at
                    end,
                    classification_hash=excluded.classification_hash,
                    source_updated_at=excluded.source_updated_at
                """,
                rows,
            )

    def merge_upsert_snps(self, records: Any) -> None:
        records = list(records)
        existing = {}
        with self.connect() as conn:
            for record in records:
                row = conn.execute("select * from snps where rsid = ?", [record.rsid]).fetchone()
                if row:
                    existing[record.rsid] = self._row_to_record(row)
        self.upsert_snps(_merge_record_update(record, existing.get(record.rsid)) for record in records)

    def upsert_genotypes(self, genotypes: dict[str, str]) -> None:
        now = utc_now()
        rows = [(normalize_rsid(rsid), genotype, now) for rsid, genotype in genotypes.items()]
        with self.connect() as conn:
            conn.executemany(
                """
                insert into genotypes (rsid, genotype, imported_at)
                values (?, ?, ?)
                on conflict(rsid) do update set
                    genotype=excluded.genotype,
                    imported_at=excluded.imported_at
                """,
                rows,
            )

    def upsert_genome_variants(self, variants: Iterable[Any]) -> int:
        now = utc_now()
        rows = [
            (
                normalize_rsid(variant.rsid),
                variant.chromosome,
                variant.position,
                variant.genotype,
                variant.allele_a,
                variant.allele_b,
                variant.zygosity,
                variant.assembly,
                variant.annotation_release,
                now,
            )
            for variant in variants
        ]
        with self.connect() as conn:
            conn.executemany(
                """
                insert into genotype_variants (
                    rsid, chromosome, position, genotype, allele_a, allele_b, zygosity,
                    assembly, annotation_release, imported_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(rsid) do update set
                    chromosome=excluded.chromosome,
                    position=excluded.position,
                    genotype=excluded.genotype,
                    allele_a=excluded.allele_a,
                    allele_b=excluded.allele_b,
                    zygosity=excluded.zygosity,
                    assembly=excluded.assembly,
                    annotation_release=excluded.annotation_release,
                    imported_at=excluded.imported_at
                """,
                rows,
            )
        return len(rows)

    def clear_genotypes(self) -> int:
        with self.connect() as conn:
            count = self.count_genotypes()
            conn.execute("delete from genotypes")
            conn.execute("delete from genotype_variants")
            return count

    def list_genome_variants(
        self,
        search: str = "",
        zygosity: str = "",
        clinical_only: bool = False,
        annotated_only: bool = False,
        mutated_only: bool = False,
        clinical_match_only: bool = False,
        promethease_only: bool = False,
        new_since_import_only: bool = False,
        vep_impact: str = "",
        vep_consequence: str = "",
        sort_field: str = "",
        sort_dir: str = "",
        limit: int = 1000,
        offset: int = 0,
        with_total: bool = False,
    ) -> list[dict[str, Any]] | tuple[list[dict[str, Any]], int]:
        params: list[Any] = []
        where = []
        if search:
            search_lower = search.lower()
            if re.fullmatch(r"(?:rs|gs)\d+", search_lower):
                where.append("lower(gv.rsid) = ?")
                params.append(search_lower)
            else:
                like = f"%{search_lower}%"
                where.append(
                    "(lower(gv.rsid) like ? or lower(s.gene) like ? or lower(s.description) like ? "
                    "or lower(s.clinical_significance_json) like ? or lower(s.clinvar_json) like ?)"
                )
                params.extend([like, like, like, like, like])
        if zygosity:
            where.append("gv.zygosity = ?")
            params.append(zygosity)
        if clinical_only:
            where.append("exists (select 1 from clinvar_variants cv where cv.rsid = gv.rsid)")
        if annotated_only:
            where.append("s.rsid is not null")
        if mutated_only or clinical_match_only or promethease_only:
            where.append("s.rsid is not null")
            if clinical_match_only:
                where.append("s.risk_allele != ''")
                where.append("s.clinical_significance_json != '[]'")
            if mutated_only or promethease_only:
                where.append(
                    "(s.variations_json != '[]' or (s.risk_allele != '' and s.clinical_significance_json != '[]'))"
                )
        if new_since_import_only:
            where.append("s.classification_updated_at != ''")
            where.append("g.imported_at != ''")
            where.append("s.classification_updated_at > g.imported_at")
        if vep_impact:
            where.append("exists (select 1 from vep_consequences vc where vc.rsid = gv.rsid and upper(vc.impact) = ?)")
            params.append(vep_impact.upper())
        if vep_consequence:
            where.append(
                "exists (select 1 from vep_consequences vc where vc.rsid = gv.rsid "
                "and lower(vc.consequence) like ?)"
            )
            params.append(f"%{vep_consequence.lower()}%")
        order_clause = _variant_order_clause(sort_field, sort_dir)
        base_sql = """
            select
                gv.rsid,
                gv.chromosome,
                gv.position,
                gv.genotype,
                gv.allele_a,
                gv.allele_b,
                gv.zygosity,
                gv.assembly,
                gv.annotation_release,
                gv.imported_at,
                g.imported_at as genotype_imported_at,
                s.rsid as snp_rsid,
                s.description,
                s.clinvar_json,
                s.clinical_significance_json,
                s.frequency,
                s.studies,
                s.citations,
                s.gene,
                s.risk,
                s.risk_allele,
                s.frequency_percent,
                s.variations_json,
                s.source_urls_json,
                s.first_seen_at,
                s.classification_hash,
                s.classification_updated_at,
                s.source_updated_at,
                vep.vep_impact_rank,
                vep.vep_impacts,
                vep.vep_consequences,
                vep.vep_symbols
            from genotype_variants gv
            left join snps s on s.rsid = gv.rsid
            left join genotypes g on g.rsid = gv.rsid
            left join (
                select
                    rsid,
                    max(case upper(impact)
                        when 'HIGH' then 4
                        when 'MODERATE' then 3
                        when 'LOW' then 2
                        when 'MODIFIER' then 1
                        else 0
                    end) as vep_impact_rank,
                    group_concat(distinct nullif(impact, '')) as vep_impacts,
                    group_concat(distinct nullif(consequence, '')) as vep_consequences,
                    group_concat(distinct nullif(symbol, '')) as vep_symbols
                from vep_consequences
                group by rsid
                ) vep on vep.rsid = gv.rsid
        """
        if where:
            base_sql += " where " + " and ".join(where)
        sql = base_sql + f" order by {order_clause} limit ? offset ?"
        with self.connect() as conn:
            if mutated_only or clinical_match_only or promethease_only:
                rows, total = _load_paged_rows(
                    conn,
                    sql,
                    params,
                    limit,
                    offset,
                    self._variant_row_to_legacy,
                    post_filters=[
                        (lambda batch: [row for row in batch if row["HasClinicalAlleleMatch"]])
                        if clinical_match_only
                        else None,
                        (lambda batch: [row for row in batch if row["HasPrometheaseMatch"]])
                        if promethease_only or mutated_only
                        else None,
                    ],
                )
            else:
                count_sql = f"select count(*) from ({base_sql}) as counted"
                rows, total = _load_paged_rows(
                    conn,
                    sql,
                    params,
                    limit,
                    offset,
                    self._variant_row_to_legacy,
                    count_sql=count_sql,
                )
        return (rows, total) if with_total else rows

    def list_snps(
        self,
        search: str = "",
        has_genotype: bool = False,
        mutated_only: bool = False,
        clinical_match_only: bool = False,
        promethease_only: bool = False,
        new_since_import_only: bool = False,
        severity_filters: list[str] | None = None,
        summary_only: bool = False,
        sort_field: str = "",
        sort_dir: str = "",
        limit: int = 1000,
        offset: int = 0,
        with_total: bool = False,
    ) -> list[dict[str, str]] | tuple[list[dict[str, str]], int]:
        base_sql, params = _snps_base_sql(
            search=search,
            has_genotype=has_genotype,
            mutated_only=mutated_only,
            clinical_match_only=clinical_match_only,
            promethease_only=promethease_only,
            new_since_import_only=new_since_import_only,
            severity_filters=severity_filters,
            summary_only=summary_only,
        )
        order_clause = _snps_order_clause(sort_field, sort_dir)
        sql = base_sql + f" order by {order_clause} limit ? offset ?"

        with self.connect() as conn:
            if mutated_only or clinical_match_only or promethease_only:
                rows, total = _load_paged_rows(
                    conn,
                    sql,
                    params,
                    limit,
                    offset,
                    self._row_to_legacy,
                    post_filters=[
                        (lambda batch: [row for row in batch if row["HasClinicalAlleleMatch"]])
                        if clinical_match_only
                        else None,
                        (lambda batch: [row for row in batch if row["HasPrometheaseMatch"]])
                        if promethease_only or mutated_only
                        else None,
                    ],
                    resort_score=sort_field == "SignificanceScore",
                    sort_reverse=_normalize_sort_dir(sort_dir) == "desc",
                )
            else:
                count_sql = f"select count(*) from ({base_sql}) as counted"
                rows, total = _load_paged_rows(
                    conn,
                    sql,
                    params,
                    limit,
                    offset,
                    self._row_to_legacy,
                    count_sql=count_sql,
                )
        return (rows, total) if with_total else rows

    def snp_summary_counts(
        self,
        search: str = "",
        has_genotype: bool = False,
        mutated_only: bool = False,
        clinical_match_only: bool = False,
        promethease_only: bool = False,
        new_since_import_only: bool = False,
        severity_filters: list[str] | None = None,
        summary_only: bool = False,
    ) -> dict[str, int]:
        base_sql, params = _snps_base_sql(
            search=search,
            has_genotype=has_genotype,
            mutated_only=mutated_only,
            clinical_match_only=clinical_match_only,
            promethease_only=promethease_only,
            new_since_import_only=new_since_import_only,
            severity_filters=severity_filters,
            summary_only=summary_only,
        )
        counts_sql = f"""
            select
                count(*) as findings,
                sum(case when (
                    lower(coalesce(clinical_significance_json, '')) not in ('', '[]')
                    or lower(coalesce(clinvar_json, '')) not in ('', '[]')
                    or coalesce(risk_allele, '') != ''
                ) then 1 else 0 end) as clinical,
                sum(case when (
                    coalesce(risk_allele, '') != ''
                    and coalesce(genotype, '(n/a)') != '(n/a)'
                    and upper(coalesce(genotype, '')) like '%' || upper(coalesce(risk_allele, '')) || '%'
                    and (
                        {_severity_count_clause('counted', 'pathogenic')}
                        or {_severity_count_clause('counted', 'drug')}
                        or {_severity_count_clause('counted', 'risk')}
                        or {_severity_count_clause('counted', 'modifier')}
                        or {_severity_count_clause('counted', 'uncertain')}
                    )
                ) then 1 else 0 end) as clinical_match,
                sum(case when {_severity_count_clause('counted', 'pathogenic')} then 1 else 0 end) as pathogenic,
                sum(case when {_severity_count_clause('counted', 'risk')} then 1 else 0 end) as risk,
                sum(case when {_severity_count_clause('counted', 'drug')} then 1 else 0 end) as drug,
                sum(case when {_severity_count_clause('counted', 'modifier')} then 1 else 0 end) as modifier,
                sum(case when {_severity_count_clause('counted', 'uncertain')} then 1 else 0 end) as uncertain,
                sum(case when {_severity_count_clause('counted', 'benign')} then 1 else 0 end) as benign,
                sum(case when (
                    counted.classification_updated_at != ''
                    and counted.imported_at != ''
                    and counted.classification_updated_at > counted.imported_at
                ) then 1 else 0 end) as new_findings
            from ({base_sql}) as counted
        """
        with self.connect() as conn:
            row = conn.execute(counts_sql, params).fetchone()
        return {
            "clinical": int(row["clinical"] or 0),
            "clinical-match": int(row["clinical_match"] or 0),
            "findings": int(row["findings"] or 0),
            "pathogenic": int(row["pathogenic"] or 0),
            "risk": int(row["risk"] or 0),
            "drug": int(row["drug"] or 0),
            "modifier": int(row["modifier"] or 0),
            "uncertain": int(row["uncertain"] or 0),
            "benign": int(row["benign"] or 0),
            "new": int(row["new_findings"] or 0),
        }


    def rsids_missing_annotations(self, rsids: list[str]) -> list[str]:
        rsids = [normalize_rsid(rsid) for rsid in rsids]
        if not rsids:
            return []
        placeholders = ",".join("?" for _ in rsids)
        with self.connect() as conn:
            cached = {
                row["rsid"]
                for row in conn.execute(f"select rsid from snps where rsid in ({placeholders})", rsids)
            }
        return [rsid for rsid in rsids if rsid not in cached]

    def rsids_missing_finding_dates(self, rsids: list[str]) -> list[str]:
        rsids = [normalize_rsid(rsid) for rsid in rsids]
        if not rsids:
            return []
        placeholders = ",".join("?" for _ in rsids)
        with self.connect() as conn:
            dated = {
                row["rsid"]
                for row in conn.execute(
                    f"""
                    select rsid from snps
                    where rsid in ({placeholders})
                      and classification_updated_at != ''
                    """,
                    rsids,
                )
            }
        return [rsid for rsid in rsids if rsid not in dated]

    def get_snp(self, rsid: str, enrich_snpedia: bool = False) -> dict[str, str] | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                select
                    s.*,
                    coalesce(g.genotype, '(n/a)') as genotype,
                    gv.chromosome,
                    gv.position,
                    gv.zygosity,
                    gv.assembly,
                    gv.annotation_release
                from snps s
                left join genotypes g on g.rsid = s.rsid
                left join genotype_variants gv on gv.rsid = s.rsid
                where s.rsid = ?
                """,
                [normalize_rsid(rsid)],
            ).fetchone()
            if not row:
                return None
            return self._row_to_legacy(row, enrich_snpedia=enrich_snpedia)

    def create_scrape_run(self, total: int, message: str = "", rsids: list[str] | None = None) -> int:
        now = utc_now()
        with self.connect() as conn:
            cur = conn.execute(
                "insert into scrape_runs (status, total, message, started_at) values (?, ?, ?, ?)",
                ("running", total, message, now),
            )
            run_id = int(cur.lastrowid)
            if rsids:
                conn.executemany(
                    """
                    insert or replace into scrape_run_items (run_id, rsid, status, message, updated_at)
                    values (?, ?, 'pending', '', ?)
                    """,
                    [(run_id, normalize_rsid(rsid), now) for rsid in rsids],
                )
            return run_id

    def update_scrape_run(self, run_id: int, status: str, completed: int, failed: int, message: str = "") -> None:
        ended_at = utc_now() if status in {"complete", "failed", "paused", "canceled"} else None
        with self.connect() as conn:
            conn.execute(
                """
                update scrape_runs
                set status=?, completed=?, failed=?, message=?, ended_at=coalesce(?, ended_at),
                    requested_status=case when ? in ('paused', 'canceled', 'complete', 'failed') then null else requested_status end
                where id=?
                """,
                (status, completed, failed, message, ended_at, status, run_id),
            )

    def request_scrape_status(self, run_id: int, requested_status: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "update scrape_runs set requested_status = ?, message = ? where id = ? and status = 'running'",
                (requested_status, f"{requested_status} requested", run_id),
            )

    def get_scrape_requested_status(self, run_id: int) -> str | None:
        with self.connect() as conn:
            row = conn.execute("select requested_status from scrape_runs where id = ?", [run_id]).fetchone()
            return row["requested_status"] if row else None

    def latest_scrape_run(self) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("select * from scrape_runs order by id desc limit 1").fetchone()
            return dict(row) if row else None

    def get_scrape_run(self, run_id: int) -> dict[str, Any] | None:
        with self.connect() as conn:
            run = conn.execute("select * from scrape_runs where id = ?", [run_id]).fetchone()
            if not run:
                return None
            items = [
                dict(row)
                for row in conn.execute(
                    "select rsid, status, message, updated_at from scrape_run_items where run_id = ? order by rsid",
                    [run_id],
                )
            ]
            result = dict(run)
            result["items"] = items
            return result

    def set_scrape_item_status(self, run_id: int, rsid: str, status: str, message: str = "") -> None:
        with self.connect() as conn:
            conn.execute(
                """
                insert into scrape_run_items (run_id, rsid, status, message, updated_at)
                values (?, ?, ?, ?, ?)
                on conflict(run_id, rsid) do update set
                    status=excluded.status,
                    message=excluded.message,
                    updated_at=excluded.updated_at
                """,
                (run_id, normalize_rsid(rsid), status, message, utc_now()),
            )

    def set_scrape_items_status_by_status(
        self,
        run_id: int,
        from_statuses: list[str],
        to_status: str,
        message: str = "",
    ) -> None:
        placeholders = ",".join("?" for _ in from_statuses)
        with self.connect() as conn:
            conn.execute(
                f"""
                update scrape_run_items
                set status = ?, message = ?, updated_at = ?
                where run_id = ? and status in ({placeholders})
                """,
                [to_status, message, utc_now(), run_id, *from_statuses],
            )

    def scrape_items_by_status(self, run_id: int, statuses: list[str]) -> list[str]:
        placeholders = ",".join("?" for _ in statuses)
        with self.connect() as conn:
            rows = conn.execute(
                f"select rsid from scrape_run_items where run_id = ? and status in ({placeholders}) order by rsid",
                [run_id, *statuses],
            )
            return [row["rsid"] for row in rows]

    def export_csv(self, path: Path) -> Path:
        rows = self.list_snps(limit=100000)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys() if rows else ["Name"])
            writer.writeheader()
            writer.writerows(rows)
        return path

    def export_vep_input(self, path: Path, zygosity: str = "", limit: int = 1000000) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        params: list[Any] = []
        where = ["zygosity != 'no-call'", "chromosome != ''", "position is not null"]
        if zygosity:
            where.append("zygosity = ?")
            params.append(zygosity)
        params.append(limit)
        with self.connect() as conn, path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="\t")
            for row in conn.execute(
                f"""
                select chromosome, position, allele_a, allele_b, rsid
                from genotype_variants
                where {' and '.join(where)}
                order by chromosome, position, rsid
                limit ?
                """,
                params,
            ):
                writer.writerow(
                    [
                        row["chromosome"],
                        row["position"],
                        row["position"],
                        f"{row['allele_a']}/{row['allele_b']}",
                        "+",
                        row["rsid"],
                    ]
                )
        return path

    def export_vep_ids(self, path: Path, zygosity: str = "", limit: int = 1000000) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        params: list[Any] = []
        where = ["rsid like 'rs%'"]
        if zygosity:
            where.append("zygosity = ?")
            params.append(zygosity)
        params.append(limit)
        with self.connect() as conn, path.open("w", newline="", encoding="utf-8") as file:
            for row in conn.execute(
                f"""
                select rsid
                from genotype_variants
                where {' and '.join(where)}
                order by chromosome, position, rsid
                limit ?
                """,
                params,
            ):
                file.write(f"{row['rsid']}\n")
        return path

    def _row_to_record(self, row: sqlite3.Row) -> SNPRecord:
        return SNPRecord(
            rsid=row["rsid"],
            description=row["description"],
            clinvar=json.loads(row["clinvar_json"] or "[]"),
            frequency=row["frequency"],
            studies=row["studies"],
            citations=row["citations"],
            gene=row["gene"],
            risk=row["risk"],
            risk_allele=row["risk_allele"],
            frequency_percent=row["frequency_percent"] if row["frequency_percent"] and row["frequency_percent"] > 0 else None,
            variations=json.loads(row["variations_json"] or "[]"),
            clinical_significance=json.loads(row["clinical_significance_json"] or "[]"),
            source_urls=json.loads(row["source_urls_json"] or "{}"),
            classification_updated_at=row["classification_updated_at"],
        )

    def _row_to_legacy(self, row: sqlite3.Row, enrich_snpedia: bool = False) -> dict[str, Any]:
        payload = self._row_to_record(row).to_legacy(row["genotype"])
        if enrich_snpedia:
            payload = _enrich_cached_snpedia_summary(payload)
        payload["FirstSeenAt"] = row["first_seen_at"]
        payload["ClassificationUpdatedAt"] = row["classification_updated_at"]
        payload["RecentFindingAt"] = row["classification_updated_at"]
        payload["SourceUpdatedAt"] = row["source_updated_at"]
        payload["ImportedAt"] = row["imported_at"] if "imported_at" in row.keys() else ""
        payload["FindingFreshness"] = _finding_freshness(
            row["classification_updated_at"],
            row["source_updated_at"],
            row["imported_at"] if "imported_at" in row.keys() else "",
        )
        payload.update(_variant_metadata(row))
        return payload

    def _variant_row_to_legacy(self, row: sqlite3.Row, enrich_snpedia: bool = False) -> dict[str, Any]:
        if row["snp_rsid"]:
            payload = self._row_to_record(row).to_legacy(row["genotype"])
            if enrich_snpedia:
                payload = _enrich_cached_snpedia_summary(payload)
            payload["FirstSeenAt"] = row["first_seen_at"]
            payload["ClassificationUpdatedAt"] = row["classification_updated_at"]
            payload["RecentFindingAt"] = row["classification_updated_at"]
            payload["SourceUpdatedAt"] = row["source_updated_at"]
            payload["ImportedAt"] = row["genotype_imported_at"] if "genotype_imported_at" in row.keys() else row["imported_at"]
            payload["FindingFreshness"] = _finding_freshness(
                row["classification_updated_at"],
                row["source_updated_at"],
                row["genotype_imported_at"] if "genotype_imported_at" in row.keys() else row["imported_at"],
            )
        else:
            payload = _unannotated_variant_row(row)
        payload.update(
            {
                "Chromosome": row["chromosome"],
                "Position": row["position"],
                "VariantZygosity": row["zygosity"],
                "VariantAssembly": row["assembly"],
                "AnnotationRelease": row["annotation_release"],
                "AlleleA": row["allele_a"],
                "AlleleB": row["allele_b"],
                "HasCachedAnnotation": bool(row["snp_rsid"]),
                "VepImpact": _vep_best_impact(row["vep_impacts"], row["vep_impact_rank"]),
                "VepImpactRank": row["vep_impact_rank"] or 0,
                "VepConsequence": row["vep_consequences"] or "",
                "VepSymbol": row["vep_symbols"] or "",
                "HasVepConsequence": bool(row["vep_impact_rank"]),
            }
        )
        return payload


def _snps_base_sql(
    search: str = "",
    has_genotype: bool = False,
    mutated_only: bool = False,
    clinical_match_only: bool = False,
    promethease_only: bool = False,
    new_since_import_only: bool = False,
    severity_filters: list[str] | None = None,
    summary_only: bool = False,
) -> tuple[str, list[Any]]:
    params: list[Any] = []
    where = []
    if search:
        search_lower = search.lower()
        if re.fullmatch(r"(?:rs|gs)\d+", search_lower):
            where.append("lower(s.rsid) = ?")
            params.append(search_lower)
        else:
            like = f"%{search_lower}%"
            where.append(
                "(lower(s.rsid) like ? or lower(s.gene) like ? or lower(s.description) like ? "
                "or lower(s.clinical_significance_json) like ?)"
            )
            params.extend([like, like, like, like])
    if has_genotype:
        where.append("g.genotype is not null")
    if mutated_only or clinical_match_only or promethease_only:
        where.append("g.genotype is not null")
        if clinical_match_only:
            where.append("s.risk_allele != ''")
            where.append("s.clinical_significance_json != '[]'")
        if mutated_only or promethease_only:
            where.append(
                "(s.variations_json != '[]' or (s.risk_allele != '' and s.clinical_significance_json != '[]'))"
            )
    if new_since_import_only:
        where.append("s.classification_updated_at != ''")
        where.append("g.imported_at != ''")
        where.append("s.classification_updated_at > g.imported_at")
    if severity_filters:
        severity_clauses = []
        for severity in severity_filters:
            severity = str(severity or "").strip().lower()
            if not severity:
                continue
            clause = _severity_search_clause("s", severity)
            if clause:
                severity_clauses.append(clause)
        if severity_clauses:
            where.append("(" + " or ".join(severity_clauses) + ")")

    if summary_only:
        base_sql = """
            select
                s.rsid,
                s.description,
                '[]' as clinvar_json,
                s.clinical_significance_json,
                s.frequency,
                '' as studies,
                s.citations,
                s.gene,
                s.risk,
                s.risk_allele,
                s.frequency_percent,
                s.variations_json,
                '{}' as source_urls_json,
                s.first_seen_at,
                s.classification_updated_at,
                s.source_updated_at,
                g.imported_at,
                coalesce(g.genotype, '(n/a)') as genotype,
                gv.chromosome,
                gv.position,
                gv.zygosity,
                gv.assembly,
                gv.annotation_release
            from snps s
            left join genotypes g on g.rsid = s.rsid
            left join genotype_variants gv on gv.rsid = s.rsid
        """
    else:
        base_sql = """
            select
                s.*,
                coalesce(g.genotype, '(n/a)') as genotype,
                g.imported_at,
                gv.chromosome,
                gv.position,
                gv.zygosity,
                gv.assembly,
                gv.annotation_release
            from snps s
            left join genotypes g on g.rsid = s.rsid
            left join genotype_variants gv on gv.rsid = s.rsid
        """
    if where:
        base_sql += " where " + " and ".join(where)
    return base_sql, params


def _normalize_sort_dir(value: str) -> str:
    return "asc" if str(value).lower() == "asc" else "desc"


def _clinical_score_sql(alias: str) -> str:
    text = f"lower(coalesce({alias}.clinical_significance_json, ''))"
    clauses = [f"when {text} like '%{marker}%' then {score}" for marker, _, score in CLINICAL_SEVERITY_RULES]
    return "case " + " ".join(clauses) + " else 0 end"


def _snps_order_clause(sort_field: str, sort_dir: str) -> str:
    direction = _normalize_sort_dir(sort_dir)
    clinical_score = _clinical_score_sql("s")
    expressions = {
        "Name": f"s.rsid {direction}",
        "Gene": f"lower(coalesce(s.gene, '')) {direction}, s.rsid asc",
        "RiskAllele": f"coalesce(s.risk_allele, '') {direction}, s.rsid asc",
        "FrequencyPercent": f"coalesce(s.frequency_percent, -1) {direction}, s.rsid asc",
        "ClassificationUpdatedAt": f"coalesce(s.classification_updated_at, '') {direction}, s.rsid asc",
        "PublicationCount": f"cast(coalesce(s.citations, '0') as integer) {direction}, s.rsid asc",
        "SnpediaMagnitude": (
            "coalesce(cast(json_extract(s.variations_json, '$[0][1]') as real), -1) "
            f"{direction}, s.rsid asc"
        ),
        "SignificanceScore": f"{clinical_score} {direction}, s.rsid asc",
        "FindingSeverityScore": f"{clinical_score} {direction}, s.rsid asc",
        "FindingType": (
            f"{clinical_score} "
            f"{direction}, coalesce(s.classification_updated_at, '') desc, s.rsid asc"
        ),
        "Genotype": f"coalesce(g.genotype, '') {direction}, s.rsid asc",
        "Description": f"lower(coalesce(s.description, '')) {direction}, s.rsid asc",
    }
    return expressions.get(sort_field, f"s.rsid {direction}")


def _variant_order_clause(sort_field: str, sort_dir: str) -> str:
    direction = _normalize_sort_dir(sort_dir)
    expressions = {
        "Name": f"gv.rsid {direction}",
        "Gene": f"lower(coalesce(s.gene, '')) {direction}, gv.rsid asc",
        "FrequencyPercent": f"coalesce(s.frequency_percent, -1) {direction}, gv.rsid asc",
        "ClassificationUpdatedAt": f"coalesce(s.classification_updated_at, '') {direction}, gv.rsid asc",
        "PublicationCount": f"cast(coalesce(s.citations, '0') as integer) {direction}, gv.rsid asc",
        "Genotype": f"coalesce(gv.genotype, '') {direction}, gv.rsid asc",
        "RiskAllele": f"coalesce(s.risk_allele, '') {direction}, gv.rsid asc",
        "Description": f"lower(coalesce(s.description, '')) {direction}, gv.rsid asc",
    }
    return expressions.get(sort_field, "gv.chromosome asc, gv.position asc, gv.rsid asc")


def _clinvar_target_sql(alias: str) -> str:
    field = f"lower({alias}.clinical_significance)"
    return (
        f"({field} like '%pathogenic%' or {field} like '%risk%' or {field} like '%drug%' "
        f"or {field} like '%affects%' or {field} like '%protective%' or {field} like '%association%' "
        f"or {field} like '%uncertain%' or {field} like '%conflicting%')"
    )


def _heterozygous_genotype_sql(alias: str) -> str:
    return f"(length({alias}.genotype) >= 5 and substr({alias}.genotype, 2, 1) != substr({alias}.genotype, 4, 1))"
