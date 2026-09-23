# Milestone 3 decision — recorded before implementation

The starter indexed 88 campus_life documents as 88 chunks: mean 317 characters,
minimum 178, maximum 549, using 800-character windows with 120-character overlap.
It did not split a post. This is the baseline, not evidence of a broken index.

Use a 400-character soft target including the title. Keep paragraphs intact
when they fit, split longer paragraphs only at sentence boundaries, and repeat
the original short title in each chunk so a second chunk retains its subject.
Use zero body-text overlap: these short posts already pack facts tightly, so
repeating body sentences could crowd the top results with duplicate evidence.
The repeated title is deliberate context, not a fixed overlapping window.

Keep a whole post when it fits. Prefer a paragraph break when another paragraph
would exceed the target. A sentence too long to fit remains intact, even if the
result exceeds 400 characters; do not create fragments merely to enforce size.
The lightweight sentence splitter is intended for the supplied English posts,
not arbitrary prose with every possible abbreviation.

Rationale: the dining posts can separate their descriptive paragraph from hours
and prices, while short policy posts should remain whole. A 400-character target
is above the observed mean but below the longest posts. This is a design choice
to inspect, not a claim that shorter chunks improve measured retrieval.

Preserve fallback_split for comparison. Do not change criteria or expected
phrases in response to observed results. Unit 2 evaluation is a separate task.
