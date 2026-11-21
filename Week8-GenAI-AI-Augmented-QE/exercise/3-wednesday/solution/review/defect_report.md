# AI-assisted: Claude drafted defect report; reviewed by a.trainee 2026-10-21

**Title:** 15-character gift card code is accepted at checkout

**Severity:** High (money: an invalid code redeems a balance; no crash or data loss)

**Environment:** staging, build 4.12.0

**Steps to reproduce**
1. Build a cart with an order total of $80.00.
2. At checkout, enter the gift card code `QATEST26ABCD123` (15 characters) with a $50.00 balance.
3. Click Apply.

**Expected result:** "Gift card code not recognised" is shown and the gift card pays nothing (US-420 AC1, AC4).

**Actual result:** The gift card is applied: it pays $50.00 and $30.00 remains to pay by card.

**Notes:** Reproduced at unit level: `apply_gift_card(80, "QATEST26ABCD123", 50)` in `shopfront/giftcard_buggy.py` returns pays 50.0, remainder 30.0. 14-character and 17-character codes are rejected correctly (checked). Found by approved test TC-H1.

Corrections to Claude's draft: severity Critical changed to High; removed the unverified claim that 14-character codes are also affected (checked: they are rejected); added the requirement references and the test id.
