# SumUp Migration Handover (MW82CKEA → M8ZXCMPQ)

Status as at 2026-11-27 22:50 UTC. Passwords are not copied here; read
them from `sumup_password.txt` (line numbers given below).

## 1. Environment

| Item | Value |
| --- | --- |
| Old account | `Migena Lika`, merchant code `MW82CKEA` |
| New account | `EGI'S BRUNCH LIMITED` (`Egzon Qelia`), `M8ZXCMPQ` |
| Credentials | `/home/neville/itoldyouso/migena/sumup_password.txt` |
| Settings stock-take | `sumup_settings_stocktake.md` (same folder) |
| Raw menu export | `~/Downloads/2026-11-18_22-29-02_items-export_MW82CKEA.csv` |
| Clean import CSV | `~/Downloads/items-import-ready-new-account.csv` |
| Android app | `com.kaching.merchant` via `adb -s emulator-5554` |
| Android login | Signed in to `M8ZXCMPQ` |
| Container Chrome | `/opt/google/chrome/chrome`, DevTools enabled |
| Thunderbird mail | `~/.thunderbird/ju23ktc2.default-default/Mail/` |
| Employee inboxes | `imap.purelymail.com-<name>/INBOX` (mbox files) |

Note: direct IMAP login with the SumUp passwords fails (they are
SumUp passwords, not mail passwords). Read codes from the local
Thunderbird mbox files instead; Thunderbird must be running to sync.

## 2. Completed

1. Full stock-take of the old account (every setting, floor plan,
   22 categories, 21 modifier sets with prices and rules, discounts,
   option sets, 223 item/variant rows).
2. New account settings, set in the Android app and verified:
   1. Cash payments ON; Calculate change ON.
   2. Multiple orders ON; Floor plan ON; Sync this device ON.
   3. Split payments ON (custom amounts, equal parts, items).
   4. VAT ON, default 20 %, rates No VAT / 0 % / 5 % / 20 %,
      prices shown including VAT.
   5. Use printer ON; Use barcode scanner ON.
   6. Order types, Courses, Tipping, Till management, PIN login
      left OFF (as on old account).
3. Floor plan: Indoors (tables 1–12) and Outdoors (13–18). The
   operator fixed the layout by hand; do not touch it.
4. Discounts 10 %, 20 %, 50 % and option sets Color / Size present.
5. All 20 active modifier sets created with exact options and prices.
6. Menu CSV imported on me.sumup.com (job
   `de15d740-4154-4bf7-9ed5-00026ac9fb8a`): 189 items plus 34
   variants (223 rows) in 22 categories, with colours, VAT, modifiers.
7. Six Cashier invitations sent to `egi`, `zina`, `laura`, `yian`,
   `luan`, `yusuf` `@itoldyouso.tech`. Managed users with preset
   passwords were refused by SumUp (HTTP 403, merchant profile not yet
   verified), so the invitation route was used.
8. Ethernet dongle advice for the POS Lite: Belkin `INC019btBK`
   (Argos 265/4492) or UGREEN 9-in-1 hub (Argos 874/1550).
9. All six employee invitations accepted; every employee shows **Active**
   on `https://me.sumup.com/en-gb/members`.
10. Modifier links verified in Android Checkout for `Americano`
    (**Coffee Extras**, **Milk**), `Eggs on Toast`
    (**Eggs on Toast Side**, **Egg Style**), and `Club`
    (**Bread Choice**).
11. Small clean-ups done: `Garden Burger Extras` now contains only
    `Add Halloumi` (£4.90), and the default `(Example) Toppings`
    modifier set has been deleted.

### 2.1 Employee invitation acceptance detail

Most of the original 19:59 UTC invites had expired by the time
acceptance was resumed, so invitations were resent from the owner
Members page and accepted with a fresh token and verification code.

| # | Email | Password line | Invite token used | Verification code |
| --- | --- | --- | --- | --- |
| 1 | `egi@itoldyouso.tech` | 5 | `inv_rytxVLNAb19CAuKvIFL6oPA3mcseQ2VTpAnM` | `926918` |
| 2 | `zina@itoldyouso.tech` | 8 | `inv_QPbMhHC0wpYFzxJrWEDQdWygQEpD4byH6eCN` | `632782` |
| 3 | `laura@itoldyouso.tech` | 11 | `inv_MUq60N1Lfp7XQe1WBHzAujIoX7vNMUurbWzf` | `871276` |
| 4 | `yian@itoldyouso.tech` | 14 | `inv_5OoG6qKBIeK3Y3vIzrF4kmaavAi1u4WtXCkf` | `985456` |
| 5 | `luan@itoldyouso.tech` | 17 | `inv_lvB9iF6gEnnLv4gne3CX1y7b8y4A0NNJRPes` | `337982` |
| 6 | `yusuf@itoldyouso.tech` | 20 | `inv_VKqGc7c3r4kELI2HJ0dxVwr45FY1apYHHdBu` | `981728` |

Notes:

- The five resent invites were sent at approximately 20:22 UTC and
  matched the tokens above.
- For `egi`, the mailbox only contains the original 19:59 UTC invite
  (`inv_rytxVLNAb19CAuKvIFL6oPA3mcseQ2VTpAnM`) and the 20:06 UTC
  verification code (`926918`); no later resent invite appears in the
  mailbox. Nevertheless, `egi` shows **Active** on the Members page.

Process followed per employee:

1. Open the invite URL in an isolated Chrome context.
2. Log in with the employee email and password.
3. Read the newest 6-digit code from the employee's Thunderbird mbox.
4. Accept the invitation, then close the context before the next
   employee.
5. Confirmed all six show **Active** on
   `https://me.sumup.com/en-gb/members`.

## 3. Outstanding

### 3.1 Operator / on-site steps (cannot be done remotely)

1. Confirm POS Plus is active: me.sumup.com → Settings → Plans.
2. Complete SumUp merchant profile verification for `M8ZXCMPQ`.
3. On the shop's POS Lite: sign out of `MW82CKEA`, sign in to
   `M8ZXCMPQ`, pair the card reader and receipt printer, run a £1
   test sale.
4. Download sales and payout history from `MW82CKEA` before access
   is closed (receivable balance was £392.93 on 27.11.2026).
