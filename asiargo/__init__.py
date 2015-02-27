import argparse
import inspect

_subparser_setup_functions = []

def allez_cuisine(description=None):
    parser = argparse.ArgumentParser(description=description)
    subparser_action_object_thing = parser.add_subparsers()
    for setup_subparser in _subparser_setup_functions:
        setup_subparser(subparser_action_object_thing)
    argparse_namespace = parser.parse_args()

    args = []
    kwargs = {}
    for name, value in vars(argparse_namespace).items():
        if name.startswith("p_"):
            args.append(value)
        elif name.startswith("k_"):
            kwargs[name[2:]] = value
    try:
        func = argparse_namespace.func
    except AttributeError:
        parser.error("Must specify a command")
    return argparse_namespace.func(*args, **kwargs)

def command(func):
    parameters = inspect.signature(func).parameters.values()
    def setup_subparser(saot):
        subparser = saot.add_parser(func.__name__, help=func.__doc__)
        subparser.set_defaults(func=func)
        for parameter in parameters:
            args = []
            kwargs = {
                "default": (parameter.default
                            if parameter.default is not inspect.Parameter.empty
                            else None),
                "metavar": _py_name_to_cmd(parameter.name).upper(),
                "type": (parameter.annotation
                         if parameter.annotation is not inspect.Parameter.empty
                         else None),
            }
            if parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if kwargs["default"]:
                    kwargs["nargs"] = "?"
                args.append("p_%s" % parameter.name)
            elif parameter.kind == inspect.Parameter.KEYWORD_ONLY:
                args.append("--" + _py_name_to_cmd(parameter.name))
                kwargs["dest"] = "k_%s" % parameter.name
            subparser.add_argument(*args, **kwargs)
    _subparser_setup_functions.append(setup_subparser)
    return func

def _py_name_to_cmd(py_name):
    return py_name.replace("_", "-")

def _cmd_name_to_py(cmd_name):
    return cmd_name.replace("-", "_")
