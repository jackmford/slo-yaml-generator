import argparse
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
    service_name = input("Service name\n")
    print(service_name)
    sli_name = input("SLI Name\n")
    metric_source = input("Metric Source (Cloudwatch/Dynatrace)\n")
    if metric_source.lower() == "cloudwatch":
        region = input("Region\n")
        aws_service = input("AWS Service\n")
        metric_name = input("Metric name\n")
        statistic = input("Statistic\n")

        # TODO: figure out how to do dimensions

    elif metric_source.lower() == "dynatrace":
        query = input("Query\n")

    slo_name = input("SLO Name\n")
    operation = input("Operation (gte, lte, gt, lt)\n")
    value = input("SLI Value\n")
    target = input("SLO Target\n")
    time_window = input("Time Window (28d, 24h, etc.)\n")
    is_rolling = input("True/False\n")
    budgeting_method = input("Occurrences/Timeslices\n")

    values = {
        "service_name": service_name,
        "sli_name": sli_name,
        "metric_source": metric_source,
        "slo_name": slo_name,
        "operation": operation,
        "value": value,
        "target": target,
        "time_window" : time_window,
        "is_rolling": is_rolling,
        "budgeting_method": budgeting_method
    }

    if metric_source.lower() == "cloudwatch":
        values["region"] = region
        values["aws_service"] = aws_service
        values["metric_name"] = metric_name
        values["statistic"] = statistic
    elif metric_source.lower() == "dynatrace":
        values["query"] = query



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
