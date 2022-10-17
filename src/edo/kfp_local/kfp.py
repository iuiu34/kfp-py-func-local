"""Run pipeline."""
import inspect
import os
import subprocess  # noqa

import fire
from google.cloud import aiplatform
from kfp.v2 import compiler


def docker_build_vm_(base_image):
    """Build docker image in vm."""
    script = 'container/vm_docker_build.sh'
    script = f'sh {script} {base_image}'
    # script = "pwd"

    # we call 2 times, 1 to display output at runtime, 2 to catch error (if any)
    out = subprocess.run(script, shell=True, capture_output=False)  # noqa
    # out = subprocess.run(script, shell=True, capture_output=True)  # noqa

    if out.stderr:
        raise subprocess.CalledProcessError(
            returncode=out.returncode,
            cmd=out.args,
            stderr=out.stderr
        )


def docker_build_(base_image, print_log, vm):
    """Build docker image."""
    print('docker')
    print('build')
    if vm:
        docker_build_vm_(base_image)
        return
    else:
        import docker  # noqa
        client_docker = docker.from_env()
        print(f"docker image: {base_image}")
        _, log = client_docker.images.build(path='.', dockerfile='container/Dockerfile', tag=base_image)
        if print_log:
            log2 = [v['stream'] for v in log if 'stream' in v.keys()]
            for line in log2:
                print(line)

        print('push')
        log = client_docker.images.push(base_image)

        if print_log:
            print(log)


# vertex-build-run
def pipeline_build(project=None, output_path=None,
                   slack=False,
                   cache_timestamp=None,
                   pipeline=None,
                   display_name=None, **kwargs):
    """Build vertex pipeline."""
    print('define pipeline')
    print('kfp')
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    pipeline_filename = 'tmp/kfp_pipeline.json'
    args_pipeline = kwargs

    pipeline_parameters_ = inspect.signature(pipeline).parameters.keys()
    args_churn_pipeline_update = dict(
        cache_timestamp=str(cache_timestamp),
        output_path=output_path,
        project=project
    )

    # only update params if exist in pipeline
    args_churn_pipeline_update = {k: v for k, v in args_churn_pipeline_update.items()
                                  if k in pipeline_parameters_}
    args_pipeline.update(
        **args_churn_pipeline_update
    )

    compiler.Compiler().compile(pipeline_func=pipeline,
                                package_path=pipeline_filename,
                                pipeline_parameters=args_pipeline)

    aiplatform.init(project=project)
    if cache_timestamp is None:
        enable_caching = False
    else:
        enable_caching = True
    job = aiplatform.PipelineJob(
        enable_caching=enable_caching,
        display_name=display_name,
        location='europe-west1',
        template_path=pipeline_filename,
        project=project,
        pipeline_root=output_path,
    )

    if display_name.startswith('ds'):
        experiment = display_name[3:]
    else:
        experiment = display_name

    service_account_email = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_MAIL')
    job.submit(service_account=service_account_email, experiment=experiment)

    if slack:
        # edo-ds-mkt-lib-slack-bot
        command = f'slack_ds_mkt {job.resource_name}'
        cmd = f'sh gcloud compute ssh "docker" --zone=europe-west1-b --command="{command}"'
        subprocess.run(cmd)  # noqa

    return


def run_kfp_pipeline(docker_build=True,
                     docker_build_vm=True,
                     kfp_build=True,
                     print_log=False,
                     base_image=None,
                     **kwargs):
    """Run vertex pipeline."""
    if docker_build:
        docker_build_(base_image, print_log, vm=docker_build_vm)
    if kfp_build:
        pipeline_build(**kwargs)


def main():
    """Execute main program."""
    fire.Fire(run_kfp_pipeline)
    print('\x1b[6;30;42m', 'Success!', '\x1b[0m')


if __name__ == "__main__":
    main()
