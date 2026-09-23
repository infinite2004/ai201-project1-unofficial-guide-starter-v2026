"""Record Milestone 4 distances and full retrieved context without model calls."""
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from questions import QUESTIONS, OUT_OF_SCOPE
from store import search


def main():
    rows = []
    for covered, questions in [(True, [q['question'] for q in QUESTIONS]),
                               (False, OUT_OF_SCOPE)]:
        for question in questions:
            hits = search(question, corpus='campus_life', top_k=config.TOP_K)
            rows.append(dict(question=question, in_corpus=covered,
                             best_distance=hits[0].distance,
                             results=[asdict(hit) for hit in hits]))
            print(f"{'IN ' if covered else 'OUT'} {hits[0].distance:.6f} {question}", flush=True)
    report = dict(corpus='campus_life', chunk_size=config.CHUNK_SIZE,
                  overlap=config.CHUNK_OVERLAP, top_k=config.TOP_K,
                  embedding_model=config.EMBEDDING_MODEL, rows=rows)
    path = config.RESULTS_DIR / 'milestone-4-retrieval.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    lines = ['# Milestone 4 retrieval evidence', '',
             'Actual local embeddings; no generation calls. Lower distance is closer.', '']
    for row in rows:
        lines += [f"## {row['question']}", '', f"In corpus: {row['in_corpus']}", '']
        for i, hit in enumerate(row['results'], 1):
            lines += [f"### {i}. {hit['label']} — distance {hit['distance']:.6f}", '',
                      '```text', hit['text'], '```', '']
    (config.RESULTS_DIR / 'milestone-4-retrieval.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
