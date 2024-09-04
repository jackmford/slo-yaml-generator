# slo-yaml-generator

:bangbang: This project is under development and subject to change. :bangbang:

Quickly generate [OpenSLO](https://github.com/OpenSLO/OpenSLO) and
[Nobl9](https://docs.nobl9.com/yaml-guide) yaml so I can stop going and looking
at the doc.

## Usage

1. Install using pip
    ```
    pip install slo_yaml_generator
    ```

The script takes a json file containing the fields needed for each template.

Files are currently sent to the ./output/ directory. I plan to add an option to
configure this soon.

Example:

```bash
slo_yaml_generator --resource_type slo --config_file "example-configs/cloudwatch-slo.json"
```

## Config Files

### SLO

```json
{
  "resource_name": "My Demo SLO",
  "service_name": "Service Name",
  "project_name": "Project Name",
  "sli_name": "test indicator",
  "metric_source": "Dynatrace",
  "operation": "lt",
  "value": "100",
  "target": ".99",
  "duration": "28d",
  "is_rolling": "True",
  "budgeting_method": "Occurrences"
}
```

For metric_source Cloudwatch please include these fields:

```json
{
  "region": "us-east-1",
  "aws_service": "AWS/Lambda",
  "metric_name": "Errors",
  "statistic": "Sum"
}
```

For metric_source Dynatrace please include these fields:

```json
{
  "query": "dynatrace query"
}
```

## Service

```json
{
  "resource_name": "This is a test service",
  "project_name": "Jack's Project",
  "description": "This is a test description for Jack's little tool for SLO consulting"
}
```

## Project (Nobl9 format only)

```json
{
  "resource_name": "This is a test project",
  "description": "This is a test description for Jack's little tool for SLO consulting"
}
```
