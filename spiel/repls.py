import code
from collections.abc import Callable, MutableMapping

import IPython
from traitlets.config import Config

REPLExecutor = Callable[[], None]

REPLS: MutableMapping[str, REPLExecutor] = {}


def repl(name: str) -> Callable[[REPLExecutor], REPLExecutor]:
    def register(executor: REPLExecutor) -> REPLExecutor:
        REPLS[name] = executor
        return executor

    return register


@repl("builtin")
def builtin() -> None:
    code.InteractiveConsole().interact()


@repl("ipython")
def ipython() -> None:
    c = Config()
    c.InteractiveShellEmbed.colors = "Neutral"

    IPython.embed(config=c)
