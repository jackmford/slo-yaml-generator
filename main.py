import argparse
import json
import logging
import os

from jinja2 import Template

logger = logging.getLogger(__name__)

def make_file(yaml_input, filename, args):
    with open(f"./output/openslo-formatted-{filename}", "w") as file:
        file.write(yaml_input)
        file.close()
    out = os.system(f"oslo validate -f ./output/openslo-formatted-{filename}")
    print(out)
    if out == 0:
        print("yay")
        out = os.system(f"oslo convert -f ./output/openslo-formatted-{filename} -p {args.project_name} -o nobl9 > ./output/nobl9-formatted-{filename}")
    return


def make_slo(args):
    if args.config_file:
        with open("./config/slo.json", "r") as file:
            json_config = json.loads(file.read())
    # Get cloudwatch specific fields
    if json_config["metric_source"].lower() == "cloudwatch":

        with open("./templates/cloudwatch-slo.yaml.j2", "r") as file:
            yaml_template = file.read()

        template = Template(yaml_template)
        processed_slo = template.render(json_config)

    # Get dynatrace specific fields
    elif json_config["metric_source"].lower() == "dynatrace":
        query = input("Query\n")
        json_config["query"] = query

    make_file(processed_slo, f"{args.resource_name}-slo.yaml", args)


def make_service(args):
    with open("./templates/service.yaml.j2", "r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)
    values = {
        "project_name": args.project_name,
        "service_name": args.resource_name
    }

    if args.description:
        values["description"] = args.description

    processed_service = template.render(values)
    make_file(processed_service, f"{args.resource_name}-service.yaml", args)
    return

def make_project(project_name):
    with open("./templates/project.yaml.j2", "r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)
    values = {
        "project_name": project_name
    }

    processed_project = template.render(values)
    # Need to write tmp file, push it to n9, and delete it
    print(processed_project)
    return

def main():
    parser = argparse.ArgumentParser(description='Process Nobl9 yaml inputs.')
    parser.add_argument("--project_name", help="Project Name", required=True)
    parser.add_argument("--resource_type", help="Project, SLO, Service, Integration", required=True)
    parser.add_argument("--resource_name", help="Resource name", required=True)
    parser.add_argument("--description", help="Description of resource")
    parser.add_argument("--config_file", help="Config file location")
    args = parser.parse_args()

    print(args)
    print(args.resource_type)
    if args.resource_type.lower() == "project":
        make_project(args)
    elif args.resource_type.lower() == "service":
        make_service(args)
    elif args.resource_type.lower() == "slo":
        make_slo(args)
    logger.debug(args)
    return

if __name__ == "__main__":
    main()
