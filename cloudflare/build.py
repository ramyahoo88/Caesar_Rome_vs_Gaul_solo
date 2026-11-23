"""Build the Caesar addition to the existing Solo Table Pages deployment.

The generated advanced-mode Worker embeds the authored helper and the exact
shipped print packet. Other site paths use the pinned preceding deployment.
No third-party packages, remote build inputs or print regeneration required.
"""
import base64
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
config = json.loads((HERE / "deployment.json").read_text())
helper = (ROOT / "print/Caesar_Solo_Deck.html").read_text()
packet = (ROOT / "print/Caesar_Solo_Print_and_Play.pdf").read_bytes()
worker = (HERE / "worker.template.mjs").read_text()
for marker, value in {
    "__CONFIG_JSON__": json.dumps(config),
    "__HELPER_JSON__": json.dumps(helper, ensure_ascii=False),
    "__PACKET_BASE64_JSON__": json.dumps(base64.b64encode(packet).decode()),
    "__PACKET_SHA256_JSON__": json.dumps(hashlib.sha256(packet).hexdigest()),
}.items():
    assert worker.count(marker) == 1, marker
    worker = worker.replace(marker, value)
out = HERE / "dist"
out.mkdir(exist_ok=True)
(out / "_worker.js").write_text(worker)
(out / "manifest.json").write_text("{}\n")
manifest = {
    "helper_sha256": hashlib.sha256(helper.encode()).hexdigest(),
    "packet_sha256": hashlib.sha256(packet).hexdigest(),
    "packet_bytes": len(packet),
    "worker_sha256": hashlib.sha256(worker.encode()).hexdigest(),
    "worker_bytes": len(worker.encode()),
    "config": config,
}
(out / "build.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(manifest, indent=2))
