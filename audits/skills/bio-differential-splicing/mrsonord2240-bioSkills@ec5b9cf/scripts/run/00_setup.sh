#!/bin/bash
# Copy the fixed Skill (commit ec5b9cf) out of the worktree into run/skill (read-only source; nothing written in the worktree).
# git archive reads the object store, so the bytes are exactly the commit's.
set -e
R=/f/OpenScience/audits/bio-differential-splicing/run
rm -rf $R/skill $R/_arch; mkdir -p $R/_arch
git -C /f/OpenScience/wt/as-diffsplice rev-parse HEAD
git -C /f/OpenScience/wt/as-diffsplice archive ec5b9cf46e2b1c73a361724dab97168c464fcbac alternative-splicing/differential-splicing | tar -x -C $R/_arch
mv $R/_arch/alternative-splicing/differential-splicing $R/skill
rm -rf $R/_arch
find $R/skill -type f | sort; sha256sum $R/skill/SKILL.md
# byte-identity check vs the worktree file
cmp $R/skill/SKILL.md /f/OpenScience/wt/as-diffsplice/alternative-splicing/differential-splicing/SKILL.md && echo "SKILL.md identical to worktree"
find /f/OpenScience/wt/as-diffsplice -name __pycache__ | head
