import argparse
import inspect
import sys

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
        if value is not None:
            if name.startswith("p_"):
                args.append(value)
            elif name.startswith("k_"):
                kwargs[name[2:]] = value
            elif name.startswith("v_"):
                args.extend(value)
    try:
        func = argparse_namespace.func
    except AttributeError:
        parser.error("Must specify a command")
    print("Calling {} with args {} and kwargs {}".format(func, args, kwargs),
          file=sys.stderr)
    return func(*args, **kwargs)

def command(func):
    parameters = inspect.signature(func).parameters.values()
    def setup_subparser(saot):
        subparser = saot.add_parser(func.__name__, help=func.__doc__)
        subparser.set_defaults(func=func)
        for parameter in parameters:
            args = []
            kwargs = {
                "metavar": _py_name_to_cmd(parameter.name).upper(),
                "type": (parameter.annotation
                         if parameter.annotation is not inspect.Parameter.empty
                         else None),
            }
            if parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                args.append("p_%s" % parameter.name)
                if _has_default(parameter):
                    kwargs["nargs"] = "?"
            elif parameter.kind == inspect.Parameter.KEYWORD_ONLY:
                args.append("--" + _py_name_to_cmd(parameter.name))
                kwargs["dest"] = "k_%s" % parameter.name
            elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                args.append("v_%s" % parameter.name)
                kwargs["metavar"] = (kwargs["metavar"][:-1]
                                     if kwargs["metavar"].endswith("S")
                                     else kwargs["metavar"])
                kwargs["nargs"] = "+"
            subparser.add_argument(*args, **kwargs)
    _subparser_setup_functions.append(setup_subparser)
    return func

def _has_default(parameter):
    return parameter.default is not inspect.Parameter.empty

def _py_name_to_cmd(py_name):
    return py_name.replace("_", "-")
