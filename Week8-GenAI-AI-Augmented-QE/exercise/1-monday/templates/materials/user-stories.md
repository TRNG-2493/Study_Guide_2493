# ShopFront user stories (synthetic, safe to paste into Claude)

These stories are deliberately written the way real backlog items often arrive: short, a little vague, and missing details. That is the point.

## US-101 Promo codes at checkout
As a registered shopper I want to enter a promo code at checkout so that I get a discount.
- One promo code per order.
- Promo codes expire.
- The discount is shown before payment.

## US-102 Guest checkout
As a visitor I want to check out without creating an account so that I can buy quickly.
- Guests enter an email address for the receipt.
- Guests cannot see order history.
- The checkout should be fast.

## US-103 Saved addresses
As a registered shopper I want to save up to a few delivery addresses so that I do not retype them.
- The default address is pre-selected.
- Addresses can be edited and removed.
- Shipping rules (see shipping.py) apply to the selected address.

## Registration rules (used by the data-generation probe)
| Field | Rule |
|---|---|
| username | 4-16 characters; lower-case letters, digits and hyphen; must start with a letter |
| email | exactly one `@`; domain must be `example.com` or `example.org` (reserved test domains) |
| age | whole number from 16 to 99 |
| country | `US` or `CA` only |
| marketing_opt_in | `yes` or `no` |
