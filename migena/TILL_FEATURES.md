# EGGI'S — Till Feature Reference

**Summary:** this is the reference for every feature of the SumUp Point of
Sale (POS) app on the shop's Android device, what each one does, and what
state it is in on 19 November 2026.

Read `TILL_PROCEDURES.md` for step-by-step tasks. This document answers
"what is this screen for?"

## How to read the status column

1. **Seen** — opened on the device and described from the screen.
2. **Offer only** — the device shows an introduction and a "Get started"
   button. The feature is not switched on for this account.
3. **Plus** — labelled as a POS Plus feature. Needs the paid plan.
4. **Web** — managed on the SumUp website (me.sumup.com), not on the till.
5. **Not confirmed** — not opened, or the screen did not finish loading.

## 1. Cart and checkout (main till screen)

| Feature | What it does | Status |
|---|---|---|
| Category tabs | Filters the item tiles by category. "All" shows everything. | Seen |
| Search (magnifier) | Finds an item by name. | Seen |
| New item (pencil) | Starts a new item from the till. | Not confirmed |
| Item tiles | Tap to add the item to the cart. Price shown on each. | Seen |
| Cart header | Shows the order code, for example E-003, and the timing label. | Seen |
| Cart lines | One line per item, with quantity and price. | Seen |
| Add course | Creates a course, so items can be sent to the kitchen in stages. | Plus |
| Park order | Saves the order open and unpaid. | Seen |
| Card | Opens the payment methods screen. | Seen |
| Expand (chevron) | Opens the split and all-payment menu. | Seen |
| Three dots menu | Manual price entry, Add discount, Add order note, Clear cart. | Seen |
| Add order note | Free text for the kitchen, up to 300 characters. | Seen |
| Clear cart | Empties the cart. Only for a cart not yet sent. | Seen |
| Manual price entry | Types in a price that is not on the menu. | Seen (menu) |
| Add discount | Applies a discount to the cart. | Seen (menu) |
| Split | Splits the bill between payments. | Seen (menu) |

## 2. Payment methods

| Feature | What it does | Status |
|---|---|---|
| Tap to Pay | Takes a contactless card or phone on the device's own NFC chip. | Not available on this device (see section 13) |
| Card Reader | Sends the amount to the Solo card machine. | Seen |
| Payment Links | Creates a link or QR code the customer pays online. | Seen |

Cash is not a payment method on this screen. Cash is counted into the
till tray (see `TILL_PROCEDURES.md`, section 8.4).

## 3. Open orders (bell icon)

| Feature | What it does | Status |
|---|---|---|
| Open order list | Every parked order, with its code, time and items. | Seen |
| Search | Finds an open order by code, item or amount. | Seen |
| New order | Starts a new order. | Seen |
| Use courses banner | Explains courses; links to POS Plus. | Plus |

## 4. Sales (receipt icon)

| Feature | What it does | Status |
|---|---|---|
| Today's sales total | Total for the day, with a link to detail. | Seen |
| Sales list by date | Each sale with items, time and result. | Seen |
| Search and filter | Finds a sale; filters by date or result. | Seen (search) |
| Sale detail | Shows the items, the VAT and the payment. | Seen |
| Receipt button | Reprints the customer receipt. | Seen |
| Payment line | The card reference, time and result of the payment. | Seen |

A sale that did not complete shows "Unsuccessful" in red.

## 5. Reporting (chart icon)

| Feature | What it does | Status |
|---|---|---|
| Periods | Today, Yesterday, This week, This month, Custom. | Seen |
| Sales total and count | The total and the number of sales. | Seen |
| Items sold | Number of items sold in the period. | Seen |
| Average sale | Total divided by number of sales. | Seen |
| Refunds total | Money refunded in the period. | Seen |
| Discounts total | Money taken off by discounts. | Seen |
| Best-selling items | The items sold most. | Seen |
| Busiest period | Sales by hour, and the busiest time. | Seen |
| Payment methods | How customers paid. | Seen |
| Insights, Revenue, Payouts, Fee invoice, Payments | Detailed tabs. | Seen (names) |
| Go there now | Opens the full reports on the website. | Web |

The first day's figures are zero until a successful sale is made.

## 6. Items (price-tag icon)

| Feature | What it does | Status |
|---|---|---|
| Library | The full list of items with their prices. Search, sort and filter. | Seen |
| Add item | Creates a new item. | Seen (button) |
| Categories | The till categories and how many items each holds. | Seen |
| Inventory | Stock tracking. Filter by low stock, sold out, tracked. | Seen |
| Modifiers | Modifier sets and their choices, such as milk or bread. | Seen |
| Option sets | Variations such as size or colour. | Seen |
| Deposits | Container deposits, for example bottles. | Plus |
| Discounts | Named discounts. The shop has 10%, 20% and 50%. | Plus |
| Create modifier set / option set / discount | Creates a new group. | Seen (button) |

**Clean-up needed:** the modifier list still holds "(Example) Toppings",
and the option sets still hold the sample "Color" and "Size" sets. The
checklist already asks for the toppings set to be deleted.

## 7. Tools (grid icon)

The Tools screen is a menu. Each entry opens its own feature.

| Feature | What it does | Status |
|---|---|---|
| Items | Opens section 6. | Seen |
| Employees | Staff accounts and their roles. | Seen (section 8) |
| Customers | Customer list for invoices and loyalty. | Seen (section 9) |
| Reporting | Opens section 5. | Seen |
| Online Store | Builds a free online shop (Webspace). | Offer only |
| Bookings | Appointment booking. | Offer only |
| Loyalty | Reward programmes. | Not confirmed (did not finish loading) |
| Gift Cards | Sells and redeems gift cards. | Not confirmed |
| Card readers | Pairs and buys card machines. | Not confirmed (see section 13) |
| Tap to Pay | Settings for contactless on the device. | Seen (section 13) |
| Payment links | Creates customer payment links. | Seen (section 2) |
| Cash Advance | Loans repaid from sales. | Offer only (eligibility rules shown) |
| Invoices | Creates and sends invoices. | Not confirmed |
| Expenses | Tracks spending and exports for tax. | Offer only |

Cash Advance eligibility, as shown on the device: complete identity
checks, take card payments for at least three months, and use the SumUp
Business Account and card. Meeting these does not guarantee an offer.

## 8. Employees

| Feature | What it does | Status |
|---|---|---|
| Members | Lists everyone who can log in, with role and status. | Seen |
| Search, Role and Status filters | Finds a member. | Seen |
| Add team member | Invites a person by e-mail. | Seen (button) |
| Roles | The permission sets a member can have. | Seen (tab) |
| Edit team member | Changes a member's role. | Seen (panel) |

On 19 November 2026 the only member is the account owner, as
Administrator. The six staff e-mail addresses are still needed (see the
checklist). Each staff member needs their own address to be invited.

## 9. Customers

| Feature | What it does | Status |
|---|---|---|
| Customer list | Names and contact details of customers. | Seen (empty) |
| Add customer | Adds a customer by hand. | Seen (button) |
| Invoice customers note | Invoice customers are kept in the Invoices directory. | Seen |

The list is empty. Customers are added by hand, or created from invoices.

## 10. Profile (person icon, bottom left)

| Feature | What it does | Status |
|---|---|---|
| Account name and merchant code | Shows MW82CKEA. | Seen |
| 24/7 priority support | Opens support. | Seen |
| Inbox | Messages from SumUp, with an unread count. | Seen |
| Login and security | Password, two-factor authentication. | Seen (name) |
| Payouts | Money sent to the bank account. | Seen |
| Payout settings | Which bank account receives payouts. | Seen (name) |
| Tap to Pay | See section 13. | Seen |
| Card Reader | Card machine settings. | Seen (name) |

## 11. Settings and business profile (web)

These are on the website, not the till.

| Feature | What it does | Status |
|---|---|---|
| Business information | Registered name, trade name, address. | Web |
| Business profile | Name on SumUp listings, statement descriptor, phone. | Web |
| VAT | VAT rates charged. | Web |
| Plans and fees | Current plan and fees. | Web |
| Employees | Staff profiles (also on the till). | Web |

The registered name still reads "Greens Kitchen". Only SumUp Support can
change it (checklist, section 8.5).

## 12. Printing and kitchen (checklist)

The printing and order-sending settings are per device, and are not in
the till's menu. They are covered by checklist Rules U3 and U4:

1. The "Till" printer prints POS Lite receipts.
2. The Solo's counter printer prints standalone card receipts.
3. The Terminal prints order tickets only where "Print order tickets" is
   on.

## 13. Known limits on this device

1. **Tap to Pay: not available.** The device reports "NFC not available",
   so contactless payment on this Chromebook will not work. Use the Solo.
2. **Card readers** and **Loyalty** did not finish loading during this
   check, so they are not confirmed.
3. **Refunds** and **split bills** have not been used on a real sale.

## 14. Not yet checked

1. Gift Cards and Invoices (did not load in this check).
2. Loyalty (did not load).
3. Items: creating and editing an item; deleting a category.
4. Courses, the Z-report and the kitchen send button.

These need a manager's test sale or a run-through before the document can
be called complete.

## Source

This reference was compiled from the POS app on the shop's Android device
on 19 November 2026. Where a screen did not load or was not opened, the
status column says so rather than guessing.
