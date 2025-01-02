# BUD-E explains itself

<p align="center">
  <a href="https://youtu.be/RYdWd7hRZQk">
    <img src="https://github.com/LAION-AI/Desktop_BUD-E/blob/main/BUD-E-Yt.jpg?raw=true" alt="BUD-E Framework Introduction">
  </a>
</p>

## Project Vision

BUD-E, short for "Buddy", is an innovative voice assistant framework designed to be a plug-and-play interface that allows seamless interaction with open-source AI models and API interfaces. The framework aims to empower anyone to contribute and innovate, particularly in education and research, by maintaining a low entry threshold for writing new skills and building a supportive community.

## Key Features and Flexibility

BUD-E integrates several core components including a speech-to-text model, a language model, and a text-to-speech model. These components are interchangeable and can be accessed either locally or through APIs. The framework supports integration with services from leading providers like OpenAI and Anthropic, or allows users to deploy their own models using open-source frameworks like Ollama or VLLM.

### Skills Interface

Any Python function can become a skill, allowing the voice assistant to handle tasks ranging from processing screenshots with captioning and OCR models to interacting with clipboard contents including text, images, and links. BUD-E supports dynamic skill activation, either by allowing the language model to choose a skill from a "menu" that gets dynamically added to the system prompt or through direct keywords said by the user. 
Skills get dynamically added from the "skills" folder to the system, without any need to change the main code (buddy.py). Think of it as similar to adding mods to the "Mods" folder in Minecraft.

## Community and Educational Focus

BUD-E is dedicated to fostering a community-centric development environment with a strong emphasis on education and research. The framework encourages the development of skills that aid in educational content delivery, such as navigating through specific online courses or generating custom learning paths from YouTube playlists.

## Installation Instructions

The current version of BUD-E currently uses Deepgram for the audio service and Groq the LLM. For the wake word detection it uses Porcupine from Pico Voice ( https://picovoice.ai/platform/porcupine/ ). We are working on a stack of open source models that can very soon run it completely local or on your own API server.

Recommendation: Make a venv and install everything in the venv. Make sure your microphone works.

Set your API keys here:
```sh
echo 'export PORCUPINE_API_KEY="yourporcupineapikeyhere"' >> ~/.bashrc
echo 'export GROQ_API_KEY="yourgroqapikeyhere"' >> ~/.bashrc
echo 'export DEEPGRAM_API_KEY="yourdeepgramapikeyhere"' >> ~/.bashrc
source ~/.bashrc
```

Clone the repository and install the required packages:
```sh
git clone https://github.com/christophschuhmann/Desktop_BUD-E
pip install -U -r requirements.txt
python3 buddy.py
```

## Plan Management
## Plan Management and Visualization
The BUD-E framework now includes a plan management feature that allows users to create, update, mark items as completed, and retrieve plans. Additionally, users can visualize their plans using Gantt charts, which is useful for managing tasks and keeping track of progress.

### Creating a New Plan

To initialize a new plan, use the `initialize_plan` function. This will create a new plan with empty tasks and completed tasks lists.

```python
from plan_manager import initialize_plan

initialize_plan()
```

### Updating a Plan

To update a plan with new tasks or information, use the `update_plan` function. You need to provide a task ID and task information.

```python
from plan_manager import update_plan

update_plan("task1", {"description": "Complete the project", "due_date": "2023-12-31"})
```

### Marking Items as Completed

To mark a task as completed, use the `mark_item_completed` function with the task ID.

```python
from plan_manager import mark_item_completed

mark_item_completed("task1")
```

### Visualizing the Plan

To visualize the current plan, use the `visualize_plan` function. This will generate an interactive Gantt chart that displays the tasks, their start and end dates, and their completion status.

```python
from skills import visualize_plan

visualize_plan()
```

This feature uses the `plotly` library to create the Gantt chart, which allows users to interact with the chart by zooming and panning.

### Retrieving the Plan
### Visualizing the Plan

To visualize the current plan, use the `visualize_plan` function. This will generate an interactive Gantt chart that displays the tasks, their start and end dates, and their completion status.

```python
from skills import visualize_plan

visualize_plan()
```

This feature uses the `plotly` library to create the Gantt chart, which allows users to interact with the chart by zooming and panning.

### Retrieving the Plan
To retrieve the current state of the plan, use the `get_plan` function.

```python
from plan_manager import get_plan

current_plan = get_plan()
print(current_plan)
```

## Dependencies

To enable the plan visualization feature, ensure that the following dependencies are installed:

- `plotly`: Used for generating interactive Gantt charts.
- `pandas`: Required for data manipulation and preparation for visualization.

These dependencies can be installed via the `requirements.txt` file.

## Dependencies

To enable the plan visualization feature, ensure that the following dependencies are installed:

- `plotly`: Used for generating interactive Gantt charts.
- `pandas`: Required for data manipulation and preparation for visualization.

These dependencies can be installed via the `requirements.txt` file.

## Skills

### Types of Skills
BUD-E supports two types of skills: LM Activated Skills and Keyword Activated Skills.

#### LM Activated Skills
These are Python functions that the language model (LM) can call when it deems the function useful for a given request. Each LM Activated Skill requires a specific comment structure before the function definition.

Example:
```python
# LM ACTIVATED SKILL: TITLE: Weather Report DESCRIPTION: Provides the current weather for a given location. USAGE INSTRUCTIONS: To use this skill, call it with the following tags: <weather_report> ... </weather_report> Example: <weather_report> Hamburg </weather_report>
def weather_report(location):
    # Implementation to fetch and return weather report for the location
    pass
```

#### Keyword Activated Skills
These skills are activated based on specific keyword combinations present in the user's input. They also require a specific comment structure before the function definition.

Example:
```python
# KEYWORD ACTIVATED SKILL: [["weather", "report"], ["forecast", "today"]]
def weather_report_skill():
    # Implementation to fetch and return today's weather forecast
    pass
```

### Skill Usage
Skills in the BUD-E framework are used either by the language model dynamically choosing the appropriate skill or by the user triggering them through specific keywords. The integration of skills is seamless, allowing for an intuitive and flexible interaction with the voice assistant.


## Call for Collaboration

This project is led by LAION, with support from Intel, Camb AI, Alignment Labs, the Max Planck Institute for Intelligent Systems in Tübingen, and the Tübingen AI Center. We invite collaboration from open-source communities, educational and research institutions, and interested companies to help scale BUD-E’s impact.

We encourage contributions that push the boundaries of educational and research tools, leveraging the collective creativity and expertise of the global open-source community.