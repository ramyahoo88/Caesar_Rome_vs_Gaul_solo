# Cloudflare publication

The Caesar helper is served at `https://solo-table.pages.dev/games/caesar-rome-vs-gaul/`.
Its single PDF download is the existing merged `print/Caesar_Solo_Print_and_Play.pdf`, containing the rules, references, Directive cards and record sheet. There are no GitHub links in the helper or its catalog entry. The catalog retains its attribution text without GitHub hyperlinks.

Run `python3 cloudflare/build.py` from the repository root. This creates an advanced-mode Pages `_worker.js` in ignored `cloudflare/dist/`. The Worker embeds the exact HTML and PDF bytes, adds the Caesar catalog entry, and forwards other paths to the immutable preceding deployment in `deployment.json`. This preserves all other games and their files without reconstructing their source trees from an outdated catalog checkout.

Publish to the existing `solo-table` Pages project, production branch `main`, using the Pages Direct Upload API with an empty asset manifest (`{}`) and the generated `_worker.js`. Use the current source commit as deployment provenance. A preview branch can be used first. No secrets or upload credentials belong in this repository.

Keep the pinned preceding deployment available: it supplies all other game paths. Before publishing, check that production still points to the reviewed preceding deployment, or reconcile concurrent changes. For a future full-site release, collect the complete current site sources before replacing this forwarding arrangement.

The existing deck JavaScript, card definitions, rules and PDF contents are not changed by publication. Only the helper's bottom download section is added.
