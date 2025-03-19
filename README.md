# SS WAT Application - in progress

![Files selection](/docs/files_selection.png)

## Overview
The SS WAT Application is a Python-based tool designed to help student government with their actions e.g. manage and analyze student payment data. It provides a user-friendly interface for selecting and processing PDF, DOCX and Excel files, extracting relevant information, and updating records accordingly.

![Excel options](/docs/excel_options.png)

## Features
- **Navigation Panel** (needs update): A left & top navigation panels with tabs, forward and backward arrows for easy navigation.
- **File Selection**: Allows users to select multiple PDF, DOCX and Excel files for processing.
- **Data Analysis**: Reads and analyzes data from the selected files, updating Excel records based on the analysis.
- **Logging**: Generates detailed logs of the application's operations and data processing steps.

![Logs summary](/docs/logs_summary.png)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Farcryx/ss-wat-app.git
    ```
2. Navigate to the project directory:
    ```sh
    cd ss-wat-app
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Project Structure
- `app.py`: Main application file.
- `src/logic/`: Directory containing application logic.
- `frames/`: Directory containing the different frames used in the application.
- `logs/`: Directory where log files are stored.

## Author
Łukasz Sokół
