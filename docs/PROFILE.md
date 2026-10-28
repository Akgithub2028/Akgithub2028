# Profile maintenance

The homepage features only SFP, Real-Time Voice Translator, Qwen QLoRA,
NexusAgent, Autonomous AI Co-Scientist, and the Wunder Fund forecasting competition.
Project claims come from the supplied resume and each linked repository; the
cards describe recorded experiments, not independently reproduced results.

Edit `scripts/build_visuals.py` to update the cards or theme. With Pillow and the
DejaVu system fonts installed, run `python3 scripts/build_visuals.py`. Commit the
script and generated `assets/` files together. The desktop and mobile layouts
are separate; README pictures choose the appropriate one. Reduced-motion
preferences select static PNG header art. Animation is a six-second GIF loop;
all essential text remains still. No scripts, external fonts, or SVG foreign
objects execute on the GitHub profile.

`scripts/update_signal.py` reads the actual GitHub contribution calendar and
atomically writes `profile/signal.svg`. The workflow runs daily with the built-in
`GITHUB_TOKEN`; no personal access token or paid renderer is needed. API failure
leaves the previous image intact. The date is UTC. Contribution counts follow
GitHub's account visibility rules and are not a count of commits alone.

The original Komarev URL and `Akgithub2028` username are preserved so the same
profile-view counter continues. It counts image requests under Komarev/GitHub
caching behavior, not distinct people. Do not change the username to reset the
identity. Local preview tooling should replace that remote image with a
placeholder to avoid adding preview requests to the counter.

The old Pac-Man workflow and unused stats cards were replaced by the custom
contribution card. The historical `output` branch is retained.
