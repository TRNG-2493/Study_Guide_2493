# Materials (synthetic, safe to paste into Claude)

`inputs/` holds candidate inputs for your sample pairs and your Claude dry run. They use the
three fields every requirements agent needs (`story_id`, `title`, `acceptance_criteria`).
If your input contract adds per-call options (for example a limit on findings), add them
to your pair inputs; the default must be in your input schema.

| File | What it is good for |
|---|---|
| `us420.json` | Wednesday's gift card story: several real problems (case, spaces, "quickly", shipping/tax) |
| `us430.json` | A story with a contradiction (AC2 vs AC3) and a missing rule (a 6th address?) |
| `us440.json` | A well-written story. Is "no findings" a legal, honest answer in your contract? |
| `us450.json` | Placeholders only: nothing can be reviewed. What does your agent say? |
| `bad_input.json` | Malformed request: must be rejected before any model call |
| `out_of_scope.json` | Asks for something other than a requirements review |

Write each pair's expectations from the story text BEFORE you show the story to Claude.
