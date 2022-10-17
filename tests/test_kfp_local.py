import pytest

from edo.kfp_local.kfp_local import run_kfp_pipeline_local


def test_run_kfp_pipeline_local():
    with pytest.raises(ValueError):
        run_kfp_pipeline_local('error')
