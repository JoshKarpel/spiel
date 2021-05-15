from typing import TYPE_CHECKING, Callable, MutableMapping

if TYPE_CHECKING:
    from .state import State

from nbterm import Notebook

NotebookExecutor = Callable[["State"], None]

NOTEBOOKS: MutableMapping[str, NotebookExecutor] = {}


def notebook(name: str) -> Callable[[NotebookExecutor], NotebookExecutor]:
    def registrar(executor: NotebookExecutor) -> NotebookExecutor:
        NOTEBOOKS[name] = executor
        return executor

    return registrar


@notebook("nbterm")
def nbterm(state: "State") -> None:
    save_path = state.tmp_dir / f"{id(state.current_slide)}.ipynb"

    nb = Notebook(state.current_slide.notebook or save_path)

    state.current_slide.notebook = save_path

    nb.show()
    nb.save(save_path)
