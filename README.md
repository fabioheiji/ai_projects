# GitHub AI Projects

This repository contains various AI projects implemented in Python. Below is a brief description of each project and its components.

## Projects

### AI Voice Agent
- **File:** `ai_voice_agent/langgraph_tools_chatgpt_elevenlabs_voice_pt_br.py`
- **Description:** This script integrates ChatGPT and ElevenLabs for creating a voice agent that communicates in Brazilian Portuguese.

### Product Offering Optimization
- **File:** `optimization/product_offering_optimization/test_pyomo.ipynb`
- **Description:** This Jupyter Notebook uses Pyomo to optimize product offerings based on various parameters such as net sales, OTIF, turnover, and NPS. The optimization model selects the best SKUs to maximize net sales while satisfying constraints on OTIF, turnover, NPS, and product family diversity.

## Requirements

- Python 3.8+
- Pyomo
- Pandas
- CBC or GLPK solver

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/github_ai_projects.git
    cd github_ai_projects
    ```

2. Install the required Python packages (TO BE CREATED):
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure you have a solver installed (e.g., CBC or GLPK).

## Usage

### Running the AI Voice Agent
1. Navigate to the `ai_voice_agent` directory.
2. Run the script:
    ```sh
    python langgraph_tools_chatgpt_elevenlabs_voice_pt_br.py
    ```

### Running the Product Offering Optimization
1. Open the Jupyter Notebook `test_pyomo.ipynb` in the `optimization/product_offering_optimization` directory.
2. Execute the cells to run the optimization model.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

