# Contributing

Thanks for taking an interest in Open Sports Profile. The specification is a working draft, so feedback is most useful right now.

## What helps most

- **Questions and unclear wording.** If a section of [SPEC.md](SPEC.md) is ambiguous, open an issue. Ambiguity is a bug in a standard.
- **Real-world cases that don't fit.** A team, league or fandom story the format can't express is valuable evidence. Describe the case and what you would have wanted to write.
- **Corrections.** Wrong identifiers, broken links, schema bugs and typos can go straight to a pull request.
- **Implementation reports.** If you try producing or reading a profile, tell us what worked and what didn't.

## Proposing changes to the spec

Open an issue first for anything that changes meaning: new fields, new relationship values, changed requirements. Say what problem you are solving and what you tried instead. Version 0.1 is intentionally small, so changes that add scope may be deferred to a later version.

Small fixes can skip the issue and go straight to a pull request.

## Pull requests

- Keep each pull request to one change.
- The JSON-LD context in [section 5 of the spec](SPEC.md#5-json-ld-context) is generated from `context/v0.1/context.jsonld`. Edit the file, then run `python3 scripts/sync-spec.py`. The deploy workflow fails if the two disagree.
- If you change the structure of a profile, update the schema in `schema/v0.1/profile.schema.json` and the example in section 6 of the spec so they stay consistent.

## Licensing of contributions

By submitting a contribution you agree that it is licensed under the same terms as the file it changes: [CC BY 4.0](LICENSE-SPEC) for the specification text, [Apache 2.0](LICENSE) for the schema, context, examples and code. There is no separate contributor agreement to sign.
