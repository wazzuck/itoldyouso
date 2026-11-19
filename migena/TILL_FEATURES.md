# EGGI'S — Till Feature Reference

**Summary:** this is the reference for every feature of the SumUp Point of
Sale (POS) app on the shop's Android device, what each one does, and what
state it is in on 19 November 2026.

Read `TILL_PROCEDURES.md` for step-by-step tasks. This document answers
"what is this screen for?"

## How to read the status

1. **Seen** — opened on the device and described from the screen.
2. **Offer only** — the device shows an introduction and a "Get started"
   button. The feature is not switched on for this account.
3. **Plus** — labelled as a POS Plus feature. Needs the paid plan.
4. **Web** — managed on the SumUp website (me.sumup.com), not on the till.
5. **Not confirmed** — not opened, or the screen did not finish loading.

---

## 1. Cart and checkout (main till screen)

1. **Category tabs** — filters the item tiles by category. "All" shows
   everything. *Seen.*
2. **Search (magnifier)** — finds an item by name. *Seen.*
3. **New item (pencil)** — starts a new item from the till.
   *Not confirmed.*
4. **Item tiles** — tap to add the item to the cart. The price is shown
   on each tile. *Seen.*
5. **Cart header** — shows the order code, for example E-003, and the
   timing label. *Seen.*
6. **Cart lines** — one line per item, with quantity and price. *Seen.*
7. **Add course** — creates a course, so items can be sent to the kitchen
   in stages. *Plus.*
8. **Park order** — saves the order open and unpaid. *Seen.*
9. **Card** — opens the payment methods screen. *Seen.*
10. **Chevron beside Card** — opens the split and all-payment menu.
    *Seen.*
11. **Three dots menu** — manual price entry, add discount, add order
    note, clear cart. *Seen.*
12. **Add order note** — free text for the kitchen, up to 300 characters.
    *Seen.*
13. **Clear cart** — empties the cart. Only for a cart not yet sent.
    *Seen.*
14. **Manual price entry** — types in a price that is not on the menu.
    *Seen (menu).*
15. **Add discount** — applies a discount to the cart. *Seen (menu).*
16. **Split** — splits the bill between payments. *Seen (menu).*

---

## 2. Payment methods

1. **Tap to Pay** — takes a contactless card or phone on the device's own
   NFC chip. *Not available on this device (section 13).*
2. **Card Reader** — sends the amount to the Solo card machine. *Seen.*
3. **Payment Links** — creates a link or QR code the customer pays
   online. *Seen.*

Cash is not a payment method on this screen. Cash is counted into the
till tray (see `TILL_PROCEDURES.md`, section 8.4).

---

## 3. Open orders (bell icon)

1. **Open order list** — every parked order, with its code, time and
   items. *Seen.*
2. **Search** — finds an open order by code, item or amount. *Seen.*
3. **New order** — starts a new order. *Seen.*
4. **Use courses banner** — explains courses and links to POS Plus.
   *Plus.*

---

## 4. Sales (receipt icon)

1. **Today's sales total** — the total for the day, with a link to the
   detail. *Seen.*
2. **Sales list by date** — each sale with its items, time and result.
   *Seen.*
3. **Search and filter** — finds a sale; filters by date or result.
   *Seen (search).*
4. **Sale detail** — the items, the VAT and the payment. *Seen.*
5. **Receipt button** — reprints the customer receipt. *Seen.*
6. **Payment line** — the card reference, time and result. *Seen.*

A sale that did not complete shows "Unsuccessful" in red.

---

## 5. Reporting (chart icon)

1. **Periods** — Today, Yesterday, This week, This month, Custom. *Seen.*
2. **Sales total and count** — the total and the number of sales.
   *Seen.*
3. **Items** — number of items sold in the period. *Seen.*
4. **Average sale** — total divided by the number of sales. *Seen.*
5. **Refunds** — money refunded in the period. *Seen.*
6. **Discounts** — money taken off by discounts. *Seen.*
7. **Best-selling items** — the items sold most. *Seen.*
8. **Busiest period** — sales by hour, and the busiest time. *Seen.*
9. **Payment methods** — how customers paid. *Seen.*
10. **Insights, Revenue, Payouts, Fee invoice, Payments** — detailed
    tabs. *Seen (names).*
11. **Go there now** — opens the full reports on the website. *Web.*

The figures show zero until a successful sale is made.

---

## 6. Items (price-tag icon)

1. **Library** — the full list of items with their prices. Search, sort
   and filter. *Seen.*
2. **Add item** — creates a new item. *Seen (button).*
3. **Categories** — the till categories and how many items each holds.
   *Seen.*
4. **Inventory** — stock tracking. Filter by low stock, sold out and
   tracked. *Seen.*
5. **Modifiers** — modifier sets and their choices, such as milk or
   bread. *Seen.*
6. **Option sets** — variations such as size or colour. *Seen.*
7. **Deposits** — container deposits, for example bottles. *Plus.*
8. **Discounts** — named discounts. The shop has 10%, 20% and 50%.
   *Plus.*
9. **Create modifier set, option set or discount** — creates a new
   group. *Seen (buttons).*

**Clean-up needed:** the modifier list still holds "(Example) Toppings",
and the option sets still hold the sample "Color" and "Size" sets. The
checklist already asks for the toppings set to be deleted.

---

## 7. Tools (grid icon)

The Tools screen is a menu. Each entry opens its own feature.

1. **Items** — opens section 6. *Seen.*
2. **Employees** — staff accounts and their roles. *Seen (section 8).*
3. **Customers** — customer list for invoices and loyalty. *Seen
   (section 9).*
4. **Reporting** — opens section 5. *Seen.*
5. **Online Store** — builds a free online shop (Webspace). *Offer only.*
6. **Bookings** — appointment booking. *Offer only.*
7. **Loyalty** — reward programmes. *Not confirmed (did not finish
   loading).*
8. **Gift Cards** — sells and redeems gift cards. *Not confirmed.*
9. **Card readers** — pairs and buys card machines. *Not confirmed.*
10. **Tap to Pay** — settings for contactless on the device. *Seen
    (section 13).*
11. **Payment links** — creates customer payment links. *Seen (section
    2).*
12. **Cash Advance** — loans repaid from sales. *Offer only.* The
    eligibility rules are shown: complete identity checks, take card
    payments for at least three months, and use the SumUp Business
    Account and card. Meeting them does not guarantee an offer.
13. **Invoices** — creates and sends invoices. *Not confirmed.*
14. **Expenses** — tracks spending and exports it for tax. *Offer only.*

---

## 8. Employees

1. **Members** — lists everyone who can log in, with role and status.
   *Seen.*
2. **Search, Role and Status filters** — finds a member. *Seen.*
3. **Add team member** — invites a person by e-mail. *Seen (button).*
4. **Roles** — the permission sets a member can have. *Seen (tab).*
5. **Edit team member** — changes a member's role. *Seen (panel).*

On 19 November 2026 the only member is the account owner, as
Administrator. The six staff e-mail addresses are still needed (see the
checklist). Each staff member needs their own address to be invited.

---

## 9. Customers

1. **Customer list** — names and contact details of customers. *Seen
   (empty).*
2. **Add customer** — adds a customer by hand. *Seen (button).*
3. **Invoice customers note** — invoice customers are kept in the
   Invoices directory, not on this list. *Seen.*

The list is empty. Customers are added by hand, or created from invoices.

---

## 10. Profile (person icon, bottom left)

The Profile menu opens from the person icon at the extreme bottom left of
the till screen and scrolls through every device, checkout, tax, team,
accessory and account setting. All menus and submenus below were inspected
on 19 November 2026 (except **Log out**, which was not tapped).

### 10.1 Account and security

1. **Account header** — shows the account name (`Migena Lika`) and merchant
   code (`MW82CKEA`). Display header only; tapping it does not open a
   submenu. *Seen.*
2. **24/7 priority support** — opens the Priority Support web view. *Seen.*
3. **Inbox** — messages from SumUp with an unread badge (`1` on 19 November
   2026). Lists account alerts including "ID verification needed", mobile
   number verification and profile setup. *Seen.*
4. **Login and security** — *Seen.*
   - **Link device** ("Increase your account security"): links this device
     to the account to confirm important activities.
   - **Login credentials**: shows **Mobile phone** (masked, with **Change**)
     and **Email** (with **Change**).
   - Password note: directs you to `me.sumup.com` to change your password.

### 10.2 Payouts

5. **Payouts** — summary of **Payout destination** (`SumUp Business
   Account`, "Fastest payouts") and **Frequency** (`Next-day payouts`),
   plus **Recent payouts** (`No payouts yet`), **Go to payout history**,
   and top-right **Report** and **Settings** icons. *Seen.*
6. **Payout settings** — shows the current payout destination (`SumUp
   Business Account`, marked `Current`) and the **7am payouts every day**
   toggle (*on* — next-day payouts by 7am, 365 days a year). *Seen.*

### 10.3 Payment methods

7. **Tap to Pay** — **Tap to Pay** toggle (*on*) with device readiness
   checks: **NFC not available** (red — Near Field Communication (NFC) is
   unsupported on this device; see section 13), **SumUp App version**,
   **Developer options** and **Android version**. *Seen.*
8. **Card Reader** — **Accept payments with card reader** toggle (*on* —
   shows Card Reader at checkout) and **Connect card reader** button.
   *Seen.*
9. **Other payments** — introduces adding non-SumUp payment methods (such
   as bank transfer or digital payments) to checkout so every payment is
   recorded in one place, with a **Set up** button. *Offer only.*

### 10.4 Orders

10. **Order types** *(New)* — **Use order types** toggle (*off*): applies
    an order type at checkout to charge the right prices and Value Added
    Tax (VAT), and prints it on order tickets. *Seen.*
11. **Multiple orders** *(New)* — *Seen.*
    - **Accept multiple orders** toggle (*on*): open, park and manage
      orders before taking payment (running tabs or multiple tables).
    - **Floor plan** toggle (*off*): create and manage a restaurant floor
      plan and place orders on tables.
    - **Sync orders across devices — Sync this device** toggle (*off* on
      this device): view and edit open orders on synced devices in real
      time.
12. **Courses** *(New)* — shows a notice that courses work best with
    multiple orders and order tickets turned on, **Use courses** to hold
    or fire kitchen courses separately, and a **How courses work** guide
    ("Send the next course"). *Seen.*

### 10.5 Checkout

13. **Split Payments** *(New)* — **Split payments** toggle (*on* — accept
    multiple payments per order), plus three **Split options** toggles:
    **Custom amounts** (*on*), **Equal parts** (*on*) and **Items** (*on*
    — each customer pays for their own items). *Seen.*
14. **Tipping** — **Standard tipping** toggle (*off*): lets customers add
    gratuity at payment. *Seen.*

### 10.6 Taxes

15. **VAT** (opens **Taxes** screen) — *Seen.*
    - **Charge VAT** toggle (*on*), with **Learn more**.
    - **Default rate**: `VAT 20%` (with **Edit**; pre-selected at checkout
      and in the Online Store).
    - **VAT Rates**: `No VAT (-)`, `VAT 0%`, `VAT 5%` and `VAT 20%` (with
      **Edit** to change or add rates).
    - **Prices**: **Show prices including VAT** toggle (*on*).

### 10.7 Sales & cash tracking

16. **Till management** — *Seen.*
    - **Manage till** toggle (*off*): manually open or close the till at
      the start and end of the trading day, and generate Z Reports when
      closing.
    - **Manage cash** toggle (*off*): record the starting cash float and
      track cash movements for cash reconciliation.

### 10.8 Your team

17. **Employees** — opens the Employees management screen (see section 8).
    *Seen.*
18. **PIN login** — **Use PIN login** toggle (*off*): lets each employee
    sign in with a 4-digit Personal Identification Number (PIN) for faster
    switching on shared devices and activity tracking. *Seen.*

### 10.9 Plans & fees

19. **Your plans** — opens the **Your plans** embedded web view for
    subscription details. *Web.*
20. **Card payment summary** — opens the **Annual fees summary** embedded
    web view. *Web.*

### 10.10 Accessories

21. **Printer settings** — **Use printer** toggle (*off* on this device):
    enables printed customer receipts and cash drawer management. *Seen.*
22. **Barcode scanner** — **Use barcode scanner** toggle (*on*), connected
    device status (`ChromeOS Keyboard`, Universal Serial Bus (USB),
    `Ready`), **Switch scanner** button and top-right **Info** icon.
    *Seen.*

### 10.11 Support

23. **Support** *(Prio)* — *Seen.*
    - **Get in touch**: **Ask AI Support** for quick self-service
      troubleshooting.
    - **Priority support**: **Chat with an agent** (`Online`) and **Call
      us** (displays phone hours, e.g. `Reopens at 08:00 AM`), plus
      top-right **Conversation history**.
    - **Useful self-services**: **Free device replacement** (`Resolution
      time: 1 min`) and **Change phone number**.

### 10.12 For SumUp fans, privacy, legal and log out

24. **Refer a friend** (opens **Invite** screen) — referral offer ("Get
    £60 when you refer SumUp"; friend gets up to £50 off their first
    payment device), **Share link**, **Your rewards** and top-right
    **Terms**. *Seen.*
25. **Like this app? Tell others** — opens the SumUp app listing in Google
    Play Store. *Seen.*
26. **Cookies Preferences** — opens the **Cookies Preferences** embedded
    web view. *Web.*
27. **Legal information — Terms & Conditions** — opens SumUp Terms &
    Conditions on `sumup.com` in the browser. *Web.*
28. **Legal information — Privacy policy** — opens SumUp Privacy Policy on
    `sumup.com` in the browser. *Web.*
29. **Log out** — signs out of the SumUp account on this device (not
    tapped during inspection). *Seen (name).*

---

## 11. Settings and business profile (web)

These are on the website, not the till.

1. **Business information** — registered name, trade name, address.
   *Web.*
2. **Business profile** — name on SumUp listings, statement descriptor
   and phone. *Web.*
3. **VAT** — VAT rates charged. *Web.*
4. **Plans and fees** — the current plan and its fees. *Web.*
5. **Employees** — staff profiles (also on the till). *Web.*

The registered name still reads "Greens Kitchen". Only SumUp Support can
change it (checklist, section 8.5).

---

## 12. Printing and kitchen (checklist)

The printing and order-sending settings are per device and are not in
the till's menu. They are covered by checklist Rules U3 and U4:

1. The "Till" printer prints POS Lite receipts.
2. The Solo's counter printer prints standalone card receipts.
3. The Terminal prints order tickets only where "Print order tickets" is
   on.

---

## 13. Known limits on this device

1. **Tap to Pay: not available.** The device reports "NFC not available",
   so contactless payment on this device will not work. Use the Solo.
2. **Card readers** and **Loyalty** did not finish loading during this
   check, so they are not confirmed.
3. **Refunds** and **split bills** have not been used on a real sale.

---

## 14. Not yet checked

1. Gift Cards and Invoices (did not load in this check).
2. Loyalty (did not load).
3. Items: creating and editing an item; deleting a category.
4. Courses, the Z-report and the kitchen send button.

These need a manager's test sale or a run-through before the document can
be called complete.

---

## Source

This reference was compiled from the POS app on the shop's Android device
on 19 November 2026. Where a screen did not load or was not opened, the
status says so rather than guessing.
