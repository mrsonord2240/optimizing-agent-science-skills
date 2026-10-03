"""Re-audit 6: minimal reproduction of fig.set_layout_engine('constrained') after a colorbar was added (failure-modes.md says it is a valid fix).
Usage: py.sh r6_engine_minimal.py"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

print("matplotlib", matplotlib.__version__)
for label, build in (
    ("single axes + colorbar, engine set after", lambda: _after(1)),
    ("1x2 axes, colorbar on one, engine set after", lambda: _after(2)),
    ("1x2 axes, no colorbar, engine set after", lambda: _nocb()),
    ("1x2 axes, colorbar, engine set BEFORE the colorbar", lambda: _before()),
):
    pass


def _after(n):
    f, axs = plt.subplots(1, n)
    ax = np.atleast_1d(axs)[-1]
    f.colorbar(ax.imshow(np.zeros((3, 3))), ax=ax)
    f.set_layout_engine('constrained')
    f.canvas.draw()
    return f


def _nocb():
    f, axs = plt.subplots(1, 2)
    axs[0].plot([1, 2])
    f.set_layout_engine('constrained')
    f.canvas.draw()
    return f


def _before():
    f, axs = plt.subplots(1, 2)
    f.set_layout_engine('constrained')
    f.colorbar(axs[1].imshow(np.zeros((3, 3))), ax=axs[1])
    f.canvas.draw()
    return f


for label, fn in (("single axes + colorbar, engine set after", lambda: _after(1)),
                  ("1x2 axes, colorbar on one, engine set after", lambda: _after(2)),
                  ("1x2 axes, no colorbar, engine set after", _nocb),
                  ("1x2 axes, engine set BEFORE adding the colorbar", _before)):
    try:
        fn()
        print(f"OK        {label}")
    except Exception as e:
        print(f"EXCEPTION {label}: {type(e).__name__}: {e}")
    plt.close('all')
