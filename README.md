# kfp local
![](https://img.shields.io/badge/version-v0.0.1-blue.svg?style=for-the-badge)
![](https://img.shields.io/badge/python-3.9-blue.svg)
[![Docs](https://img.shields.io/badge/docs-confluence-013A97)]()
![](https://img.shields.io/badge/dev-orange.svg)



Utils to run 'kfp-pipeline' with only py-function components in local without kubernetes & docker build.

Main purpose is to debug faster in early stages. 


## Getting Started
Install:

```sh
pip install kfp-local
```

Assume you have
1) a custom library with a custom function
```py
def add_op(a: float, b: float) -> float:
    '''Calculates sum of two arguments.'''
    return a + b
```
2) a kfp component based on the function
```py 
from kfp.v2.dsl import component
@component(base_image=custom_image_with_my_library_installed)
def add_op(a: float, b: float) -> float:
    kwargs = locals()
    from my_library import add_op
    return add_op(**kwargs)
```

3) a kfp pipeline using the kfp component
```py 
@pipeline
def add_pipeline(
            a: float = 1,
            b: float = 7
    ):
    first_add_task = add_op(a, 4)
    second_add_task = add_op(first_add_task.output, b)
```

Then you would push your image `custom_image_with_my_library_installed` to a container registry.
And compile it to a `yaml` to then run it in top of a kubernetes.

With `kfp-local` you can avoid this, and run your code locally on your computer doing
```py
from kfp_local import create_run_from_pipeline_func_locally
arguments = dict(a=1,b=2)
func_imports = ["from my_library import add_op"]
create_run_from_pipeline_func_locally(add_pipeline, arguments=arguments, func_imports=func_imports)
```

## Why run locally a kubernetes orchestrator?
Here we're assuming that all components are based on custom-made functions.
To debug those,
1) debugging them separately is not practical nor accurate (cause are build to interact with each other)
2) create (and mantain) 2 pipelines, one for local and other for kubeflow is painful and error pruning

Typical usage of `kfp-local` would be to debug your custom code locally with very few data samples.
Check that code works fine, and then run it in kubernetes with all samples.# kubeflow-local
