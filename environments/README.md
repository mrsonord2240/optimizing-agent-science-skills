# environments/

How each audit runtime was built, so an audit can be reproduced: interpreters, packages and
command-line tools with their versions, where they came from, and which Skills need them.

One file per env, e.g. `mass-spec-proteomics-analyst.md`.

No binaries, no virtual environments, no package libraries — those live outside the repository and are
rebuilt from these notes.

Each file records:

- **Interpreters:** Python and R versions and where they came from.
- **Packages:** name, version, and whether it went into the shared environment or its own, and why.
- **Command-line tools:** version, download URL, how it was unpacked, and the smoke test that proved
  it runs.
- **Gated tools:** anything behind a registration form, login or payment, with its URL and the free
  substitute used instead.
- **Blocked:** what could not be installed here and what that leaves unverifiable.

A licence that had to be accepted by a person (academic or non-commercial terms) is named here with
who accepted it.
