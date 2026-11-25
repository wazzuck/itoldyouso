<!--
FILE: migena/NETWORK_SETUP.md

Purpose:
    Neville's job-file note for the Migena register: how to move the
    power brick and the network adapter under the counter so the
    SumUp POS Lite on the counter top reaches the internet by cable
    instead of by Wi-Fi, with only two slim cables through the
    grommet.

Deliberately NOT for:
    Being the task itself. The task lives as "Neville task 7 of 7" on
    migena/documentation.html, built by scripts/split_portal.py. This
    note holds the reasoning, the parts to order and the test plan
    that the task card summarises.

Invariants relied upon:
    1. The register is a first-generation SumUp POS Lite running
       Android 10, confirmed by the operator on 25 November 2026.
       Do not use the Android 15 specification of the POS Lite 2.0
       (model POS-REG-027) for this unit.
    2. SumUp publishes no supported-adapter list for the POS Lite,
       so every claim below about a working adapter is a probability,
       not a guarantee. The bench test in section 8 decides.
    3. Wi-Fi stays configured as the fallback throughout.

Prepared by Neville Bryce, IToldYouSo Computing.
Date: 25 November 2026. Status: to do.
-->

# Under-counter power and wired network for the register

## 1. What this document is for

The SumUp POS Lite on the front counter currently reaches the
internet over Wi-Fi, and its 65 watt power brick sits on or behind
the counter. The aim of this job is:

1. to run the register's network by cable, so payments no longer
   depend on the Wi-Fi signal at the counter; and
2. to hide the power brick and the network adapter under the
   counter, so only two slim cables pass through the grommet.

This note records the parts to order, the two ways of wiring it, the
one that is recommended, and the test that proves it works before
anything is drilled. The task card on the documentation page
summarises the same work in seven steps.

## 2. What the register actually is

These are the facts the design rests on. Each one was checked on
25 November 2026.

1. **It is a first-generation POS Lite on Android 10.** The
   current POS Lite 2.0 (model POS-REG-027) ships with Android 15
   and a different specification, so its specification sheet does
   not describe this unit.
2. **It has no built-in Ethernet (Local Area Network, LAN) port.**
   Retailer specifications for the POS Lite list Wi-Fi 5
   (802.11ac), Bluetooth, two Universal Serial Bus (USB) 2.0 ports
   and a USB-C port used for power and for the card reader cradle.
   SumUp publishes no port list for the first-generation unit, so
   confirm the ports on the unit itself before ordering.
3. **The USB-C port carries data as well as power.** The Solo card
   reader cradle is driven from it, which is why a cable from this
   port can carry a network connection as well as charging current.
4. **SumUp documents no Ethernet adapter as supported for the
   POS Lite.** Its own kiosk setup guide does say, of a wired
   printer connection, "you will need an adaptor to connect an
   Ethernet cable to your POS", so an adapter is the intended route
   to wired networking on its devices. The SumUp Register gets its
   Ethernet from the hub bundled with that product; the POS Lite is
   sold without one.

## 3. Why the adapter is uncertain on this unit

An Ethernet adapter that is certain to work on a laptop can be dead
on this register, for three reasons.

1. **Android 10 predates Google's Generic Kernel Image (GKI)
   rules,** which arrived with Android 11. The chipsets this
   register supports are whatever SumUp compiled into that kernel,
   and SumUp publishes neither the kernel configuration nor an
   adapter list.
2. **Android only adopts interfaces named `eth0`, `eth1` and so
   on.** An adapter driven by a chipset driver (ASIX or Realtek)
   creates `ethX` and is adopted. An adapter that relies only on the
   generic Communications Device Class (CDC) standards — Ethernet
   Control Model (ECM), Ethernet Emulation Model (EEM), Network
   Control Model (NCM) — creates an interface called `usb0`, which
   the kernel sees but Android ignores. The adapter then looks
   broken: the Ethernet settings stay greyed out and nothing
   connects, even though the hardware is working.
3. **Some Android 10 devices only bring the interface up at boot.**
   An adapter plugged in after boot may need a full power-cycle
   before it is used at all.

The practical consequence is a chipset shopping rule:

| Chipset family | Odds on this register |
| --- | --- |
| ASIX AX88772 and relatives | Best on Android; creates `ethX` |
| Realtek RTL8152 / RTL8153 | Often works; may end up as `usb0` |
| Standards-only, unnamed | Worst: this is the `usb0` trap |

The Realtek row deserves its detail: if the kernel omits the `r8152`
driver, that adapter falls back to ECM, becomes `usb0`, and is
ignored, exactly as the unnamed row describes.

## 4. The two ways to do it

### Option A — two slim cables (recommended)

Power and network use different ports, so they are extended
separately and the bulk stays under the counter.

1. **Power:** a 3 metre USB-C cable rated 100 watts (5 amps,
   e-marked) runs from the register down to the original SumUp
   65 watt adapter, which lives under the counter. This long, proper
   cable *is* the extension: a compliant passive USB-C extension
   lead effectively does not exist as a product.
2. **Network:** the adapter hangs off a USB 2.0 port through a
   3 metre USB Type-A extension lead, with its RJ45 lead running to
   the router or switch.

Why this is the better of the two:

- no hub, so no extra chipset to fail the Android 10 test;
- no Power Delivery (PD) pass-through to go wrong, so the register
  keeps the original SumUp adapter that its own troubleshooting
  guide insists on;
- if the adapter fails, the Wi-Fi fallback is untouched and the
  till keeps trading.

USB 2.0 tops out at 480 megabits per second, so a 100 megabit
adapter is all the bandwidth a till needs; a gigabit adapter buys
nothing here and draws more current.

### Option B — one cable and a hub under the counter

A single full-featured USB-C cable runs down to a hub with PD
pass-through under the counter; the hub takes the 65 watt adapter
in one socket and an RJ45 lead in another. This gives one neat
cable at the counter top, at the cost of three risks:

1. **PD pass-through quality.** The hub must accept 65 watts in and
   forward it while still enumerating data. Some negotiate only 45
   or 60 watts, or drop the link under load.
2. **A second chipset gamble.** The hub's own Ethernet chipset must
   pass the same Android 10 test as any other adapter.
3. **One cable carries everything.** A single fault takes power and
   network down together, where Option A lets the network fail alone.

Use Option B only if Option A's two cables cannot be routed
tidily, and bench-test it in full before fitting it.

### Approaches that are ruled out

1. **Passive USB-C extension leads.** Most sold as extensions are
   charging-only, with no data wires, or unreliable at data.
2. **Daisy-chaining hubs**, or powering a hub from a USB 2.0 port:
   a USB 2.0 port supplies 500 milliamps, which will not carry a hub
   and an adapter at the same time.
3. **The adapter in the USB-C port with no power path**, which
   leaves the register running on its battery and charging
   unpredictably.

## 5. Parts to order

### 5.1 Buying specification

1. **Ethernet adapter:** USB Type-A plug, 10/100 megabit, and the
   listing must **name an ASIX chipset** (AX88772 family is the
   best documented on Android). An unbranded "driverless USB network
   adapter" that names no chipset is the listing to avoid.
2. **USB-C cable:** 3 metres, rated 100 W / 5 A with an e-marked
   plug, and the listing must say it carries **data as well as
   charging**. 480 megabits per second of data is plenty.
3. **USB Type-A extension lead:** 3 metres, USB 2.0, passive. The
   total of the original cable plus the extension must stay under
   5 metres.
4. **RJ45 patch lead:** 2 metres, Category 5e or Category 6. Already
   covered by `INSTALLATION_CHECKLIST.md`, section 2.2.
5. **Fixings:** hook-and-loop ties and self-adhesive cable-tie
   mounts, already covered by section 2.3 of the same checklist.

### 5.2 Shortlist

Prices below were seen in search results on 25 November 2026 and
must be checked on the listing before ordering. Plain product
links, no affiliate tag.

**Ethernet adapters, best fit first**

1. **Plugable USB2-E100**, ASIX AX88772A, 10/100. The manufacturer
   states support for "some Android devices", and the driver sits
   in the Linux kernel from 2.6.35 onwards, which is the strongest
   pedigree of these three.
   <https://www.amazon.co.uk/Plugable-Ethernet-Network-Compatible-Chromebook/dp/B00484IEJS>
2. **i-tec USB-A Fast Ethernet Adapter Advance (U2LAN)**, ASIX
   AX88772C, 10/100, £8.80 excluding Value Added Tax (VAT) on the
   manufacturer's own site.
   <https://i-tec.pro/en/produkt/u2lan-2/>
3. **usangreen USB to RJ45**, ASIX AX88772B, 10/100, £15 seen.
   <https://www.amazon.co.uk/Ethernet-Adapter-100Mbps-AX88772B-Converter-USB-male-RJ45/dp/B085X8BJMY>
4. **Fallback chipset:** any Realtek RTL8152 or RTL8153 adapter if
   all three above fail. It often works, but the `usb0` trap in
   section 3 makes it a second choice rather than a first.

**USB-C cable, 3 metres, 100 W with data**

1. **StarTech USB2C5C3M**, USB-IF certified, 3 metres, 100 W, £23.78
   seen. The safest of the three.
   <https://www.amazon.co.uk/StarTech-USB2C5C3M-Fast-Charge-Cable/dp/B07DPKX1N5>
2. **Aioneus 100 W 5 A**, 3 metres, 480 megabits per second, two-pack
   at £9.34 seen.
   <https://www.amazon.co.uk/Charging-Charger-Charge-MacBook-Samsung/dp/B0D1FX9DJS>
3. **UGREEN right-angle 100 W**, 3 metres, £9.89 seen. The
   right-angle plug suits a port that faces out of a slim chassis,
   but check it does not foul the counter.
   <https://www.amazon.co.uk/UGREEN-Charger-Transfer-Compatible-MacBook-Metallic-Grey/dp/B08HS6R164>

**USB Type-A extension lead, 3 metres**

1. **Lindy Anthra Line 36714**, double shielded, 10 year warranty,
   £7.02 seen.
   <https://www.amazon.co.uk/LINDY-36714-Extension-Cable-Anthra/dp/B07FWDMRS9>
2. **C2G 52108**, black, 3 metres, £6.88 seen. The listing states
   the 5 metre total limit that matters here.
   <https://www.amazon.co.uk/C2G-Cables-52108-Female-Extension-Black/dp/B001KUSZ1A>
3. **kenable PRO metal**, 24 gauge core, 3 metres, £5.49 seen.
   <https://www.amazon.co.uk/kenable-PUE/dp/B09WBRYZYT>

## 6. Wiring layout

```text
 COUNTER TOP                      UNDER THE COUNTER
+-------------------+  USB-C 3 m  +-----------------------+
|                   |============>| 65 W SumUp adapter    |--> mains
|                   |   (power)   +-----------------------+
| SumUp POS Lite    |
| register          |  USB-A 3 m  +-----------------------+
+-------------------+ ==> ext ==> |  ASIX adapter         |== RJ45 ==> router
                                  +-----------------------+
```

Two cables cross the grommet: one USB-C for power, one USB Type-A
for the network. Everything with a plug on it sits below.

## 7. Fitting it under the counter

1. Route both cables through the grommet with a service loop, so
   the register can still be lifted clear of the counter for
   cleaning without unplugging anything.
2. Fix the cables to the underside of the counter with
   self-adhesive cable-tie mounts and hook-and-loop ties. Hook-and-loop
   rather than nylon ties on the data lead, so it is never crushed.
3. Site the power brick where it can breathe, away from the till
   drawer's travel and away from any water route. Never daisy-chain
   a mains extension to reach it.
4. Keep the data lead clear of mains leads where they must cross;
   where they run together, use the spiral wrap from the checklist.
5. Label both ends of both cables, as the checklist requires of
   every cable on this job.

## 8. Test plan — bench first, then on site

Nothing is drilled until steps 1 to 4 pass.

1. **Assemble the whole chain on the bench:** extension lead into
   the register's USB Type-A port, adapter into the extension, USB-C
   cable from the original SumUp 65 watt adapter into the register,
   RJ45 from the adapter into the router.
2. **Boot with everything already attached,** and check the
   adapter's link light is lit.
3. **Turn the Wi-Fi off on the register.** The register must still
   reach the internet: open the SumUp dashboard and let it load.
   This is the real test, because Android 10 shows no Ethernet icon
   you can rely on.
4. **Power the register off and on again with everything still
   attached,** turn Wi-Fi off once more, and repeat the test. This
   catches the devices that only bring the interface up at boot.
5. **If it fails:** try a second adapter with a different chipset,
   ASIX first and Realtek second, and check the router's client list
   for a new device before concluding the register cannot do it. A
   device listed there but unreachable from the register is the
   `usb0` trap from section 3.
6. **Record the result:** which adapter worked, on what date, and
   whether it survived a power-cycle. Put it in the job file and in
   `STATUS.md`.

## 9. Acceptance and fallback

The job is finished when:

1. the register reaches the internet with Wi-Fi switched off, both
   immediately after boot and after a power-cycle;
2. the brick and the adapter are under the counter, the two cables
   are tied and labelled, and the drawer still travels freely;
3. **Wi-Fi is switched back on and left configured as the
   fallback**, because SumUp supports Wi-Fi only and a support call
   may otherwise have no answer to give;
4. one live sale has been taken in a busy period over the wired
   connection, with the date recorded.

## 10. Risks and open questions

1. **Port occupancy.** The receipt printer or the card reader
   cradle may already hold the USB Type-A port on the day. If so,
   decide between Option B and a small hub on site, and test before
   fitting.
2. **No SumUp guarantee.** SumUp documents no adapter for this
   register, so a wired path that misbehaves is not a warranty
   matter. Wi-Fi remains the supported configuration.
3. **Age of the platform.** Android 10 is the register's operating
   system and is no longer receiving security updates. That is a
   separate question from this job, but it belongs in the same
   conversation at the next hardware review.

## 11. Sources, checked 25 November 2026

1. SumUp Support: "What's the POS Lite?", "Set up the POS Lite" and
   "Troubleshoot my POS Lite" — power, ports and Wi-Fi setup.
   <https://help.sumup.com/en-GB/articles/25FQdXxaLBSF9OgJuwZOba-pos-lite-overview>
2. SumUp setup guide, Kiosk section — "you will need an adaptor to
   connect an Ethernet cable to your POS".
   <https://setup.sumup.com/kiosk>
3. SumUp POS Lite product page and retailer specifications
   (POS-REG-027) — no Ethernet port, Wi-Fi 5, two USB 2.0 ports,
   Android 15 on the current model.
   <https://www.sumup.com/en-us/pos/pos-lite/>
4. "Why Android can't use CDC Ethernet", 31 May 2023 — the
   `ethX` naming rule behind the `usb0` trap.
   <https://jordemort.dev/blog/why-android-cant-use-cdc-ethernet/>
5. Linux kernel `drivers/net/usb` documentation — which chipsets
   each driver covers and which interface name it creates.
6. Plugable support and product pages — Android compatibility for
   the ASIX AX88772A is device dependent and cannot be guaranteed
   by the manufacturer either.
   <https://plugable.com/products/usb2-e100>
