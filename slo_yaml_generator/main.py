import argparse
import importlib.resources as pkg_resources
import templates
import json
import os
import re

from jinja2 import Template


def clean_name(name):
    name = name.replace(" ", "-").lower()
    name = re.sub(r"[^a-zA-Z0-9_-]+", "", name)
    return name


def make_file(yaml_input, filename, project_name):
    with open(f"./output/openslo-formatted-{filename}", "w") as file:
        file.write(yaml_input)
        file.close()
    out = os.system(f"oslo validate -f ./output/openslo-formatted-{filename}")
    if out == 0:
        print("Converting OpenSLO format to Nobl9...")
        out = os.system(
            f"oslo convert -f ./output/openslo-formatted-{filename} -p {project_name} -o nobl9 > ./output/nobl9-formatted-{filename}"
        )
        if out == 0:
            print("Successfully converted.")
    return


def make_slo(args):
    with open(args.config_file, "r") as file:
        json_config = json.loads(file.read())
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
        with pkg_resources.open_text(templates, "cloudwatch-slo.yaml.j2") as file:
            yaml_template = file.read()

        template = Template(yaml_template)
        processed_slo = template.render(json_config)

    elif json_config["metric_source"].lower() == "dynatrace":
        with pkg_resources.open_text(templates, "dynatrace-slo.yaml.j2") as file:
            yaml_template = file.read()

        template = Template(yaml_template)
        processed_slo = template.render(json_config)

    else:
        return

    make_file(
        processed_slo,
        f"{json_config["resource_name"]}-slo.yaml",
        json_config["project_name"],
    )


def make_service(args):
    with open(f"{args.config_file}", "r") as file:
        json_config = json.loads(file.read())

    with pkg_resources.open_text(templates, "service.yaml.j2") as file:
        yaml_template = file.read()

    template = Template(yaml_template)

    json_config["resource_name"] = clean_name(json_config["resource_name"])
    json_config["project_name"] = clean_name(json_config["project_name"])

    processed_service = template.render(json_config)
    make_file(
        processed_service,
        f"{json_config["resource_name"]}-service.yaml",
        json_config["project_name"],
    )
    return


def make_project(args):
    with open(f"{args.config_file}", "r") as file:
        json_config = json.loads(file.read())

    with pkg_resources.open_text(templates, "project.yaml.j2") as file:
        yaml_template = file.read()

    template = Template(yaml_template)

    # Save original name as display name
    json_config["project_display_name"] = json_config["resource_name"]
    # Clean it for actual project name
    json_config["resource_name"] = clean_name(json_config["resource_name"])

    processed_project = template.render(json_config)
    with open(f"./output/{json_config["resource_name"]}-project.yaml", "w") as file:
        file.write(processed_project)
    return


def main():
    parser = argparse.ArgumentParser(description="Process Nobl9 yaml inputs.")
    parser.add_argument(
        "--resource_type", help="Project, SLO, Service, Integration", required=True
    )
    parser.add_argument("--config_file", help="Config file location", required=True)
    args = parser.parse_args()

    if args.resource_type.lower() == "project":
        make_project(args)
    elif args.resource_type.lower() == "service":
        make_service(args)
    elif args.resource_type.lower() == "slo":
        make_slo(args)
    return


if __name__ == "__main__":
    main()