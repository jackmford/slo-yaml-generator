import argparse
import logging
import os

from jinja2 import Template


logger = logging.getLogger(__name__)

def make_service(args):
    with open("./templates/openslo-service.yaml.j2", "r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)
    values = {
        "project_name": args.project_name,
        "service_name": args.resource_name
    }

    if args.description:
        values["description"] = args.description

    processed_service = template.render(values)
    with open("./templates/tmp-service.yaml", "w") as file:
        file.write(processed_service)
        file.close()
    out = os.system("oslo validate -f ./templates/tmp-service.yaml")
    print(out)
    if out == 0:
        print("yay")
        out = os.system(f"oslo convert -f ./templates/tmp-service.yaml -p {args.project_name} -o nobl9 > ./output/service.yaml")
    os.remove("./templates/tmp-service.yaml")
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
    args = parser.parse_args()

    print(args)
    print(args.resource_type)
    if args.resource_type.lower() == "project":
        make_project(args)
    elif args.resource_type.lower() == "service":
        make_service(args)
    logger.debug(args)
    return

if __name__ == "__main__":
    main()
