import pytest

from kfp_local import LocalClient


def test_run_kfp_pipeline_local():
    local_client = LocalClient()

    with pytest.raises(ValueError):
        local_client.create_run_from_pipeline_func('error')



    def add_pipeline(
            a='1',
            b='7',
    ):
        def add_op(a: float, b: float) -> float:
            '''Calculates sum of two arguments.'''
            return a + b
        first_add_task = add_op(a, 4)
        second_add_task = add_op(first_add_task.output, b)
        return second_add_task

    arguments = {'a': 7, 'b': 8}
    local_client.create_run_from_pipeline_func(add_pipeline, arguments=arguments)
