# Open Sports Profile

**A portable format for your sports identity.**

Open Sports Profile (OSP) is a small, open data format for describing which sports teams a person supports, which they used to support, when, and why. Create your fandom once, export it, and any app that speaks OSP can understand it.

OSP is a standard, not a product. It says nothing about how a profile looks; logos, colors and cards are up to whoever displays it.

```json
{
  "team": "http://www.wikidata.org/entity/Q194116",
  "teamName": "Detroit Red Wings",
  "sport": "Ice Hockey",
  "relationship": "former_fan",
  "seasons": [{ "from": "1996-97", "to": "2011-12" }],
  "reason": "Huge fan of Steve Yzerman and Nicklas Lidstrom."
}
```

That is one entry from a profile. A full example is in [section 6 of the specification](SPEC.md#6-example-profile).

## Status

**Version 0.1, a working draft.** The scope is deliberately small: current fan or former fan of a specific team, with optional seasons and a reason. Playing history, verification and privacy controls are planned for later versions. There is no validator or reference implementation yet, so expect changes.

## Links

- **Specification:** [opensportsprofile.org](https://opensportsprofile.org) (source: [SPEC.md](SPEC.md))
- **JSON-LD context:** <https://opensportsprofile.org/v0.1/context.jsonld>
- **JSON Schema:** <https://opensportsprofile.org/v0.1/profile.schema.json>
- **Vocabulary:** <https://opensportsprofile.org/ns>

## How it fits with other standards

OSP reuses existing vocabularies and defines only what they lack, the fan relationship itself:

- [Schema.org](https://schema.org/) for the profile document, the person and team descriptions.
- [IPTC Sport Schema](https://iptc.org/standards/sport-schema/) for team entities and the competitions behind seasons.
- [Wikidata](https://www.wikidata.org/) as the default source of team and sport identifiers.

## Repository layout

| Path | What it is |
|---|---|
| `SPEC.md` | The specification |
| `schema/v0.1/profile.schema.json` | JSON Schema for the structural rules |
| `context/v0.1/context.jsonld` | The JSON-LD context (the source of the block in section 5 of the spec) |
| `scripts/sync-spec.py` | Keeps section 5 of the spec in sync with the context file |
| `scripts/build-site.py` | Builds the website from the files above |

Pushes to `main` rebuild and deploy the site through GitHub Pages.

## Working on the spec

After editing `context/v0.1/context.jsonld`, run `python3 scripts/sync-spec.py` to update the spec. Run it with `--check` to confirm the two agree; the deploy workflow does this too. Building the site locally needs `pip install markdown`, then `python3 scripts/build-site.py`.

## Contributing

Questions, corrections and proposals are welcome as [issues](https://github.com/darrenaalfonso/open-sports-profile/issues). See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Copyright (c) 2026 Darren Alfonso and the Open Sports Profile contributors.

| What | License | File |
|---|---|---|
| The specification text (`SPEC.md`) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [LICENSE-SPEC](LICENSE-SPEC) |
| The schema, context, examples and code | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE) |

The names "Open Sports Profile" and "OSP" are not licensed by either of the above.
