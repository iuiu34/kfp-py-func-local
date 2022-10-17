"""Run pipeline local."""
import datetime as dt  # noqa
import inspect
import os  # noqa
import random  # noqa
import re
import types

import fire


# import kfp  # noqa


def run_kfp_pipeline_local(pipeline,
                           start_step=None,
                           func_steps_output: dict = None,
                           locals_: dict = None,
                           func_imports: list = None,
                           **kwargs  # noqa
                           ):
    """Run kfp pipeline in local (debugging)."""
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    # debug with "run with python console"
    if locals_ is not None:
        locals().update(**locals_)
    # func_steps_output = dict(
    #     get_data=f"os.path.join(output_path, website, 'get_data', 'train', 'data.csv')",
    #     train="os.path.join(output_path, website, 'train','pipeline.joblib')",
    #     evaluate="os.path.join(output_path, website, 'evaluate', 'metrics.json')",
    # )
    if not isinstance(pipeline, types.FunctionType):
        raise ValueError

    if func_steps_output is None:
        func_steps_output = {}
    func_steps = list(func_steps_output.keys())

    if start_step is not None:
        if start_step not in func_steps:
            raise ValueError(f"start step '{start_step}' not defined.")
        print(f"start_step: {start_step}")
        start_index = func_steps.index(start_step)
    else:
        start_index = -1

    if func_imports is None:
        func_imports = []

    func_imports_ = {k: f"def {k}(*args, **kwargs): return {v}" for k, v in func_steps_output.items()}
    func_imports_ = [v for k, v in func_imports_.items() if func_steps.index(k) < start_index]
    func_imports += func_imports_
    func_imports = [f"    {v}" for v in func_imports if not v.startswith('    ')]
    func_imports = '\n'.join(func_imports)
    func_source = inspect.getsource(pipeline)

    # delete kfp stuff
    func_source = func_source.replace('.outputs[\'output\']', '')
    func_source = func_source.replace('.outputs', '._asdict()')
    func_source = func_source.replace('.output', '')
    func_source = re.sub('.set_memory_limit.+\)', '', func_source)  # noqa
    func_source = re.sub('.set_display_name.+\)', '', func_source)  # noqa
    func_source = re.sub('.set_gpu_limit.+\)', '', func_source)  # noqa
    func_source = re.sub('.add_node_selector_constraint.+\)', '', func_source)  # noqa


    func_source = func_source.replace('.component_spec', '')
    # func_source = func_source.replace('with Condition', 'if')

    func_source = re.sub(r'with Condition[\(](.+?)[\,](.+?):', 'if \\1:', func_source)
    func_source = func_source.replace('\'None\'', 'None')

    func_source_index_def = func_source.index(f"def {pipeline.__name__}")
    func_source = func_source[func_source_index_def:]
    func_source_index_end_def = func_source.index("):")
    func_source_def = func_source[:func_source_index_end_def + 3]

    func_source_body = func_source[func_source_index_end_def + 3:]
    func_source_body = re.sub(r'([\s\,\=\:])str[\(](.+?)[\)]', '\\1\\2', func_source_body)

    exec_source = f"{func_source_def}\n{func_imports}\n{func_source_body}\n{pipeline.__name__}(**kwargs)"
    print(exec_source)

    exec(exec_source)  # noqa


def main():
    """Execute main program."""
    fire.Fire(run_kfp_pipeline_local)
    print('\x1b[6;30;42m', 'Success!', '\x1b[0m')


if __name__ == "__main__":
    main()
