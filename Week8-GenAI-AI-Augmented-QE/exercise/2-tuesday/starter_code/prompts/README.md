# ShopFront Prompt Library

Prompts the ShopFront QE team uses with Claude for test design and debugging.
Every prompt is a versioned file. Use the latest version unless its notes say otherwise.

## How to use a prompt
1. Open the latest version and copy the text inside its `## Prompt` block.
2. Paste it into a **fresh** Claude chat with any material it asks for. Synthetic or approved material only.
3. Save the reply in `evidence/` and run the "Check with" command from the header.
4. Review the reply yourself. A passing check is a first filter, not approval.

## Index

| ID | File (latest) | Area | Technique | Output | How the output is checked |
|---|---|---|---|---|---|
| TD-1 | | test design | | | |
| TD-2 | | test design | | | |
| TD-3 | | test design | | | |
| DB-1 | | debugging | | | |
| DB-2 | | debugging | | | |

## Rules for this library
- One change per new version. Keep old versions; never edit a version that has evidence.
- Commit message format: `prompts: <what changed> (<ID> v<N>)`.
- (Add the team rules you learned today: what never goes into a prompt, what is never accepted from a reply.)
