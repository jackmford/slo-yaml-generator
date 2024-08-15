import argparse
import logging

from jinja2 import Template


logger = logging.getLogger(__name__)

def make_project(project_name):
    with open("./project.yaml.j2", "r") as file:
        yaml_template = file.read()

    template = Template(yaml_template)
    values = {
        "project_name": project_name
    }

    processed_project = template.render(values)
    print(processed_project)
    return

def main():
    parser = argparse.ArgumentParser(description='Process Nobl9 yaml inputs.')
    parser.add_argument("--resource_type", help="Project, SLO, Service, Integration", required=True)
    parser.add_argument("--project_name", help="Project name", required=True)
    args = parser.parse_args()

    logger.propagate
    print(args)
    print(args.resource_type)
    if args.resource_type.lower() == "project":
        make_project(args.project_name)
    logger.debug(args)
    return

if __name__ == "__main__":
    main()
