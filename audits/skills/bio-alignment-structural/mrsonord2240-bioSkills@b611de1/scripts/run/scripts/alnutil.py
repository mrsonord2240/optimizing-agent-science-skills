"""Independent helpers used by the audit (NOT part of the Skill): read CA atoms, Kabsch RMSD, TM-score from a
given residue pairing and a given rotation, TMalign alignment-string parser. Pure numpy, so it is a second
method for every number the Skill's tools print.
Run inside WSL (env alignment python): imported by the other scripts."""
import subprocess
import numpy as np

AA3 = {'ALA','ARG','ASN','ASP','CYS','GLN','GLU','GLY','HIS','ILE','LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL'}


MODIFIED = {'MSE', 'SEP', 'TPO', 'PTR', 'CSO', 'MLY', 'HYP'}


def read_ca(path, chain=None, model_first=True, include_modified=False):
    """Standard-residue CA atoms of the first model; ordered list of (chain, resseq, icode, resname, xyz).
    First altloc only. Independent of Biopython on purpose (fixed-column PDB parse)."""
    out, seen = [], set()
    for line in open(path):
        if line.startswith('ENDMDL') and model_first and out:
            break
        if not (line.startswith('ATOM') or (include_modified and line.startswith('HETATM') and line[17:20] in MODIFIED)):
            continue
        if line[12:16].strip() != 'CA':
            continue
        if line[16] not in ' A':
            continue
        ch, num, ic, rn = line[21], int(line[22:26]), line[26], line[17:20]
        if chain and ch != chain:
            continue
        key = (ch, num, ic)
        if key in seen:
            continue
        seen.add(key)
        out.append((ch, num, ic, rn, np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])))
    return out


def kabsch(P, Q):
    """Optimal rotation R and translation t so that (P @ R.T + t) ~ Q; returns rmsd, R, t."""
    Pc, Qc = P.mean(0), Q.mean(0)
    H = (P - Pc).T @ (Q - Qc)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = Qc - R @ Pc
    diff = (P @ R.T + t) - Q
    return float(np.sqrt((diff ** 2).sum() / len(P))), R, t


def d0_tm(L):
    return 1.24 * (L - 15) ** (1.0 / 3) - 1.8 if L > 21 else 0.5


def tm_score(P_moved, Q, Lnorm):
    d0 = d0_tm(Lnorm)
    d = np.linalg.norm(P_moved - Q, axis=1)
    return float((1.0 / (1.0 + (d / d0) ** 2)).sum() / Lnorm)


def parse_tmalign_alignment(stdout):
    """From full (non -outfmt 2) TMalign text: the three alignment lines (seq1, marks, seq2)."""
    lines = stdout.splitlines()
    for i, l in enumerate(lines):
        if l.startswith('(":" denotes'):
            return lines[i + 1].rstrip('\n'), lines[i + 2].rstrip('\n'), lines[i + 3].rstrip('\n')
    raise RuntimeError('no alignment block in TMalign output')


def pairs_from_alignment(s1, s2):
    """Index pairs (i, j) of residues aligned (both non-gap), 0-based into the residue lists."""
    i = j = 0
    pairs = []
    for a, b in zip(s1, s2):
        if a != '-' and b != '-':
            pairs.append((i, j))
        if a != '-':
            i += 1
        if b != '-':
            j += 1
    return pairs


def tmalign_independent(pdb1, pdb2, ch1=None, ch2=None):
    """Run TMalign full output, rebuild the residue pairing from its alignment strings, and compute RMSD and both
    TM-scores in numpy from that pairing (superposition by Kabsch on all aligned pairs)."""
    out = subprocess.run(['TMalign', pdb1, pdb2], capture_output=True, text=True).stdout
    s1, _, s2 = parse_tmalign_alignment(out)
    r1, r2 = read_ca(pdb1, ch1), read_ca(pdb2, ch2)
    pairs = pairs_from_alignment(s1, s2)
    P = np.array([r1[i][4] for i, _ in pairs])
    Q = np.array([r2[j][4] for _, j in pairs])
    rmsd, R, t = kabsch(P, Q)
    moved = P @ R.T + t
    return {'lali': len(pairs), 'rmsd': rmsd, 'tm_by_1': tm_score(moved, Q, len(r1)), 'tm_by_2': tm_score(moved, Q, len(r2)),
            'L1': len(r1), 'L2': len(r2)}
