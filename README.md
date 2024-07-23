# Markdown Exam Generator

This project combines multiple Markdown files into a single file and generates multiple-choice exam questions based on the combined content using the OpenAI API.

## Table of Contents

- [Markdown Exam Generator](#markdown-exam-generator)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  - [Contact](#contact)

## Prerequisites

- Python 3.x
- OpenAI API key

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/markdown-exam-generator.git
   cd markdown-exam-generator
   ```

2. **Create and activate a virtual environment**:

   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   - In the root directory of your project, create a file named `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. **Run the script**:

   ```bash
   python generate_exam.py
   ```

2. **Follow the prompts**:

   - Enter the number of lines to read from each Markdown file.
   - Enter the number of questions you want to generate (in increments of 10).

3. **Output**:
   - The combined Markdown content will be saved to `combined.md`.
   - The generated exam questions will be saved to `exam_questions.json`.

## Configuration

- **.env file**:
  - Store your OpenAI API key in the `.env` file:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenAI](https://www.openai.com/) for the API.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for managing environment variables.

## Contact

Created by [noclipping](https://github.com/noclipping) - feel free to contact me!
