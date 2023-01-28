# SurveyGuru

Smart survey data generation

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Example](#example)

### Installation

Run the following commands:

```
pip install https://github.com/jkalasas/SurveyGuru.git
```

_Note that python 3.6 or above should be installed int the system_

### Usage

Run the following commands:

```
surveyguru --input [json/yaml filename] --population [number_of_samples] --output [output_filename]
```

_The output file is optional, if not especified it will default to the current time._

#### Example

##### test.json

```json
{
  "title": "Testing survey",
  "description": "This is a test survey",
  "questions": [
    {
      "id": 1,
      "question": "This is a test question",
      "options": [
        {
          "name": "Option 1",
          "value": 1
        },
        {
          "name": "Option 2",
          "value": 2
        },
        {
          "name": "Option 3",
          "value": 3
        }
      ]
    },
    {
      "id": 2,
      "question": "This is a test question 2",
      "options": [
        {
          "name": "Option 1",
          "value": 1
        },
        {
          "name": "Option 2",
          "value": 2
        },
        {
          "name": "Option 3",
          "value": 3
        }
      ]
    }
  ],
  "connections": [
    {
      "affector": 1,
      "affected": 2,
      "effect": 1,
      "weight": 1
    }
  ]
}
```

Running the commmand:

```
surveyguru --input test.json --population 100 -o test_output.csv
```

This will produce a csv file _test_output.csv_ with the generated answers.

