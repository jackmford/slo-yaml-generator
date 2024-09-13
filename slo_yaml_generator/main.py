import argparse
import importlib.resources as pkg_resources
import json
import os
import re
import sys

from slo_yaml_generator import templates

from jinja2 import Template

RESOURCE_TYPES = [
    "slo",
    "project",
    "service",
    "alert_policy",
    "alert_condition",
    "alert_notification_target",
]

def clean_name(name):
    name = name.replace(" ", "-").lower()
    name = re.sub(r"[^a-zA-Z0-9_-]+", "", name)
    return name


def open_config_file(file_path):
    try:
        with open(file_path, "r") as file:
            json_config = json.loads(file.read())
    except FileNotFoundError:
        print(f"{file_path} not found. Please check your path.")
        sys.exit(1)

    return json_config


def make_file(yaml_input, filename, project_name, args):
    file_prefix = ""
    if args.outdir:
        file_prefix = args.outdir
    else:
        file_prefix = "output"

    if not os.path.exists(file_prefix):
        os.makedirs(file_prefix)

    with open(f"{file_prefix}/openslo-formatted-{filename}", "w") as file:
        file.write(yaml_input)
        file.close()

    out = os.system(f"oslo validate -f {file_prefix}/openslo-formatted-{filename}")
    if out == 0 and args.nobl9:
        print("Converting OpenSLO format to Nobl9...")
        out = os.system(
            f"oslo convert -f {file_prefix}/openslo-formatted-{filename} -p {project_name} -o nobl9 > {file_prefix}/nobl9-formatted-{filename}"
        )
        if out == 0:
            print("Successfully converted.")
    return


def make_slo(args):
    json_config = open_config_file(args.config_file)
    # Get cloudwatch specific fields
    if not "description" in json_config.keys():
        json_config["description"] = ""

    json_config["resource_name"] = json_config["resource_name"].replace(" ", "-").lower()
    json_config["resource_name"] = re.sub(
        r"[^a-zA-Z0-9_-]+", "", json_config["resource_name"]
    )

    json_config["project_name"] = json_config["project_name"].replace(" ", "-").lower()
    json_config["project_name"] = re.sub(
        r"[^a-zA-Z0-9_-]+", "", json_config["project_name"]
    )

    if json_config["metric_source"].lower() == "cloudwatch":
        with pkg_resources.files(templates).joinpath("cloudwatch-slo.yaml.j2").open("r") as file:
            yaml_template = file.read()

        template = Template(yaml_template)
        processed_slo = template.render(json_config)

    elif json_config["metric_source"].lower() == "dynatrace":
        with pkg_resources.files(templates).joinpath("dynatrace-slo.yaml.j2").open("r") as file:
            yaml_template = file.read()

        template = Template(yaml_template)
        processed_slo = template.render(json_config)

    else:
        return

    make_file(
        processed_slo,
        f"{json_config["resource_name"]}-slo.yaml",
        json_config["project_name"],
        args,
    )


def make_service(args):
    json_config = open_config_file(args.config_file)

    with pkg_resources.files(templates).joinpath("service.yaml.j2").open("r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)

    json_config["resource_name"] = clean_name(json_config["resource_name"])
    json_config["project_name"] = clean_name(json_config["project_name"])

    processed_service = template.render(json_config)
    make_file(
        processed_service,
        f"{json_config["resource_name"]}-service.yaml",
        json_config["project_name"],
        args,
    )
    return


def make_alert_policy(args):
    json_config = open_config_file(args.config_file)

    with pkg_resources.files(templates).joinpath("alert_policy.yaml.j2").open("r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)

    json_config["resource_name"] = clean_name(json_config["resource_name"])
    json_config["project_name"] = clean_name(json_config["project_name"])

    processed_alert_policy = template.render(json_config)
    make_file(
        processed_alert_policy,
        f"{json_config["resource_name"]}-alert-policy.yaml",
        json_config["project_name"],
        args,
    )
    return


def make_alert_condition(args):
    json_config = open_config_file(args.config_file)

    with pkg_resources.files(templates).joinpath("alert_condition.yaml.j2").open("r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)

    json_config["resource_name"] = clean_name(json_config["resource_name"])
    json_config["project_name"] = clean_name(json_config["project_name"])

    processed_alert_policy = template.render(json_config)
    make_file(
        processed_alert_policy,
        f"{json_config["resource_name"]}-alert-condition.yaml",
        json_config["project_name"],
        args,
    )
    return

def make_project(args):
    json_config = open_config_file(args.config_file)

    with pkg_resources.files(templates).joinpath("project.yaml.j2").open("r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)

    # Save original name as display name
    json_config["project_display_name"] = json_config["resource_name"]
    # Clean it for actual project name
    json_config["resource_name"] = clean_name(json_config["resource_name"])

    processed_project = template.render(json_config)
    #with open(f"./output/{json_config["resource_name"]}-project.yaml", "w") as file:
    if args.outdir:
        if not os.path.exists(args.outdir):
            os.makedirs(args.outdir)
        with open(f"{args.outdir}/{json_config["resource_name"]}-project.yaml", "w") as file:
            file.write(processed_project)
    else:
        with open(f"./output/{json_config["resource_name"]}-project.yaml", "w") as file:
            file.write(processed_project)
    return


def main():
    parser = argparse.ArgumentParser(description="Process Nobl9 yaml inputs.")
    parser.add_argument(
        "--resource_type", help="Project, SLO, Service, Integration", required=True
    )
    parser.add_argument("--config_file", help="Config file location", required=True)
    parser.add_argument("--nobl9", help="Generate Nobl9 configuration", nargs="?", const=True, default=False)
    parser.add_argument("--outdir", help="Specify directory to write output files")
    args = parser.parse_args()

    if args.resource_type.lower() == "project":
        make_project(args)
    elif args.resource_type.lower() == "service":
        make_service(args)
    elif args.resource_type.lower() == "slo":
        make_slo(args)
    elif args.resource_type.lower() == "alert_policy":
        make_alert_policy(args)
    elif args.resource_type.lower() == "alert_condition":
        make_alert_condition(args)
    else:
        print("resource_type must be of type: " + str(RESOURCE_TYPES))

    return


if __name__ == "__main__":
    main()
