# Profile maintenance

The profile uses native GitHub Markdown for headings, project descriptions,
technology labels, links, and the technical-focus table. Content inherits
GitHub's typography and light/dark theme, wraps on mobile, and remains selectable.
There are no generated hero banners, project cards, or animated text assets.

Featured work is limited to SFP, Real-Time Voice Translator, Qwen QLoRA,
NexusAgent, Autonomous AI Co-Scientist, and the Wunder Fund forecasting competition.
Project claims come from the supplied resume and linked repositories; reported
results have not been independently reproduced in this profile repository.
GPU programming and LLM serving are explicitly presented as current study.

Pac-Man remains near the top. Its daily workflow publishes dark and light SVG
animations to the `output` branch using pinned action revisions. A reduced-motion
preference selects the static contribution calendar instead.

`scripts/update_signal.py` reads GitHub's contribution calendar and atomically
writes the desktop and mobile `profile/signal*.svg` files. The daily workflow
uses the built-in `GITHUB_TOKEN`; no personal access token or paid renderer is
needed. A failed API request leaves the last generated image intact. Dates are
UTC. Contributions follow GitHub's visibility rules and include more than commits.

The Komarev counter retains the original `Akgithub2028` username, preserving its
counter identity. Only its appearance has changed to a compact, muted badge.
The service counts image requests under Komarev/GitHub caching behaviour, not
distinct people. Preview tools should substitute a placeholder for this image
to avoid adding preview requests to the counter.
