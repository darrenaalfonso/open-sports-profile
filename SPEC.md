# Open Sports Profile (OSP) — Specification

**Version:** 0.1 (draft)
**Status:** Working draft, not yet implemented
**Tagline:** A portable format for your sports identity.

## 1. Introduction

Open Sports Profile is a small, open data format for describing a person's *fandom*: which sports teams they support, which they used to support, when, and why. A profile can be created once, exported, and understood by any application that implements this specification.

OSP is a **standard**, not a product. It deliberately says nothing about how a profile is displayed. Logos, colors, wordmarks and other presentation assets are out of scope (see §8).

### 1.1 Scope of 0.1

Version 0.1 covers fandom only:

- Current fan of a specific team
- Former fan of a specific team
- Optional seasons
- Optional free-text reason

Participation history ("played for", coached, worked for), verification, privacy controls, authentication and federation are **intentionally outside the scope of 0.1**. Their omission is a scoping decision, not a claim that fandom is the only kind of sports identity. Participation history is expected in a future version (see §8).

### 1.2 Conformance language

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as in RFC 2119 / RFC 8174.

## 2. Design principles

1. **Reuse, don't reinvent.** Where Schema.org, IPTC Sport Schema or Wikidata already define a concept or an identifier, OSP uses it. OSP only defines terms for what they lack: the *fan relationship* itself.
2. **Teams are references, not strings.** A team is identified by an IRI wherever one exists. A human-readable name and sport accompany it for legibility, but never replace it. A team with no IRI at all is a *bare team*, identified only by its name and sport (§3.2).
3. **A fan supports a specific team.** A relationship names one team in one sport, never a whole school or club.
4. **Meaning, not presentation.** If a team's logo changes, no profile changes.
5. **Plain JSON first.** A profile is valid JSON-LD, but a consumer that knows nothing about JSON-LD can read it as ordinary JSON.
6. **Tiny.** Few required fields; everything else is optional.

## 3. Alignment with Schema.org, Sport Schema and Wikidata

OSP is serialized as JSON-LD and composes three vocabularies. It also uses Wikidata as the default source of team identifiers.

| Vocabulary | Prefix | Namespace | Used for |
|---|---|---|---|
| Schema.org | `schema` | `https://schema.org/` | The profile document, the person, and the descriptions of team entities (name, sport, external links) |
| IPTC Sport Schema | `sport` | `https://sportschema.org/ontologies/main/` | The team entity type (`Team`) and the competition structure behind seasons, where an entity directory exposes them |
| Open Sports Profile | `osp` | `https://opensportsprofile.org/ns#` | The fan relationship and its properties (the only terms OSP itself defines) |

### 3.1 How each concept maps

| OSP concept | Schema.org | Sport Schema | Wikidata | OSP-defined |
|---|---|---|---|---|
| Profile document | `schema:ProfilePage` | — | — | — |
| Profile owner | `schema:Person` (via `schema:mainEntity`) | `sport:Agent` is a participant in an event; not used for fans | — | — |
| List of fan relationships | — | — | — | `osp:fandom` |
| Fan relationship | — | — | — | `osp:FandomRelationship` |
| Team reference (in a profile) | — | — | The team's item IRI, by default | `osp:team` (the pointer; absent on a bare team) |
| Team display name (in a profile) | — | — | — | `osp:teamName` |
| Team sport hint (in a profile) | — | — | The sport's item IRI, in `osp:sportId` | `osp:sport` (readable), `osp:sportId` (identifier) |
| Team (the entity the IRI identifies) | `schema:SportsTeam` | `sport:Team` | An item for the team | — |
| Team's own name and links (on the entity) | `schema:name`, `schema:sameAs` | — | Label, other identifiers | — |
| Team's sport (on the entity) | `schema:sport` | `sport:sport` on a `sport:Competition`, not on the team (OSP deviates, §3.2) | `sport` statement (P641) | — |
| `current_fan` / `former_fan` | — | — | — | `osp:CurrentFan`, `osp:FormerFan` |
| Seasons | — | `sport:Competition` (name = season label) | — | `osp:seasons` (labels only), with `osp:from`, `osp:to`, `osp:ongoing` |
| Reason | — | — | — | `osp:reason` |

Schema.org has no "fan of" relationship, and Sport Schema models participants in sporting events rather than audiences, so the relationship class is defined by OSP and links *to* entities defined elsewhere.

### 3.2 Team entities

A team in a profile is referenced by an IRI in `osp:team`, together with a display name in `osp:teamName` (§4.3). A team that has no IRI at all can be written as a bare team (below).

The IRI SHOULD be the team's Wikidata item (`http://www.wikidata.org/entity/Q…`) where one exists. Where none exists, it SHOULD identify a team entity published by an entity directory (§7). A directory entity SHOULD be typed with both `schema:SportsTeam` and `sport:Team`, so that consumers of either vocabulary can understand it. Wikidata items are not typed that way; a consumer that needs those types derives them from the item's `instance of` and `sport` statements.

#### Sport belongs to the team entity

A team entity represents a team in **one sport**. UC Davis Aggies football and UC Davis Aggies men's basketball are two entities with two IRIs. A team entity MUST state its sport (`schema:sport` on a directory entity; the `sport` statement on a Wikidata item).

A relationship MAY also carry the sport in `osp:sport`, so that a profile says which sport a team plays without anyone resolving the IRI. It is a display hint, like `osp:teamName`: if it disagrees with the entity the IRI identifies, the entity is authoritative. It is free text (for example `"American Football"`). To make sports comparable, a relationship MAY also carry `osp:sportId`, the IRI of the sport's Wikidata item (for example `http://www.wikidata.org/entity/Q41323` for American football). When `sportId` is present, consumers SHOULD compare sports by it and use the text only for display; where there is no suitable Wikidata item, `sportId` is omitted and the text stands alone. Like the other hints, `sportId` yields to the entity if the two disagree.

A relationship MUST name a specific team in a specific sport ("a UC Davis fan, but just for football" points at the football team). There is no "fan of the whole school or club" form: an organization that fields several teams is not itself a valid target, because a person who attended a university or follows a club is rarely a fan of every one of its teams. A person who supports several teams of the same organization lists each one as its own relationship.

Sport Schema places `sport` on a `sport:Competition` and not on the team. OSP requires it on the team entity so a fan reference is unambiguous. A directory MAY still publish the competition structure underneath (§4.5, §7).

#### Bare teams

A team with neither a Wikidata item nor a directory entry, such as a school, club or recreational team, can be written as a **bare team**: a relationship with no `osp:team`, identified only by `osp:teamName` and `osp:sport`. Both are then required. The name should be specific enough to tell the team apart, for example including the school or town.

A bare team has no identity beyond its name and sport, so applications cannot reliably tell that two profiles mean the same bare team. A directory that later publishes an entity for the team lets the person replace the bare team with an `osp:team` IRI.

#### Identity and equivalents

The IRI used in `osp:team` is the canonical identifier. Equivalent identifiers (other Wikidata items, official sites, directory IRIs) are expressed on the *entity*, with `schema:sameAs` on a directory entity or as identifier statements on a Wikidata item, not in each profile.

Wikidata items can be merged. A consumer that dereferences a Wikidata IRI SHOULD follow redirects, and a profile whose IRI has been merged remains valid.

#### Relocated and renamed franchises

Each identity of a franchise that Wikidata models as its own item is a separate target. In the cases checked, the Seattle SuperSonics (Q235326) and the Oklahoma City Thunder (Q180950) are different items, as are the Arizona Coyotes (Q206312) and the Utah Mammoth (Q125520712). A person who supported the Sonics and stopped when they left is a `former_fan` of the Seattle SuperSonics, not of the Thunder. Where Wikidata does not separate the identities, a profile can only point at the single item, and OSP does not try to split it.

## 4. Data model

```text
Profile (schema:ProfilePage)
└── mainEntity: Person (schema:Person)
    └── osp:fandom[]: FandomRelationship (osp:FandomRelationship)
        ├── osp:team          IRI of a team entity          (required, unless a bare team)
        ├── osp:teamName      string, display name          (required)
        ├── osp:sport         string, display hint          (required for a bare team)
        ├── osp:sportId       IRI of a Wikidata sport item  (optional)
        ├── osp:relationship  CurrentFan | FormerFan        (required)
        ├── osp:seasons       [ SeasonRange ]               (optional)
        └── osp:reason        string                        (optional)
```

### 4.1 Profile

| Property | Type | Required | Notes |
|---|---|---|---|
| `@context` | JSON-LD context | MUST | See §5 |
| `@type` | `"ProfilePage"` | MUST | |
| `osp:version` | string | MUST | `"0.1"` for this version |
| `dateModified` | ISO 8601 date-time | SHOULD | Maps to `schema:dateModified` |
| `mainEntity` | Person | MUST | Exactly one |

### 4.2 Person

| Property | Type | Required | Notes |
|---|---|---|---|
| `@type` | `"Person"` | MUST | |
| `@id` | IRI | SHOULD | Stable identifier for the profile owner, normally the canonical URL where the profile is published (see below) |
| `name` | string | MAY | Display name |
| `url` | IRI | MAY | |
| `sameAs` | array of IRI | MAY | Other identities of the same person (a personal site, Mastodon, GitHub). Maps to `schema:sameAs` |
| `osp:fandom` | array of FandomRelationship | MUST | May be empty |

#### Identifying and deduplicating people

A profile that is published at a URL SHOULD use that URL as the `@id` of its Person. Whoever controls the URL controls the profile, and the identifier carries nothing sensitive. A profile that has no published URL, such as an exported file, MAY omit it.

Two profiles are treated as the same person when they share an `@id`, or when each lists the other's `@id` in `sameAs` (or both list a common identity). One-way claims are weaker evidence than mutual ones, and consumers SHOULD NOT merge profiles on a single unconfirmed `sameAs`.

A profile MUST NOT contain the owner's email address, or a hash of it. A shared profile is meant to be copied, and an email in it is scraped, abused and linked to a person who only wanted to share their teams. An application that wants to match an imported profile to an existing account does so with its own account data, which is not part of the format. Consumers SHOULD drop an email property if they find one.

### 4.3 FandomRelationship

| Property | Type | Required | Notes |
|---|---|---|---|
| `@type` | `"osp:FandomRelationship"` | MUST | |
| `osp:team` | IRI | MUST, unless a bare team | Team entity IRI. One team in one sport (§3.2). Omitted only on a bare team, which then needs `osp:sport` |
| `osp:teamName` | string | MUST | Human-readable name of the team, so a profile can be read and shown without resolving the IRI. A display hint only: if it disagrees with the entity the IRI identifies, the IRI is authoritative and consumers SHOULD prefer the entity's name when they can resolve it |
| `osp:sport` | string | MUST on a bare team, otherwise MAY | The team's sport as a human-readable hint, so a profile says what sport a team plays without resolving the IRI. A display hint only: if it disagrees with the entity, the entity is authoritative (§3.2) |
| `osp:sportId` | IRI | MAY | Wikidata item IRI of the sport, so sports can be compared without matching text. When present, consumers SHOULD compare by it. A hint like `osp:sport`: the entity is authoritative if they disagree |
| `osp:relationship` | `"current_fan"` or `"former_fan"` | MUST | Controlled vocabulary, see §4.4 |
| `osp:seasons` | array of SeasonRange | MAY | See §4.5 |
| `osp:reason` | string | MAY | Free text, no markup. Consumers SHOULD allow at least 500 characters |

A profile MAY contain more than one relationship for the same team (for example, a former fan who still follows the team passively, or a person who stopped being a fan and then returned). Each relationship stands alone; consumers MUST NOT assume one supersedes another, and the spec does not require overlapping entries for the same team to be consistent.

### 4.4 Relationship vocabulary

| JSON value | IRI | Meaning |
|---|---|---|
| `current_fan` | `osp:CurrentFan` | The person supports this team now. How actively they follow it is not part of the value (it can be said in `reason`) |
| `former_fan` | `osp:FormerFan` | The person used to support this team and no longer does |

Future versions MAY add values. Consumers MUST ignore relationship values they do not recognize rather than rejecting the profile.

### 4.5 SeasonRange

Seasons are always an array of ranges, which covers both a continuous span and a set of individual years.

| Property | Type | Required | Notes |
|---|---|---|---|
| `from` | season | MUST, unless `ongoing` is `true` | When `ongoing` is `true` and `from` is omitted, the start is unspecified: the person is a fan now and gives no starting season |
| `to` | season | MAY | Omitted means a single season (`from` only), unless `ongoing` is `true`. MUST NOT be present when `ongoing` is `true` |
| `ongoing` | boolean | MAY | Default `false`. Only valid on `current_fan` |

A *season* is a label string that follows how the league itself names its seasons:

- **Single-year seasons** (e.g. MLB, NFL) use a four-digit year: `"2012"`.
- **Split-year seasons** (e.g. NHL, NBA, most European football) use the start year, a hyphen, and the last two digits of the end year: `"2011-12"`. Across a century boundary the end year keeps its two digits: `"1999-00"`.

The pattern is `^\d{4}(-\d{2})?$`. A range's `from` and `to` SHOULD use the same form. Ordering is by the four-digit start year, so `"2011-12"` sorts after `"2010-11"`, and a range from `"1996-97"` to `"2011-12"` includes every season in between. A `from` that sorts after its `to` is invalid.

Examples:

```json
[{ "from": "1996-97", "to": "2011-12" }]
```

```json
[{ "from": "2010" }, { "from": "2012" }, { "from": "2014" }]
```

```json
[{ "ongoing": true }]
```

```json
[{ "from": "2005", "ongoing": true }]
```

Because the label follows the league's own convention, nothing in this specification can check that a fan used the right form for a given sport; a validator can only check the pattern.

#### Relationship to Sport Schema

Sport Schema has no `Season` class. It models a grouping of events by time as a `sport:Competition`, and OSP follows that: **a season is a `sport:Competition`**, and the season label is that competition's `name`. For example, the NHL's 2011–12 season is a `sport:Competition` named `"2011-12"` that belongs to the NHL.

The profile itself stores only the label, so it stays human-writable and does not depend on a directory. An entity directory MAY publish the corresponding `sport:Competition` entities (§7) so applications can resolve a label to concrete dates, standings or events. Because the same label recurs across leagues (every league has a "2011-12"), a label is only meaningful together with the team it is attached to, whose league determines which competition it denotes. Seasons therefore carry no competition IRI in 0.1.

## 5. JSON-LD context

The normative context is published at `https://opensportsprofile.org/v0.1/context.jsonld`. Its contents:

<!-- BEGIN context.jsonld (generated by scripts/sync-spec.py; edit the file, not this block) -->
```json
{
  "@context": {
    "@version": 1.1,
    "@vocab": "https://schema.org/",
    "osp": "https://opensportsprofile.org/ns#",
    "version": "osp:version",
    "fandom": {
      "@id": "osp:fandom",
      "@container": "@set"
    },
    "FandomRelationship": "osp:FandomRelationship",
    "team": {
      "@id": "osp:team",
      "@type": "@id"
    },
    "teamName": "osp:teamName",
    "sport": "osp:sport",
    "sportId": {
      "@id": "osp:sportId",
      "@type": "@id"
    },
    "relationship": {
      "@id": "osp:relationship",
      "@type": "@vocab",
      "@context": {
        "@vocab": "https://opensportsprofile.org/ns#",
        "current_fan": "osp:CurrentFan",
        "former_fan": "osp:FormerFan"
      }
    },
    "seasons": {
      "@id": "osp:seasons",
      "@container": "@set"
    },
    "from": "osp:from",
    "to": "osp:to",
    "ongoing": "osp:ongoing",
    "reason": "osp:reason"
  }
}
```
<!-- END context.jsonld -->

Because the context maps short keys to the `osp:` terms, the on-the-wire JSON uses plain `team`, `teamName`, `sport`, `sportId`, `relationship`, `seasons` and `reason`. The profile context does not define the `sport:` prefix, because a profile has no Sport Schema terms and a `sport` key would collide with it; directory entities (§7) define it in their own context.

## 6. Example profile

```json
{
  "@context": "https://opensportsprofile.org/v0.1/context.jsonld",
  "@type": "ProfilePage",
  "version": "0.1",
  "dateModified": "2026-10-06T00:00:00Z",
  "mainEntity": {
    "@type": "Person",
    "name": "Darren",
    "fandom": [
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q223507",
        "teamName": "Denver Broncos",
        "sport": "American Football",
        "sportId": "http://www.wikidata.org/entity/Q41323",
        "relationship": "current_fan",
        "seasons": [{ "from": "1997", "ongoing": true }]
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q194116",
        "teamName": "Detroit Red Wings",
        "sport": "Ice Hockey",
        "sportId": "http://www.wikidata.org/entity/Q41466",
        "relationship": "former_fan",
        "seasons": [{ "from": "1996-97", "to": "2011-12" }],
        "reason": "Huge fan of Sergei Fedorov, Brendan Shanahan, Steve Yzerman, and Nicklas Lidstrom."
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q308966",
        "teamName": "San Francisco Giants",
        "sport": "Baseball",
        "sportId": "http://www.wikidata.org/entity/Q5369",
        "relationship": "former_fan",
        "seasons": [{ "from": "2010" }, { "from": "2012" }, { "from": "2014" }],
        "reason": "I lived in the Bay Area at the time."
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q7864151",
        "teamName": "UC Davis Aggies football",
        "sport": "American Football",
        "sportId": "http://www.wikidata.org/entity/Q41323",
        "relationship": "former_fan",
        "seasons": [{ "from": "2005", "to": "2007" }],
        "reason": "Went to school there. Just the football team."
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q7864151",
        "teamName": "UC Davis Aggies football",
        "sport": "American Football",
        "sportId": "http://www.wikidata.org/entity/Q41323",
        "relationship": "current_fan",
        "seasons": [{ "ongoing": true }],
        "reason": "Follow them passively now."
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q3650742",
        "teamName": "California Golden Bears football",
        "sport": "American Football",
        "sportId": "http://www.wikidata.org/entity/Q41323",
        "relationship": "current_fan",
        "seasons": [{ "ongoing": true }]
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q334634",
        "teamName": "Los Angeles Dodgers",
        "sport": "Baseball",
        "sportId": "http://www.wikidata.org/entity/Q5369",
        "relationship": "current_fan",
        "seasons": [{ "ongoing": true }]
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q203008",
        "teamName": "Los Angeles Kings",
        "sport": "Ice Hockey",
        "sportId": "http://www.wikidata.org/entity/Q41466",
        "relationship": "current_fan",
        "seasons": [{ "ongoing": true }]
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q121783",
        "teamName": "Los Angeles Lakers",
        "sport": "Basketball",
        "sportId": "http://www.wikidata.org/entity/Q5372",
        "relationship": "current_fan",
        "seasons": [{ "ongoing": true }]
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q337377",
        "teamName": "Los Angeles Rams",
        "sport": "American Football",
        "sportId": "http://www.wikidata.org/entity/Q41323",
        "relationship": "current_fan",
        "seasons": [{ "ongoing": true }]
      },
      {
        "@type": "FandomRelationship",
        "team": "http://www.wikidata.org/entity/Q7156",
        "teamName": "FC Barcelona",
        "sport": "Association Football",
        "sportId": "http://www.wikidata.org/entity/Q2736",
        "relationship": "current_fan",
        "seasons": [{ "ongoing": true }]
      },
      {
        "@type": "FandomRelationship",
        "teamName": "Millbrook School Dragons boys basketball",
        "sport": "Basketball",
        "sportId": "http://www.wikidata.org/entity/Q5372",
        "relationship": "former_fan",
        "seasons": [{ "from": "1999-00", "to": "2000-01" }]
      }
    ]
  }
}
```

Every `team` here is a Wikidata item, and every entry carries a `teamName`, a `sport` and a `sportId`, so the profile reads without resolving anything (§4.3). The last entry is a bare team (§3.2): it has no `team` IRI, so its name and sport carry the identity. The profile owner's `name` and the bare team are illustrative.

The UC Davis and California entries point at the football teams specifically, not the schools, following §3.2. UC Davis has two entries for the same team: a `former_fan` entry for the years as a student, and a separate `current_fan` entry for following the team passively now (§4.3). Entries with `{ "ongoing": true }` and no `from` are fans now who give no starting season (§4.5).

## 7. Entity directory

OSP profiles point at team entities but do not define them. A team entity is most often a Wikidata item (§3.2). Where Wikidata has no item for a team, or a consumer wants Sport Schema typing and richer structure, an **entity directory** fills the gap: any service that publishes stable IRIs for teams and dereferences them to a JSON-LD description. A directory is optional infrastructure and not required to read a profile.

A directory entry for a team SHOULD look like:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "sport": "https://sportschema.org/ontologies/main/"
  },
  "@id": "https://entities.opensportsprofile.org/team/detroit-red-wings",
  "@type": ["SportsTeam", "sport:Team"],
  "name": "Detroit Red Wings",
  "sport": "Ice Hockey",
  "sameAs": ["http://www.wikidata.org/entity/Q194116"]
}
```

The entity that the UC Davis football entries in §6 point at looks the same way if a directory publishes it. It is one team in one sport, and the school is a separate entity:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "sport": "https://sportschema.org/ontologies/main/"
  },
  "@id": "https://entities.opensportsprofile.org/team/uc-davis-aggies-football",
  "@type": ["SportsTeam", "sport:Team"],
  "name": "UC Davis Aggies football",
  "sport": "American Football",
  "sameAs": ["http://www.wikidata.org/entity/Q7864151"]
}
```

The `sameAs` values are the teams' Wikidata items (Q194116 for the Red Wings, Q7864151 for UC Davis football). The `entities.opensportsprofile.org` IRIs are placeholders.

Requirements on a directory:

- Every team entity MUST declare its `sport`, and a team that plays in more than one sport MUST be published as one entity per sport (§3.2).
- IRIs MUST be stable. Renaming or relocating a team MUST NOT change its IRI; a rename is recorded by changing `name`.
- If an entity is merged into another, the old IRI SHOULD keep resolving and SHOULD point to the survivor with `schema:sameAs` or an HTTP 301.
- A directory entity SHOULD record its Wikidata item with `schema:sameAs` where one exists.
- Any directory MAY be used. `entities.opensportsprofile.org` is a *reference* directory, not a mandatory one.

#### Sport Schema structure for league, club and sport

In IPTC Sport Schema 1.1 a team is a `sport:Team` (a `sport:Agent`), and the ontology gives the team itself no league, club or sport property. Those links are made through a `sport:TeamMembership`, which points to the team with `sport:member`, to a club with `sport:membershipOf`, and to a competition with `sport:competitionMembership`. A league is a recurring `sport:Competition`. The sport is `sport:sport` on that competition, whose value is a `skos:Concept` (the ontology recommends IPTC Media Topics).

A directory that wants to publish this structure MAY use those terms, and a directory entity MAY link to its memberships. OSP does not depend on it. On a directory entity, the team's sport stays `schema:sport`, as in the examples above, so that a consumer gets the sport from the entity without following a membership to a competition (§3.2).

## 8. Out of scope

- **Presentation.** Logos, colors, wordmarks, stadium photos. Hosted applications look these up from the entity's identity; OSP profiles MUST NOT embed them.
- **Participation history** (played, coached, worked for). Planned for a later version. The intended approach is an OSP-defined participation relationship that uses seasons, not dates, can name teams that have no entity, and can optionally reference an equivalent Sport Schema membership (such as `IndividualMembership`) where one exists.
- **Verification** of any claim, including that a profile belongs to the person it names.
- **Contact details.** Email addresses and other private identifiers are not part of a profile (§4.2).
- **Privacy and visibility controls**, authentication, OAuth and federation.
- **Organizations as fan targets.** A school, club or athletic program that fields several teams is not a valid `osp:team` (§3.2).
- **Individual athletes and non-team entities** (leagues, venues, drivers) as fan targets.
- **Engagement level.** Whether someone follows a team closely or passively is not a field; it can be said in `reason`.

## 9. Validation and processing

A conforming consumer:

1. MUST accept the profile as JSON; JSON-LD processing is OPTIONAL.
2. MUST reject a profile missing `version`, `mainEntity`, or any required property in §4, including `osp:teamName` on every relationship, and `osp:team` unless the relationship is a bare team (§3.2), which MUST then carry `osp:sport`.
3. MUST reject a season range that breaks the rules in §4.5 (missing `from` without `ongoing`, `to` together with `ongoing`, `ongoing` on a `former_fan`, or a `from` after its `to`).
4. MUST ignore unknown properties and unknown `relationship` values.
5. MUST NOT dereference `team` IRIs as a condition of accepting a profile (a directory or Wikidata being offline must not invalidate a profile).
6. SHOULD preserve unknown properties on round-trip.

A JSON Schema for the structural rules is at `schema/v0.1/profile.schema.json`. It cannot express rules that compare values (a season range whose `from` is after its `to`), so a validator that adds those checks will be published with the specification. It is not yet written.

## 10. Versioning

The `version` property is `MAJOR.MINOR`. During 0.x, minor versions may add fields and values but SHOULD NOT remove or change the meaning of existing ones. The context URL is versioned (`/v0.1/context.jsonld`) and a published version is immutable.

## 11. Open questions

None at present.

## 12. References

- [Schema.org SportsTeam](https://schema.org/SportsTeam) and [SportsOrganization](https://schema.org/SportsOrganization)
- [IPTC Sport Schema](https://iptc.org/standards/sport-schema/), ontology IRI `https://sportschema.org/ontologies/main/`, [source repository](https://github.com/iptc/sport-schema); licensed CC-BY 4.0
- [Wikidata](https://www.wikidata.org/), source of the default team identifiers
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/)

## 13. License

Copyright (c) 2026 Darren Alfonso and the Open Sports Profile contributors.

- This specification (the prose, tables and examples in this document) is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0). The full text is in `LICENSE-SPEC`.
- The JSON Schema (`schema/`), the JSON-LD context, the example profiles and any validator code are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). The full text is in `LICENSE`.

The names "Open Sports Profile" and "OSP" are not licensed by either of the above.
